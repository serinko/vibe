# Yatzy tillsammans

Håll koll på poängen när familjen spelar Yatzy. Telefonen eller datorn skriver
in poängen, TV:n visar ställningen.

Keep track of the score when the family plays Yatzy. Enter scores on a phone or
laptop, show the scoreboard on the TV.

---

# Snabbstart (svenska)

## Spela på en dator med TV:n i HDMI

1. Koppla datorn till TV:n med HDMI och välj **Utöka skärmen** (inte spegla).
2. Starta appen:

   ```sh
   ./start-yatzy.sh
   ```

3. Webbläsaren öppnas. Skriv in namnen och tryck **Starta spelet**. Du får en
   kod, till exempel `BGRVY`.
4. Öppna ett nytt webbläsarfönster, dra det till TV:n och gå till:

   ```
   http://127.0.0.1:8765/tv/BGRVY
   ```

5. Tryck **F11** för helskärm på TV:n.

Klart. Skriv in poängen på datorn, ställningen syns direkt på TV:n.

## Spela med telefoner också

1. Ta reda på datorns IP-adress:

   ```sh
   ip addr | grep 'inet 192'
   ```

2. Telefonerna öppnar `http://<DATORNS-IP>:8765/` och skriver in koden.

Om telefonen inte når datorn, öppna porten:

```sh
sudo ufw allow 8765/tcp
```

## Så fungerar spelet

- Tryck på en ruta i tabellen för att skriva in poäng. Du får bara välja
  poäng som är möjliga i den rutan.
- Turen går vidare automatiskt och hoppar över den som är färdig.
- Bonus på 50 poäng när översta delen når 63.
- Svensk Yatzy: 15 rutor, med ett par, två par, tretal, fyrtal, liten stege,
  stor stege, kåk, chans och yatzy.

Poängen sparas i `yatzy-data.json`. Ett avbrutet spel finns kvar när du startar
appen igen.

---

# Quick start (English)

## Play on one laptop with the TV on HDMI

1. Connect the laptop to the TV over HDMI and set the display to **Extend**,
   not Mirror.
2. Start the app:

   ```sh
   ./start-yatzy.sh
   ```

3. The browser opens. Type in the names and press **Starta spelet**. You get a
   code, for example `BGRVY`.
4. Open a second browser window, drag it onto the TV and go to:

   ```
   http://127.0.0.1:8765/tv/BGRVY
   ```

5. Press **F11** for fullscreen on the TV.

Done. Enter scores on the laptop, the scoreboard updates on the TV.

## Play with phones as well

1. Find the laptop's IP address:

   ```sh
   ip addr | grep 'inet 192'        # Linux
   ipconfig getifaddr en0           # macOS
   ipconfig                         # Windows
   ```

2. Phones open `http://<LAPTOP-IP>:8765/` and enter the code.

If a phone cannot reach the laptop, open the port:

```sh
sudo ufw allow 8765/tcp
```

## How the game works

- Tap a box in the table to enter a score. Only scores that are possible in
  that box are offered.
- The turn advances automatically, skipping anyone who has finished.
- Bonus of 50 points when the upper section reaches 63.
- Swedish Yatzy: 15 boxes, including one pair, two pairs, three of a kind,
  four of a kind, small straight, large straight, full house, chance and yatzy.

Scores are saved to `yatzy-data.json`, so an interrupted game is still there
next time you start the app.

---

# Setup

## Requirements

- Python 3.8 or newer. Nothing else: no pip packages, no build step.
- A browser.

## Running locally

This is the setup to start with. Everything stays on your own network.

```sh
cd yatzy
./start-yatzy.sh
```

On Windows:

```sh
python3 server.py
```

The app serves on port 8765 and opens a browser window. Leave the terminal open
while you play; close it to stop.

### Options

```sh
python3 server.py --port 8080        # different port
python3 server.py --host 127.0.0.1   # this computer only, no phones
python3 server.py --no-browser       # do not open a browser on start
```

By default it binds `0.0.0.0`, so other devices on your network can reach it.
Pass `--host 127.0.0.1` if you only ever play on the one laptop.

### Pages

| Path | What it is |
| :-- | :-- |
| `/` | Start or join a game, enter scores |
| `/spel/<CODE>` | Rejoin a game directly |
| `/tv/<CODE>` | The TV scoreboard |

### Showing it on the TV

**HDMI (recommended).** Connect the laptop, extend the display, drag a browser
window to the TV, open `/tv/<CODE>` and press F11.

**Chromecast.** Cast the browser tab showing `/tv/<CODE>`.

**The TV's own browser.** Open `http://<LAPTOP-IP>:8765/tv/<CODE>`. The TV page
is written in deliberately plain HTML and CSS so older smart TVs have a chance,
but older Samsung and LG browsers are unreliable. If it renders badly, use HDMI
or a Chromecast instead.

### Files

| File | Purpose |
| :-- | :-- |
| `server.py` | The server and all game logic |
| `index.html` | Score entry, phone and laptop |
| `tv.html` | TV scoreboard |
| `manifest.webmanifest`, `icon.svg` | Makes it installable as an app |
| `start-yatzy.sh` | Launcher |
| `yatzy-data.json` | Saved games, created on first run |

### Resetting

To wipe every saved game:

```sh
rm yatzy-data.json
```

---

## Running online on a VPS

Only worth doing if the family uses it enough that "the laptop has to be on"
becomes annoying, or if relatives in another house want to join the same game.

<!-- Read the security section at the end before exposing this to the internet. -->

### 1. DNS

Point an A record at the VPS before anything else, or certificates will fail:

```
yatzy.yourdomain.com  →  <VPS_IP>
```

Check it:

```sh
dig +short yatzy.yourdomain.com
```

### 2. Install Caddy and Python

```sh
ssh root@<VPS_IP>

apt update
apt install -y python3 debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
  | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
  | tee /etc/apt/sources.list.d/caddy-stable.list
apt update && apt install -y caddy
```

### 3. Copy the app over

From your laptop:

```sh
scp -r yatzy/ root@<VPS_IP>:/opt/
```

On the VPS, run it as its own unprivileged user:

```sh
useradd -r -s /usr/sbin/nologin yatzy
mkdir -p /var/lib/yatzy
chown -R yatzy:yatzy /opt/yatzy /var/lib/yatzy
```

### 4. Run it as a service

```sh
cp /opt/yatzy/yatzy.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now yatzy
systemctl status yatzy --no-pager
```

Confirm it answers on loopback:

```sh
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8765/
```

Expect `200`.

### 5. HTTPS

HTTPS is required for installing as an app on Android, and most smart TV
browsers refuse plain HTTP.

```sh
sed -i 's/yatzy.example.com/yatzy.yourdomain.com/' /opt/yatzy/Caddyfile
cp /opt/yatzy/Caddyfile /etc/caddy/Caddyfile
systemctl reload caddy
ufw allow 80,443/tcp
```

Check:

```sh
curl -sI https://yatzy.yourdomain.com | head -1
```

Expect `HTTP/2 200`. Certificates renew by themselves.

### 6. Use it

- Phone: `https://yatzy.yourdomain.com/`
- TV: `https://yatzy.yourdomain.com/tv/<CODE>`
- Install on Android: open in Chrome, then menu → *Add to Home screen*

### Maintenance

```sh
systemctl restart yatzy             # restart
journalctl -u yatzy -f              # follow the logs
```

Update after editing files locally:

```sh
scp -r yatzy/ root@<VPS_IP>:/opt/ && ssh root@<VPS_IP> systemctl restart yatzy
```

### Security, if you put this online

None of this matters on your home network. It matters the moment the app has a
public address.

**Use a VPS that does nothing else.** Not one that runs anything you care
about, and not one sharing SSH keys with other infrastructure. The worst case
should be "Yatzy is down, rebuild it".

Known weaknesses of this app as written:

- **No connection limit.** Each pending TV update holds a thread for up to 25
  seconds. Thousands of simultaneous connections will exhaust memory and can
  take the machine down.
- **The app directory is served as-is.** `yatzy-data.json` and `server.py` are
  readable over HTTP. Do not keep anything else in that folder.
- **No rate limit on creating games.** Each saved score rewrites the whole data
  file, so many junk games make every write slower.
- **Anyone with a game code can change that game.** That is the design: the
  code is the only thing standing in for a password.

Caddy covers the first and third with a small amount of config:

```
yatzy.yourdomain.com {
	encode gzip
	request_body { max_size 10KB }
	rate_limit {
		zone yatzy { key {remote_host} events 60 window 1m }
	}
	reverse_proxy 127.0.0.1:8765
}
```

For the second, move the data file outside the served directory by editing
`DATA_FILE` in `server.py`:

```python
DATA_FILE = Path("/var/lib/yatzy/yatzy-data.json")
```

Python's built-in HTTP server is not production software, and its own
documentation says so. Keeping Caddy in front of it, on a machine with nothing
else to lose, is what makes this acceptable for a family score sheet.
