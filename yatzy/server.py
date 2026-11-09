#!/usr/bin/env python3
"""Yatzy tillsammans - server.

Grown out of start_yatzy.py: same idea, but the game lives on the server so a
phone and a TV can look at the same scoreboard.

Games are kept in rooms named by a short code (e.g. BJORN). There are no
accounts and no passwords: whoever has the code is in the game.

State is written to yatzy-data.json so a restart does not lose a game.

Run:
    python3 server.py                 # http://0.0.0.0:8765
    python3 server.py --port 8080
    python3 server.py --host 127.0.0.1 --no-browser
"""

import argparse
import json
import os
import random
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "yatzy-data.json"

# Swedish Yatzy, not American Yahtzee: 15 categories, bonus at 63.
UPPER = ["ettor", "tvaor", "treor", "fyror", "femmor", "sexor"]
LOWER = [
    "ett_par", "tva_par", "tretal", "fyrtal",
    "liten_stege", "stor_stege", "kak", "chans", "yatzy",
]
CATEGORIES = UPPER + LOWER
BONUS_LIMIT = 63
BONUS_VALUE = 50

# No vowels that make real words, no 0/O or 1/I confusion when read off a TV.
CODE_LETTERS = "ABCDEFGHJKLMNPQRSTUVXYZ"

_lock = threading.Lock()
_rooms = {}


# ── persistence ─────────────────────────────────────────────────────────────
def load_rooms():
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        # A corrupt file should not stop the app: start fresh rather than crash
        # on a Friday evening with the family waiting.
        return {}


def save_rooms():
    tmp = DATA_FILE.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(_rooms, f, ensure_ascii=False, indent=1)
        os.replace(tmp, DATA_FILE)
    except OSError:
        pass


# ── game logic ──────────────────────────────────────────────────────────────
def new_room(code, players):
    return {
        "code": code,
        "players": players,
        "scores": {p: {} for p in players},
        "turn": 0,
        "created": time.time(),
        "updated": time.time(),
        "version": 1,
    }


def make_code():
    while True:
        code = "".join(random.choice(CODE_LETTERS) for _ in range(5))
        if code not in _rooms:
            return code


def upper_sum(scores):
    return sum(v for k, v in scores.items() if k in UPPER and isinstance(v, int))


def totals(room, player):
    s = room["scores"].get(player, {})
    up = upper_sum(s)
    bonus = BONUS_VALUE if up >= BONUS_LIMIT else 0
    low = sum(v for k, v in s.items() if k in LOWER and isinstance(v, int))
    return {
        "upper": up,
        "bonus": bonus,
        "lower": low,
        "total": up + bonus + low,
        "filled": len([k for k in s if k in CATEGORIES]),
        "to_bonus": max(0, BONUS_LIMIT - up),
    }


def public(room):
    out = dict(room)
    out["totals"] = {p: totals(room, p) for p in room["players"]}
    out["categories"] = {"upper": UPPER, "lower": LOWER}
    done = all(
        len([k for k in room["scores"].get(p, {}) if k in CATEGORIES]) == len(CATEGORIES)
        for p in room["players"]
    ) if room["players"] else False
    out["finished"] = done
    if done:
        best = max(room["players"], key=lambda p: totals(room, p)["total"])
        out["winner"] = best
    return out


# ── http ────────────────────────────────────────────────────────────────────
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(APP_DIR), **kw)

    def log_message(self, fmt, *args):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(n) or b"{}")
        except (ValueError, TypeError):
            return {}

    def do_GET(self):
        path = self.path.split("?")[0]

        # /tv/CODE and /spel/CODE are entry points; the page reads the code itself
        if path.startswith("/tv/"):
            self.path = "/tv.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        if path.startswith("/spel/"):
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        if path.startswith("/api/state/"):
            code = path.rsplit("/", 1)[-1].upper()
            # Long poll: wait for a change so the TV updates the moment a score
            # is tapped, without hammering the server.
            want = self.path.split("since=")[-1] if "since=" in self.path else "0"
            try:
                since = int(want)
            except ValueError:
                since = 0
            deadline = time.time() + 25
            while time.time() < deadline:
                with _lock:
                    room = _rooms.get(code)
                    if room is None:
                        return self._json({"error": "no_such_room"}, 404)
                    if room["version"] > since:
                        return self._json(public(room))
                time.sleep(0.4)
            with _lock:
                room = _rooms.get(code)
                return self._json(public(room) if room else {"error": "no_such_room"})

        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        path = self.path.split("?")[0]
        data = self._body()

        if path == "/api/new":
            players = [str(p).strip()[:16] for p in data.get("players", []) if str(p).strip()]
            if not 1 <= len(players) <= 8:
                return self._json({"error": "bad_players"}, 400)
            with _lock:
                code = make_code()
                _rooms[code] = new_room(code, players)
                save_rooms()
                return self._json(public(_rooms[code]))

        if path.startswith("/api/score/"):
            code = path.rsplit("/", 1)[-1].upper()
            player = str(data.get("player", ""))
            cat = str(data.get("category", ""))
            value = data.get("value")
            if cat not in CATEGORIES:
                return self._json({"error": "bad_category"}, 400)
            try:
                value = int(value)
            except (TypeError, ValueError):
                return self._json({"error": "bad_value"}, 400)
            with _lock:
                room = _rooms.get(code)
                if not room:
                    return self._json({"error": "no_such_room"}, 404)
                if player not in room["players"]:
                    return self._json({"error": "no_such_player"}, 400)
                room["scores"].setdefault(player, {})[cat] = max(0, value)
                # Next player who still has empty boxes.
                n = len(room["players"])
                for step in range(1, n + 1):
                    cand = room["players"][(room["players"].index(player) + step) % n]
                    if len([k for k in room["scores"].get(cand, {}) if k in CATEGORIES]) < len(CATEGORIES):
                        room["turn"] = room["players"].index(cand)
                        break
                room["version"] += 1
                room["updated"] = time.time()
                save_rooms()
                return self._json(public(room))

        if path.startswith("/api/undo/"):
            code = path.rsplit("/", 1)[-1].upper()
            player = str(data.get("player", ""))
            cat = str(data.get("category", ""))
            with _lock:
                room = _rooms.get(code)
                if not room:
                    return self._json({"error": "no_such_room"}, 404)
                room["scores"].get(player, {}).pop(cat, None)
                room["turn"] = room["players"].index(player) if player in room["players"] else room["turn"]
                room["version"] += 1
                room["updated"] = time.time()
                save_rooms()
                return self._json(public(room))

        return self._json({"error": "unknown"}, 404)


def main():
    ap = argparse.ArgumentParser(description="Yatzy tillsammans")
    ap.add_argument("--host", default="0.0.0.0",
                    help="0.0.0.0 so the phone and TV can reach it (default)")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    global _rooms
    _rooms = load_rooms()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://127.0.0.1:{args.port}/"
    if not args.no_browser:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()

    print(f"Yatzy tillsammans kör på port {args.port}")
    print(f"  Den här datorn:  {url}")
    print(f"  Telefon och TV:  http://<datorns-ip>:{args.port}/")
    print("Avsluta med Ctrl+C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nYatzy har stängts.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
