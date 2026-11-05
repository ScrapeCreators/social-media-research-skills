"""Offline tests for sc.py against a local fake API. Run: python3 test_sc.py"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SC = pathlib.Path(__file__).resolve().parent / "sc.py"
STATE = {"calls": [], "yt_429_left": 1}


class FakeAPI(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_json(self, status, obj, headers=None):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        STATE["calls"].append((u.path, q, self.headers.get("x-api-key")))
        if self.headers.get("x-api-key") == "bad":
            return self.send_json(401, {"success": False, "message": "Invalid API key"})
        if u.path == "/v1/credit-balance":
            return self.send_json(200, {"creditCount": 500})
        if u.path == "/v1/tiktok/profile":
            return self.send_json(200, {"success": True, "user": {"uniqueId": q.get("handle")},
                                        "credits_charged": 1, "credits_remaining": 499})
        if u.path == "/v3/tiktok/profile/videos":
            cur = int(q.get("max_cursor", "0"))
            nxt = cur + 10
            return self.send_json(200, {"aweme_list": [{"id": cur + i} for i in range(5)],
                                        "max_cursor": nxt, "has_more": nxt < 30, "credits_charged": 1})
        if u.path == "/v1/linkedin/company/posts":
            page = int(q.get("page", "1"))
            return self.send_json(200, {"posts": [{"p": page}] * (3 if page < 3 else 0)})
        if u.path == "/v1/youtube/channel":
            if STATE["yt_429_left"] > 0:
                STATE["yt_429_left"] -= 1
                return self.send_json(429, {"message": "slow down"})
            return self.send_json(200, {"name": "ok"})
        if u.path == "/v1/reddit/search":
            return self.send_json(402, {"message": "Out of credits"})
        if u.path == "/v1/threads/profile":
            self.send_response(302)
            self.send_header("location", "http://127.0.0.1:1/steal")
            self.end_headers()
            return
        if u.path == "/v1/tiktok/user/audience":
            return self.send_json(200, {"audienceLocations": [{"country": "PL"}], "credits_charged": 26})
        return self.send_json(404, {"message": "not found"})


class ScTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), FakeAPI)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        STATE["calls"].clear()

    def run_sc(self, *args, key="test-key", **env):
        e = {k: v for k, v in os.environ.items() if not k.upper().endswith("_PROXY")}
        e.update({"SCRAPECREATORS_BASE_URL": self.base, "SC_OUT": self.tmp, "NO_PROXY": "*"})
        if key is None:
            e.pop("SCRAPECREATORS_API_KEY", None)
        else:
            e["SCRAPECREATORS_API_KEY"] = key
        e.update(env)
        p = subprocess.run([sys.executable, "-I", str(SC), *args], capture_output=True, text=True, env=e, timeout=60)
        return p.returncode, json.loads(p.stdout)

    def test_missing_key(self):
        code, out = self.run_sc("call", "/v1/tiktok/profile", "handle=x", key=None)
        self.assertEqual((code, out["error"]), (2, "missing_api_key"))

    def test_profile_strips_at_and_saves_file(self):
        code, out = self.run_sc("call", "v1/tiktok/profile", "handle=@charli")
        self.assertEqual(code, 0)
        self.assertEqual(STATE["calls"][0][1]["handle"], "charli")
        self.assertEqual(STATE["calls"][0][2], "test-key")
        self.assertEqual(out["credits_charged"], 1)
        self.assertEqual(out["credits_remaining"], 499)
        self.assertTrue(pathlib.Path(out["files"][0]).exists())

    def test_cache_avoids_second_charge(self):
        self.run_sc("call", "/v1/tiktok/profile", "handle=a")
        code, out = self.run_sc("call", "/v1/tiktok/profile", "handle=a")
        self.assertEqual((code, out["pages_from_cache"], out["credits_charged"]), (0, 1, 0))
        self.assertEqual(len(STATE["calls"]), 1)

    def test_cursor_pagination_stops_on_has_more(self):
        code, out = self.run_sc("call", "/v3/tiktok/profile/videos", "handle=a", "--pages", "10")
        self.assertEqual(code, 0)
        self.assertEqual(out["pages_fetched"], 3)
        self.assertEqual(out["items"], 15)
        self.assertEqual([c[1].get("max_cursor") for c in STATE["calls"]], [None, "10", "20"])

    def test_page_counter_pagination(self):
        code, out = self.run_sc("call", "/v1/linkedin/company/posts", "url=https://linkedin.com/company/x", "--pages", "5")
        self.assertEqual(code, 0)
        self.assertEqual(out["pages_fetched"], 3)
        self.assertEqual(out["items"], 6)

    def test_retry_on_429(self):
        STATE["yt_429_left"] = 1
        code, out = self.run_sc("call", "/v1/youtube/channel", "handle=x")
        self.assertEqual(code, 0)
        self.assertEqual(len(STATE["calls"]), 2)

    def test_402_explained(self):
        code, out = self.run_sc("call", "/v1/reddit/search", "query=x")
        self.assertEqual((code, out["error"]), (1, "http_402"))
        self.assertIn("billing", out["hint"])

    def test_401(self):
        code, out = self.run_sc("call", "/v1/tiktok/profile", "handle=x", key="bad")
        self.assertEqual((code, out["error"]), (1, "http_401"))

    def test_redirect_not_followed(self):
        code, out = self.run_sc("call", "/v1/threads/profile", "handle=x")
        self.assertEqual(code, 1)
        self.assertEqual(out["error"], "http_302")
        self.assertEqual(len(STATE["calls"]), 1)

    def test_expensive_needs_flag(self):
        code, out = self.run_sc("call", "/v1/tiktok/user/audience", "handle=x")
        self.assertEqual((code, out["error"]), (3, "needs_confirmation"))
        self.assertEqual(len(STATE["calls"]), 0)
        code, out = self.run_sc("call", "/v1/tiktok/user/audience", "handle=x", "--allow-expensive")
        self.assertEqual((code, out["credits_charged"]), (0, 26))

    def test_budget_blocks(self):
        code, out = self.run_sc("call", "/v3/tiktok/profile/videos", "handle=a", "--pages", "5", SC_BUDGET="3")
        self.assertEqual((code, out["error"]), (3, "over_budget"))
        self.assertEqual(len(STATE["calls"]), 0)

    def test_missing_required_param(self):
        code, out = self.run_sc("call", "/v1/reddit/search")
        self.assertEqual((code, out["error"]), (2, "missing_params"))

    def test_unknown_endpoint_suggests(self):
        code, out = self.run_sc("call", "/v1/youtube/channel/videos", "handle=x")
        self.assertEqual((code, out["error"]), (2, "unknown_endpoint"))
        self.assertIn("/v1/youtube/channel-videos", out["did_you_mean"])

    def test_dry_run_calls_nothing(self):
        code, out = self.run_sc("call", "/v1/google/company/ads", "domain=nike.com", "get_ad_details=true", "--dry-run")
        self.assertEqual((code, out["credits_per_request"]), (0, 25))
        self.assertEqual(len(STATE["calls"]), 0)

    def test_balance_and_find(self):
        code, out = self.run_sc("balance")
        self.assertEqual((code, out["creditCount"]), (0, 500))
        code, out = self.run_sc("find", "tiktok", "transcript")
        self.assertIn("/v1/tiktok/video/transcript", [e["path"] for e in out["endpoints"]])

    def test_non_https_base_rejected(self):
        code, out = self.run_sc("balance", SCRAPECREATORS_BASE_URL="http://example.com")
        self.assertEqual((code, out["error"]), (2, "config"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
