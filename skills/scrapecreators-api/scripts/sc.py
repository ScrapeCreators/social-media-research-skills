#!/usr/bin/env python3
"""ScrapeCreators API helper for agent skills.

Stdlib only. Saves every response to disk and prints a short JSON summary,
so large payloads never have to be pasted into the conversation.

Commands:
  sc.py call <path> [key=value ...] [--pages N] [--allow-expensive] [--no-cache] [--dry-run]
  sc.py find <words ...>     search the bundled endpoint list
  sc.py balance              remaining credits (free call)
  sc.py spent                credits spent from this output directory

Environment:
  SCRAPECREATORS_API_KEY     required for call/balance
  SC_OUT                     output directory (default ./scrapecreators-data)
  SC_BUDGET                  max credits per output directory (default 100)
  SC_CACHE_TTL_HOURS         reuse identical requests for this long (default 24)
  SC_TIMEOUT                 per-request timeout in seconds (default 120)

Exit codes: 0 ok, 1 API error, 2 usage/config error, 3 blocked by cost guard, 4 network error.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import pathlib
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://api.scrapecreators.com"
HERE = pathlib.Path(__file__).resolve().parent
ENDPOINTS_FILE = HERE / "endpoints.json"
MAX_BYTES = 50 * 1024 * 1024
EXPENSIVE_AT = 10  # credits per single request
BILLING_URL = "https://app.scrapecreators.com/billing"
KEY_URL = "https://app.scrapecreators.com"


# ---------------------------------------------------------------- utilities

def emit(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=1))
    sys.exit(code)


def fail(kind, message, code, **extra):
    emit({"ok": False, "error": kind, "message": message, **extra}, code)


def load_endpoints():
    try:
        return json.loads(ENDPOINTS_FILE.read_text(encoding="utf-8"))["endpoints"]
    except FileNotFoundError:
        fail("config", f"Missing {ENDPOINTS_FILE}. Reinstall the scrapecreators-api skill.", 2)


def base_url():
    url = os.environ.get("SCRAPECREATORS_BASE_URL", DEFAULT_BASE).rstrip("/")
    parsed = urllib.parse.urlparse(url)
    local = parsed.hostname in ("127.0.0.1", "localhost")
    if parsed.scheme != "https" and not local:
        fail("config", "SCRAPECREATORS_BASE_URL must be https (http allowed only for localhost tests).", 2)
    return url


def api_key():
    key = os.environ.get("SCRAPECREATORS_API_KEY", "").strip()
    if not key:
        fail(
            "missing_api_key",
            "SCRAPECREATORS_API_KEY is not set. Get a key at "
            f"{KEY_URL} and expose it as an environment variable. In a Claude Code cloud "
            "session add it in the environment settings (secrets / environment variables), "
            "then start a new session. Never paste the key into the chat.",
            2,
        )
    return key


def out_dir():
    d = pathlib.Path(os.environ.get("SC_OUT", "scrapecreators-data"))
    (d / "cache").mkdir(parents=True, exist_ok=True)
    return d


def ledger_total(d):
    total = 0.0
    f = d / "ledger.jsonl"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                total += float(json.loads(line).get("credits", 0) or 0)
            except (ValueError, json.JSONDecodeError):
                continue
    return total


def ledger_add(d, entry):
    with open(d / "ledger.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def base_cost(meta):
    m = re.match(r"\s*(\d+(?:\.\d+)?)", str(meta.get("credits", "1")))
    return float(m.group(1)) if m else 1.0


def estimate_cost(path, meta, params):
    """Credits for ONE request, worst case we can know before calling."""
    cost = base_cost(meta)
    notes = []
    if str(params.get("get_ad_details", "")).lower() == "true" and path == "/v1/google/company/ads":
        cost = 25
        notes.append("get_ad_details=true costs 25 credits per request")
    if str(params.get("allow_long_transcription", "")).lower() == "true":
        notes.append("allow_long_transcription=true bills 10 credits per started minute of video, even for short videos; real cost depends on duration")
        cost = max(cost, 10)
    if path == "/v1/find-creator-emails":
        notes.append("1 credit when no email is found, 10 when any email is returned")
    return cost, notes


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow redirects: the API key must not be sent anywhere else."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, f"redirect to {newurl} blocked", headers, fp)


def opener():
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    ctx = ssl.create_default_context(cafile=cafile if cafile and os.path.exists(cafile) else None)
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), NoRedirect())


def http_get(path, params, key, timeout):
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{base_url()}{path}" + (f"?{query}" if query else "")
    req = urllib.request.Request(url, headers={"x-api-key": key, "accept": "application/json",
                                               "user-agent": "scrapecreators-skill-helper/1.0"})
    attempt, delays = 0, [2, 4, 8]
    while True:
        try:
            with opener().open(req, timeout=timeout) as res:
                body = res.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    fail("too_large", "Response exceeded 50 MB. Narrow the request.", 1)
                return res.status, body
        except urllib.error.HTTPError as err:
            status = err.code
            body = err.read() if err.fp else b""
            if (status == 429 or status >= 500) and attempt < len(delays):
                time.sleep(delays[attempt])
                attempt += 1
                continue
            return status, body
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            reason = str(getattr(err, "reason", err))
            if "403" in reason and "tunnel" in reason.lower():
                fail("network_blocked",
                     "The network policy of this environment blocks api.scrapecreators.com "
                     "(proxy returned 403). Allow that host in the environment's network settings, "
                     "then retry. Do not substitute made-up data.", 4)
            if isinstance(err, TimeoutError) or "timed out" in reason:
                if attempt < 1:
                    attempt += 1
                    continue
                fail("timeout", f"No response within {timeout}s. Transcript and AI routes can be slow; "
                     "raise SC_TIMEOUT or retry once.", 4)
            fail("network", f"Network error: {reason}", 4)


def explain_status(status, data):
    msg = ""
    if isinstance(data, dict):
        msg = data.get("message") or data.get("error") or ""
    hints = {
        400: "Bad or missing parameter. Check required params in references/endpoints.md or the per-endpoint OpenAPI spec.",
        401: "API key rejected. Check SCRAPECREATORS_API_KEY.",
        402: f"No credits left. Top up at {BILLING_URL}.",
        403: "Forbidden by the API (not the network proxy). The resource may be private or the plan may not include this route.",
        404: "Endpoint or resource not found. Check the path and that the account/post is public.",
        429: "Rate limited even after retries. Wait a minute before calling again.",
    }
    if 300 <= status < 400:
        hints[status] = "The API answered with a redirect, which this helper refuses to follow so the key is not sent elsewhere."
    hint = hints.get(status, "Server error after retries. Try again later." if status >= 500 else "")
    return msg, hint


def find_items(data):
    """Return (key, count) of the biggest list at depth <= 2."""
    best = (None, 0)
    if isinstance(data, list):
        return "(root)", len(data)
    if not isinstance(data, dict):
        return best
    for k, v in data.items():
        if isinstance(v, list) and len(v) > best[1]:
            best = (k, len(v))
        elif isinstance(v, dict):
            for k2, v2 in v.items():
                if isinstance(v2, list) and len(v2) > best[1]:
                    best = (f"{k}.{k2}", len(v2))
    return best


def find_field(data, field):
    if not field or not isinstance(data, dict):
        return None
    if field in data:
        return data[field]
    for container in ("pagination", "data", "meta", "page_info", "pageInfo"):
        sub = data.get(container)
        if isinstance(sub, dict) and field in sub:
            return sub[field]
    return None


def has_more_false(data):
    if not isinstance(data, dict):
        return False
    for k in ("has_more", "hasMore", "more_available", "moreAvailable", "has_next_page", "hasNextPage"):
        if k in data and data[k] in (False, 0, "false"):
            return True
    return False


def slug(path, params):
    name = path.strip("/").replace("/", "_")
    main = next((str(params[k]) for k in ("handle", "query", "hashtag", "url", "subreddit", "channelId", "id")
                 if params.get(k)), "")
    main = re.sub(r"[^A-Za-z0-9]+", "-", main)[-40:].strip("-")
    return f"{name}__{main}" if main else name


# ---------------------------------------------------------------- commands

def cmd_find(args):
    eps = load_endpoints()
    words = [w.lower() for w in args.words]
    rows = []
    for path, m in eps.items():
        hay = f"{path} {m.get('name', '')}".lower()
        if all(w in hay for w in words):
            rows.append({"path": path, "name": m.get("name"), "required": m.get("required"),
                         "optional": m.get("optional"), "credits": m.get("credits"),
                         "page_param": m.get("page_param")})
    emit({"ok": True, "matches": len(rows), "endpoints": rows[:40]})


def cmd_balance(args):
    key = api_key()
    for path in ("/v1/credit-balance", "/v1/account/credit-balance"):
        status, body = http_get(path, {}, key, float(os.environ.get("SC_TIMEOUT", "120")))
        if status == 404:
            continue
        try:
            data = json.loads(body.decode("utf-8") or "{}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = {}
        if status != 200:
            msg, hint = explain_status(status, data)
            fail(f"http_{status}", msg or hint, 1, hint=hint)
        emit({"ok": True, "creditCount": data.get("creditCount", data)})
    fail("http_404", "Credit balance route not found.", 1)


def cmd_spent(args):
    d = out_dir()
    emit({"ok": True, "out_dir": str(d), "credits_spent": ledger_total(d),
          "budget": float(os.environ.get("SC_BUDGET", "100"))})


def parse_params(pairs):
    params = {}
    for pair in pairs:
        if "=" not in pair:
            fail("usage", f"Parameter '{pair}' must look like key=value.", 2)
        k, v = pair.split("=", 1)
        params[k.strip()] = v.strip()
    for k in ("handle", "username"):
        if params.get(k, "").startswith("@"):
            params[k] = params[k][1:]
    if params.get("hashtag", "").startswith("#"):
        params["hashtag"] = params["hashtag"][1:]
    return params


def cmd_call(args):
    eps = load_endpoints()
    raw_path = args.path.strip()
    raw_path, _, query = raw_path.partition("?")
    path = "/" + raw_path.lstrip("/")
    path = re.sub(r"^/?(https?://)?api\.scrapecreators\.com", "", path) or path
    query_pairs = [f"{k}={v}" for k, v in urllib.parse.parse_qsl(query, keep_blank_values=True)]
    meta = eps.get(path)
    if meta is None and not args.force:
        close = difflib.get_close_matches(path, list(eps), n=5, cutoff=0.6)
        fail("unknown_endpoint", f"{path} is not in the bundled endpoint list.", 2,
             did_you_mean=close, hint="Use 'sc.py find <words>' or pass --force if the API added it recently.")
    meta = meta or {"required": [], "optional": [], "credits": "1", "page_param": None, "page_field": None,
                    "params_known": False}
    params = parse_params(query_pairs + list(args.params))

    missing = [r for r in meta.get("required", []) if r not in params]
    if missing and meta.get("params_known", True):
        fail("missing_params", f"Required params missing: {', '.join(missing)}", 2,
             required=meta.get("required"), optional=meta.get("optional"))

    pages = max(1, args.pages)
    page_param, page_field = meta.get("page_param"), meta.get("page_field")
    if pages > 1 and not page_param:
        pages = 1  # endpoint has no pagination
    per_call, notes = estimate_cost(path, meta, params)
    estimate = per_call * pages

    d = out_dir()
    budget = float(os.environ.get("SC_BUDGET", "100"))
    spent = ledger_total(d)
    plan = {"path": path, "params": params, "pages": pages, "credits_per_request": per_call,
            "estimated_max_credits": estimate, "spent_so_far": spent, "budget": budget, "notes": notes}
    if args.dry_run:
        emit({"ok": True, "dry_run": True, **plan})
    if per_call >= EXPENSIVE_AT and not args.allow_expensive:
        fail("needs_confirmation",
             f"This request costs about {per_call:g} credits each ({estimate:g} total). Tell the user the cost, "
             "get a yes, then re-run with --allow-expensive.", 3, **plan)
    if spent + estimate > budget:
        fail("over_budget",
             f"Would exceed the credit budget ({spent:g} spent + {estimate:g} planned > {budget:g}). "
             "Ask the user before raising SC_BUDGET.", 3, **plan)

    key = api_key()
    timeout = float(os.environ.get("SC_TIMEOUT", "120"))
    ttl = float(os.environ.get("SC_CACHE_TTL_HOURS", "24")) * 3600
    files, total_items, charged_total, remaining = [], 0, 0.0, None
    item_key, next_value, cached_pages, last_ok, stopped = None, None, 0, {}, None
    cur = dict(params)
    if page_param == "page" and "page" not in cur:
        cur["page"] = "1"

    for i in range(pages):
        digest = hashlib.sha256(json.dumps([path, sorted(cur.items())]).encode()).hexdigest()[:16]
        cache_file = d / "cache" / f"{digest}.json"
        if not args.no_cache and cache_file.exists() and time.time() - cache_file.stat().st_mtime < ttl:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            status, charged = 200, 0.0
            cached_pages += 1
        else:
            status, body = http_get(path, cur, key, timeout)
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
            except (UnicodeDecodeError, json.JSONDecodeError):
                data = {"raw": body[:2000].decode("utf-8", "replace")}
            if status != 200:
                msg, hint = explain_status(status, data)
                if files:  # keep what we already have, but say so loudly
                    stopped = {"page": i + 1, "error": f"http_{status}", "message": msg or hint,
                               "resume_with": {page_param: cur.get(page_param)} if page_param else None}
                    break
                fail(f"http_{status}", msg or hint, 1, hint=hint, path=path)
            charged = data.get("credits_charged") if isinstance(data, dict) else None
            charged = float(charged) if isinstance(charged, (int, float)) else per_call
            if isinstance(data, dict) and isinstance(data.get("credits_remaining"), (int, float)):
                remaining = data["credits_remaining"]
            cache_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            ledger_add(d, {"ts": int(time.time()), "path": path, "params": cur, "credits": charged})
        charged_total += charged
        last_ok = data

        qid = hashlib.sha256(json.dumps([path, sorted(params.items())]).encode()).hexdigest()[:8]
        f = d / f"{slug(path, params)}__{qid}__p{i + 1}.json"
        f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        files.append(str(f))
        k, n = find_items(data)
        item_key = item_key or k
        total_items += n
        if isinstance(data, dict) and data.get("success") is False:
            if i == 0:
                fail("api_success_false", str(data.get("message") or data.get("error") or
                     "API returned success: false"), 1, path=path, files=files)
            stopped = {"page": i + 1, "error": "api_success_false",
                       "message": str(data.get("message") or data.get("error") or "")}
            break

        if i + 1 >= pages or not page_param:
            if page_param == "page":
                next_value = int(cur.get("page", "1")) + 1 if n else None
            else:
                next_value = find_field(data, page_field) if page_field else None
            break
        if page_param == "page":
            if n == 0:
                break
            cur["page"] = str(int(cur.get("page", "1")) + 1)
            continue
        nxt = find_field(data, page_field)
        if nxt in (None, "", 0, "0") or str(nxt) == str(cur.get(page_param)) or has_more_false(data) or n == 0:
            next_value = None
            break
        cur[page_param] = str(nxt)
        next_value = nxt

    sample = last_ok if isinstance(last_ok, dict) else {}
    emit({
        "ok": True,
        "complete": stopped is None,
        "stopped_early": stopped,
        "path": path,
        "files": files,
        "pages_fetched": len(files),
        "pages_from_cache": cached_pages,
        "items": total_items,
        "items_key": item_key,
        "next_cursor": next_value,
        "credits_charged": charged_total,
        "credits_remaining": remaining,
        "spent_in_out_dir": ledger_total(d),
        "top_level_keys": list(sample.keys())[:25],
        "success_flag": sample.get("success"),
    })


def main():
    ap = argparse.ArgumentParser(description="ScrapeCreators helper")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("call", help="call an endpoint")
    c.add_argument("path")
    c.add_argument("params", nargs="*", help="key=value query params")
    c.add_argument("--pages", type=int, default=1, help="follow pagination up to N pages")
    c.add_argument("--allow-expensive", action="store_true", help="allow requests costing >= 10 credits")
    c.add_argument("--no-cache", action="store_true")
    c.add_argument("--dry-run", action="store_true", help="show the plan and cost, call nothing")
    c.add_argument("--force", action="store_true", help="allow paths missing from endpoints.json")
    c.set_defaults(fn=cmd_call)
    f = sub.add_parser("find", help="search bundled endpoints")
    f.add_argument("words", nargs="+")
    f.set_defaults(fn=cmd_find)
    sub.add_parser("balance").set_defaults(fn=cmd_balance)
    sub.add_parser("spent").set_defaults(fn=cmd_spent)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
