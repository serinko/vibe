# Yatzy tillsammans – Windows

Svenska nedan. English further down.

---

# Svenska

## Det här behöver du

- En Windows-dator
- Python 3 (se *Installera Python* längre ner om du inte har det)
- En HDMI- eller USB-C-kabel till TV:n

## Starta spelet

1. Koppla datorn till TV:n med kabeln.
2. Högerklicka på skrivbordet → **Bildskärmsinställningar** → välj
   **Utöka dessa bildskärmar**. Alltså inte *Dubblera*: ni vill ha två olika
   bilder, inte samma sak på båda.
3. **Dubbelklicka på `Starta Yatzy.bat`**

Nu händer det här av sig självt:

- Ett litet minimerat fönster som heter **Yatzy-server** startar. Låt det vara.
- Webbläsaren öppnas med sidan där ni skriver in namnen.

4. Skriv in namnen, ett per rad, och tryck **Starta spelet**.
5. **Ett andra webbläsarfönster öppnas automatiskt** – det är TV-vyn.
   Dra det fönstret till TV:n och tryck **F11** för helskärm.

Klart. Skriv in poängen i det första fönstret, ställningen syns på TV:n.

## Under spelets gång

- Tryck på en ruta för att skriva in poäng. Bara möjliga poäng visas.
- Turen går vidare av sig själv.
- **Skrev du fel?** Tryck på rutan igen. Du ser vad som står där nu, kan välja
  ett annat tal, eller trycka **Rensa rutan**. Att rätta en siffra flyttar inte
  turen.
- Uppe till höger på TV-vyn finns en knapp för **1 kolumn** eller
  **2 kolumner**. Välj det som ser bäst ut på er TV. Datorn kommer ihåg valet.

## När spelet är slut

TV:n visar konfetti i tio sekunder, vinnaren och hela resultatlistan.
Tryck **Spela igen** på datorn för att köra en ny omgång med samma spelare i
samma ordning. TV:n hänger med automatiskt, ni behöver inte röra den.

## Avsluta

Stäng det minimerade fönstret **Yatzy-server**.

Blev det kvar i bakgrunden? Dubbelklicka på **`Stoppa Yatzy.bat`**.

## Spela med telefoner också

Telefonerna måste vara på samma wifi som datorn.

1. Öppna **Kommandotolken** (sök på `cmd` i Start-menyn) och skriv:

   ```
   ipconfig
   ```

   Leta efter **IPv4-adress**, till exempel `192.168.1.42`.

2. Telefonerna öppnar `http://192.168.1.42:8765/` i webbläsaren och skriver in
   koden som står uppe på TV:n.

Om telefonen inte kommer fram blockerar Windows-brandväggen porten. Första
gången servern startar frågar Windows om den får släppa igenom Python – svara
**Tillåt åtkomst** på privata nätverk.

## Installera Python

Om `Starta Yatzy.bat` säger att Python inte hittades:

1. Gå till <https://www.python.org/downloads/>
2. Ladda ner och kör installationen.
3. **Viktigt:** kryssa i **Add Python to PATH** längst ner i det första
   fönstret innan du trycker Install. Utan den kryssrutan hittar inte
   startfilen Python.
4. Starta om datorn och dubbelklicka på `Starta Yatzy.bat` igen.

## Om något inte fungerar

| Problem | Vad du gör |
| :-- | :-- |
| Fönstret blinkar till och försvinner | Python saknas. Se *Installera Python*. |
| Webbläsaren visar en tom sida | Vänta några sekunder och ladda om. Servern kan behöva lite tid. |
| TV-fönstret öppnades inte | Webbläsaren blockerade det. Tryck **Öppna TV-vy här** i appen istället. |
| Texten är för liten på TV:n | Tryck **F11** för helskärm, och testa knappen **1 kolumn** / **2 kolumner**. |
| Telefonen når inte datorn | Kontrollera att båda är på samma wifi, och svara *Tillåt åtkomst* på brandväggsfrågan. |
| Porten 8765 används redan | Dubbelklicka `Stoppa Yatzy.bat` och starta om. |

---

# English

## What you need

- A Windows computer
- Python 3 (see *Installing Python* below if you do not have it)
- An HDMI or USB-C cable to the TV

## Starting the game

1. Connect the computer to the TV with the cable.
2. Right-click the desktop → **Display settings** → choose
   **Extend these displays**. Not *Duplicate*: you want two different pictures,
   not the same thing on both.
3. **Double-click `Starta Yatzy.bat`**

This happens by itself:

- A small minimised window called **Yatzy-server** starts. Leave it alone.
- The browser opens on the page where you enter the names.

4. Type in the names, one per line, and press **Starta spelet** (start the game).
5. **A second browser window opens automatically** – that is the TV view.
   Drag that window onto the TV and press **F11** for fullscreen.

Done. Enter scores in the first window, the scoreboard shows on the TV.

## While playing

- Tap a box to enter a score. Only possible scores are offered.
- The turn advances by itself.
- **Entered the wrong number?** Tap the box again. You see what is in there
  now, can pick a different number, or press **Rensa rutan** (clear the box).
  Correcting a number does not move the turn on.
- Top right of the TV view there is a button for **1 kolumn** or
  **2 kolumner** (one or two columns). Pick whichever looks better on your TV.
  The choice is remembered.

## When the game ends

The TV shows ten seconds of confetti, the winner, and the full standings.
Press **Spela igen** (play again) on the computer to start another round with
the same players in the same order. The TV follows along automatically, you do
not need to touch it.

## Stopping

Close the minimised **Yatzy-server** window.

Lost behind something? Double-click **`Stoppa Yatzy.bat`**.

## Playing with phones as well

The phones must be on the same wifi as the computer.

1. Open **Command Prompt** (search for `cmd` in the Start menu) and type:

   ```
   ipconfig
   ```

   Look for the **IPv4 Address**, for example `192.168.1.42`.

2. Phones open `http://192.168.1.42:8765/` in the browser and enter the code
   shown at the top of the TV view.

If a phone cannot get through, the Windows firewall is blocking the port. The
first time the server starts, Windows asks whether Python may accept
connections – answer **Allow access** on private networks.

## Installing Python

If `Starta Yatzy.bat` says Python was not found:

1. Go to <https://www.python.org/downloads/>
2. Download and run the installer.
3. **Important:** tick **Add Python to PATH** at the bottom of the first
   screen before pressing Install. Without it the launcher cannot find Python.
4. Restart the computer and double-click `Starta Yatzy.bat` again.

## If something does not work

| Problem | What to do |
| :-- | :-- |
| A window flashes and disappears | Python is missing. See *Installing Python*. |
| The browser shows a blank page | Wait a few seconds and reload. The server may need a moment. |
| The TV window did not open | The browser blocked it. Press **Öppna TV-vy här** in the app instead. |
| Text is too small on the TV | Press **F11** for fullscreen, and try the **1 kolumn** / **2 kolumner** button. |
| The phone cannot reach the computer | Check both are on the same wifi, and answer *Allow access* to the firewall prompt. |
| Port 8765 is already in use | Double-click `Stoppa Yatzy.bat` and start again. |

---

## Files in this folder

| File | What it is |
| :-- | :-- |
| `Starta Yatzy.bat` | Double-click this to start |
| `Stoppa Yatzy.bat` | Stops a server window left running |
| `server.py` | The server and the game rules |
| `index.html` | The page where you enter scores |
| `tv.html` | The TV scoreboard |
| `yatzy-data.json` | Saved games, created on first run |

To wipe every saved game, delete `yatzy-data.json`.
