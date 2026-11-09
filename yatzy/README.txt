YATZY TILLSAMMANS
=================

Håll koll på poängen när familjen spelar Yatzy. Telefonen skriver in poäng,
TV:n visar ställningen – båda tittar på samma spel.

Starta hemma
------------

Linux/macOS:
  ./start-yatzy.sh

Windows:
  python3 server.py

Appen öppnas i webbläsaren. Låt fönstret vara öppet medan ni spelar.

Telefon och TV
--------------

1. Starta ett nytt spel på datorn eller telefonen. Du får en kod, t.ex. ABCDE.
2. På TV:n: öppna http://<datorns-ip>:8765/tv/ABCDE
   Datorns IP hittar du med `ip addr` (Linux) eller `ipconfig` (Windows).
3. Andra telefoner går med genom att skriva in koden.

Alla ser samma spel direkt. Poängen sparas i yatzy-data.json, så ett omstartat
spel finns kvar.

Äldre TV
--------

Äldre smart-TV:ars webbläsare är opålitliga. Fungerar inte TV-vyn direkt:
anslut en dator med HDMI, eller använd en Chromecast och casta fliken.

På en VPS
---------

  1. Kopiera mappen till /opt/yatzy
  2. Redigera Caddyfile: byt yatzy.example.com mot din domän
  3. sudo cp yatzy.service /etc/systemd/system/
     sudo systemctl enable --now yatzy
  4. sudo caddy run --config Caddyfile

Då når ni spelet var ni än är, och TV:n öppnar bara https://din-domän/tv/ABCDE

Regler
------

Svensk Yatzy: 15 rutor, bonus 50 poäng när översta delen når 63.
