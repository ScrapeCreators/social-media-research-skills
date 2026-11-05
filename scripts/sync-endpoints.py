#!/usr/bin/env python3
"""Regenerate the scrapecreators-api endpoint reference from the official CLI config.

The ScrapeCreators CLI (https://github.com/ScrapeCreators/scrapecreators-cli)
ships the API catalog in api-config/*.js. This script reads those files as
plain text (it never imports or executes them), then writes:

  skills/scrapecreators-api/references/endpoints.md   human/agent-readable table
  skills/scrapecreators-api/scripts/endpoints.json    data used by scripts/sc.py

Usage:
  git clone --depth 1 https://github.com/ScrapeCreators/scrapecreators-cli /tmp/sc-cli
  python3 scripts/sync-endpoints.py /tmp/sc-cli
"""
import json
import pathlib
import re
import subprocess
import sys

PATH_RE = re.compile(r'^(\s+)path: "(/v\d+/[^"]+)",?\s*$')
STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def indent(line):
    return len(line) - len(line.lstrip(" "))


def read_value(lines, i, key_indent):
    """Return string value of `key: "..."` at line i (value may be on next line(s))."""
    line = lines[i]
    after = line.split(":", 1)[1].strip()
    buf = after
    j = i
    # multi-line: value starts on next line, possibly concatenated with +
    while (not buf or buf.endswith("+")) and j + 1 < len(lines):
        j += 1
        buf = (buf.rstrip("+ ") + " " + lines[j].strip()).strip()
    parts = STR_RE.findall(buf)
    if parts:
        return "".join(parts).replace('\\"', '"').replace("\\n", " ")
    m = re.match(r"`([^`]*)`", buf)
    if m:
        return m.group(1)
    return buf.rstrip(",")


def parse_file(fp):
    lines = fp.read_text(encoding="utf-8").splitlines()
    out = []
    for i, line in enumerate(lines):
        m = PATH_RE.match(line)
        if not m:
            continue
        ind = len(m.group(1))
        ep = {"path": m.group(2), "file": fp.name}
        # find object start backwards
        start = i
        while start > 0:
            s = lines[start - 1]
            if s.strip() in ("{", "...{") or (indent(s) < ind and s.strip().endswith("{")):
                break
            start -= 1
        # find object end forwards
        end = i
        while end + 1 < len(lines):
            s = lines[end + 1]
            if indent(s) < ind and s.strip().startswith("}"):
                break
            end += 1
        k = start
        while k <= end:
            s = lines[k]
            if indent(s) == ind:
                key = s.strip().split(":", 1)[0]
                if key in ("name", "method", "description", "docsPath"):
                    ep.setdefault(key, read_value(lines, k, ind))
                elif key == "paginationField":
                    ep["pagination"] = read_value(lines, k, ind)
                elif key in ("credits", "cost"):
                    raw = s.split(":", 1)[1].strip().rstrip(",")
                    if raw == "{":
                        obj = {}
                        k += 1
                        while k <= end and not (indent(lines[k]) == ind and lines[k].strip().startswith("}")):
                            st = lines[k].strip()
                            if indent(lines[k]) == ind + 2 and ":" in st:
                                kk = st.split(":", 1)[0]
                                if kk in ("type", "cost", "description"):
                                    obj[kk] = read_value(lines, k, ind + 2)
                            k += 1
                        ep["credits"] = obj
                    else:
                        ep["credits"] = raw
                elif key == "params":
                    rest = s.split(":", 1)[1].strip()
                    if rest.startswith("[") and rest != "[],":
                        params, k = parse_params(lines, k + 1, ind)
                        ep["params"] = params
                    elif rest == "[],":
                        ep["params"] = []
                    else:
                        ep["params_ref"] = rest.rstrip(",")
                elif key == "sampleResponse":
                    # skip the whole block
                    k += 1
                    while k <= end and not (indent(lines[k]) == ind and lines[k].strip().startswith("}")):
                        k += 1
            k += 1
        out.append(ep)
    return out


def parse_params(lines, k, ind):
    params, cur = [], None
    pind = None
    while k < len(lines):
        s = lines[k]
        st = s.strip()
        if indent(s) == ind and st.startswith("]"):
            break
        if st == "{" and (pind is None or indent(s) == pind):
            pind = indent(s)
            cur = {}
            params.append(cur)
        elif cur is not None and pind is not None and indent(s) == pind + 2 and ":" in st:
            key = st.split(":", 1)[0]
            if key in ("name", "type", "description", "placeholder"):
                cur[key] = read_value(lines, k, pind + 2)
            elif key == "required":
                cur["required"] = "true" in st
            elif key == "options" and st.endswith("["):
                pass
        elif st.startswith("...") and (pind is None or indent(s) <= (pind or ind + 2) + 2):
            params.append({"spread": st.rstrip(",")})
        k += 1
    return params, k


TRANSCRIPT_COST = "1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty"
CONST_COSTS = {
    "NATIVE_OR_AI_CREDITS": TRANSCRIPT_COST,
    "AI_TRANSCRIPTION_CREDITS": "1 (AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty",
}
PLATFORM_NAMES = {
    "tiktok": "TikTok", "instagram": "Instagram", "youtube": "YouTube", "facebook": "Facebook",
    "linkedin": "LinkedIn", "twitter": "Twitter / X", "reddit": "Reddit", "threads": "Threads",
    "bluesky": "Bluesky", "pinterest": "Pinterest", "truthsocial": "Truth Social", "twitch": "Twitch",
    "kick": "Kick", "snapchat": "Snapchat", "rumble": "Rumble", "google": "Google",
    "spotify": "Spotify", "apple-music": "Apple Music", "soundcloud": "SoundCloud", "github": "GitHub",
    "kwai": "Kwai", "telegram": "Telegram", "amazon": "Amazon",
}
LINK_IN_BIO = {"linktree", "komi", "pillar", "linkbio", "linkme"}


def cost_of(e):
    c = e.get("credits")
    if c is None:
        base = "1"
    elif isinstance(c, dict):
        base = c.get("cost", "1")
        if c.get("description"):
            base = f"{base} ({c['description'].rstrip('.')})"
        elif c.get("type") == "variable":
            base += " (variable)"
    else:
        base = CONST_COSTS.get(c, c)
    d = e.get("description", "")
    extra = re.findall(r"\(?(\d+) credits?\)?", d)
    if "get_ad_details" in d and "25" in d:
        base += "; 25 with get_ad_details=true"
    return base, bool(extra)


def short(text, n=110):
    text = re.sub(r"\s+", " ", text or "").strip()
    first = re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]
    return first if len(first) <= n else first[: n - 1].rstrip() + "…"


def group_of(path):
    seg = path.split("/")[2]
    if seg in LINK_IN_BIO:
        return "Link-in-bio"
    if seg in PLATFORM_NAMES:
        return PLATFORM_NAMES[seg]
    return "Account and utilities"


CURSOR_PARAMS = ["cursor", "max_cursor", "min_time", "continuationToken", "after", "next_max_id", "max_id", "paginationToken", "page"]


def paging(e):
    """Return (param, response_field) or (None, None)."""
    names = [p.get("name") for p in e.get("params", [])]
    f = e.get("pagination")
    if f and f in names:
        return f, f
    if f:
        alt = [n for n in names if n in CURSOR_PARAMS]
        return (alt[0] if alt else f), f
    alt = [n for n in names if n in CURSOR_PARAMS]
    if alt:
        return alt[0], (None if alt[0] == "page" else alt[0])
    return None, None


def generate(eps, skill_dir, cli_version, date):
    order = list(PLATFORM_NAMES.values()) + ["Link-in-bio", "Account and utilities"]
    groups = {}
    compact = {}
    for e in eps:
        params = e.get("params", [])
        req = [p["name"] for p in params if p.get("required") and "name" in p]
        opt = [p["name"] for p in params if not p.get("required") and "name" in p]
        cost, _ = cost_of(e)
        compact[e["path"]] = {
            "name": e.get("name", ""),
            "required": req,
            "optional": opt,
            "page_param": paging(e)[0],
            "page_field": paging(e)[1],
            "credits": cost,
            "params_known": "params" in e,
        }
        groups.setdefault(group_of(e["path"]), []).append((e, req, opt, cost))

    lines = [
        "# ScrapeCreators endpoint reference",
        "",
        f"Generated from the official `scrapecreators-cli` api-config (v{cli_version}, synced {date}).",
        f"{len(eps)} endpoints, all `GET`, base URL `https://api.scrapecreators.com`, header `x-api-key`.",
        "",
        "How to read this table:",
        "",
        "* **Required** must be sent. When a row lists alternatives in Optional (for example `handle` or `user_id`), one of them is usually enough; check the per-endpoint OpenAPI spec if a call returns 400.",
        "* **Pagination** is the param you pass on the next call. Its value comes from the same-named field in the previous response, unless the row shows `param ← response field`. `page` is a plain counter.",
        "* **Credits** is per successful request (per page for paginated calls). Default is 1.",
        "* Per-endpoint OpenAPI spec: `https://docs.scrapecreators.com/{path}/openapi.json`.",
        "",
        "Regenerate this file when the CLI config changes instead of editing rows by hand.",
        "",
    ]
    for g in order:
        if g not in groups:
            continue
        lines += [f"## {g}", "", "| Endpoint | Required | Optional | Pagination | Credits | What it returns |", "|---|---|---|---|---|---|"]
        for e, req, opt, cost in sorted(groups[g], key=lambda t: t[0]["path"]):
            reqs = ", ".join(f"`{r}`" for r in req) or ("-" if "params" in e else "see spec")
            opts = ", ".join(f"`{o}`" for o in opt) or "-"
            pp, pf = paging(e)
            if not pp:
                pag = "-"
            elif pp == "page":
                pag = "`page` (1, 2, 3…)"
            elif pf and pf != pp:
                pag = f"`{pp}` ← response `{pf}`"
            else:
                pag = f"`{pp}`"
            desc = short(e.get("description") or e.get("name", "")).replace("|", "/")
            lines.append(f"| `{e['path']}` | {reqs} | {opts} | {pag} | {cost.replace('|', '/')} | {desc} |")
        lines.append("")

    ref = skill_dir / "references"
    ref.mkdir(parents=True, exist_ok=True)
    (ref / "endpoints.md").write_text("\n".join(lines), encoding="utf-8")
    meta = {"source": f"scrapecreators-cli api-config v{cli_version}", "synced": date, "endpoints": compact}
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts" / "endpoints.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return {g: len(v) for g, v in groups.items()}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    cli = pathlib.Path(sys.argv[1]).resolve()
    config = cli / "api-config"
    if not config.is_dir():
        raise SystemExit(f"{config} not found. Pass the root of a scrapecreators-cli checkout.")
    version = json.loads((cli / "package.json").read_text(encoding="utf-8"))["version"]
    try:
        date = subprocess.run(["git", "-C", str(cli), "log", "-1", "--format=%cs"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        date = "unknown date"
    eps, seen = [], set()
    for fp in sorted(config.glob("*.js")):
        for e in parse_file(fp):
            key = (e["path"], e.get("method", "GET"))
            if key not in seen:
                seen.add(key)
                eps.append(e)
    skill_dir = pathlib.Path(__file__).resolve().parents[1] / "skills" / "scrapecreators-api"
    groups = generate(eps, skill_dir, version, date)
    print(f"{len(eps)} endpoints from scrapecreators-cli v{version} ({date})")
    print(", ".join(f"{g}: {n}" for g, n in groups.items()))


if __name__ == "__main__":
    main()
