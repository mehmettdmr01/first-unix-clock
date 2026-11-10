# The first Unix clocks, run again

Video: (link coming)

The first Unix (1971) kept time in sixtieths of a second since 1 January 1971, in 32 bits. Its own manual says so, and adds: "The chronological-minded user will note that 2\*\*32 sixtieths of a second is only about 2.5 years." The date routine's manual page says: "Jan 1 comes out Dec 32."

I ran a restored 1st Edition and the 1973 4th Edition (the tape found at the University of Utah in 2025) in a PDP-11 emulator on an ordinary $6 DigitalOcean server, set their clocks to the edges and recorded what the screen said. Everything here is the real script and the real output.

## Setup
- DigitalOcean s-1vcpu-1gb (ams3), Ubuntu 24.04.5 LTS. Run on 10 November 2026. Exact versions: `recordings/surumler.txt`.
- **1st Edition (1971–72):**
  - the [unix-jun72](https://github.com/DoctorWkt/unix-jun72) restoration (Warren Toomey and others, 2008), through the [c3x04 fork](https://github.com/c3x04/Unix-1st-Edition-jun72);
  - classic SIMH 3.12-5, PDP-11/20;
  - its user programs date from between the 1st and 2nd Editions.
- **4th Edition (1973):**
  - the University of Utah tape, files from [squoze.net/UNIX/v4](http://squoze.net/UNIX/v4/), tape sha256 `ec0a5437…`;
  - Open SIMH 4.1, PDP-11/45.

## Results

| What I did | What the screen said |
|---|---|
| 1st Edition: boot, `date` | `Fri Jan  1 00:00:05` (no year; the counter starts at zero) |
| `date 12312359` (31 Dec 23:59), wait | `Sun Dec 31 23:59:58` → **`Mon Dec 32 00:00:00`** |
| A four-line program in 1971's own assembler sets the counter to 2^32 − 512 sixtieths (8.5 s before the end) | **`Sun Dec <9 12:06:20`** … `12:06:28` |
| The counter runs out | **`Fri Jan  1 00:00:00`** |
| 4th Edition: install from the tape, boot, `date` | **`Wed Jun 12 19:50:49 EDT 1974`** (the time last saved on the disk) |
| A C program (1973 compiler) sets the clock to 943,732,790 (27 Nov 1999 15:59:50 EDT) | `Sat Nov 27 15:59:52 EDT 1999` … `15:59:59` |
| 10 s later | **`Tue Feb 22 00:00:00 EDT 1983`**; the raw counter keeps counting: `14400 14403` |
| `date 1231235999` (31 Dec 1999 23:59) | **`Wed Mar  9 04:47:00 EDT 1983`**; raw counter `14445 31623` = 946,699,143 s = 31 Dec 1999 23:59 EDT |

**Why the 1st Edition clock ends:**
- 2^32 / 60 s = 828 days 12:06:28.
- Counted from 1 January 1971 (the 1971 manual's base), that is 8 April 1973 at 12:06:28. The screen wraps at exactly that time of day.
- `Dec <9`: the day of the month no longer fits in two digits. The tens digit came out as 12, printed as the ASCII character after `9`, `:`, `;`, which is `<`.

**Why the 4th Edition calendar ends in 1999:**
- `gmtime` in the tape's `usr/source/s3/ctime.c` first divides the time by 8 hours: `d0 = ldiv(tim[0], tim[1], 28800);`. The result is an `int`, 16 bits on the PDP-11, so at most 32,767.
- 32,768 × 28,800 s is 27 November 1999, 16:00 in the routine's local time. After that the division overflows.
- The counter itself (two 16-bit words, seconds since 1970) goes on until 2038.
- Landing in 1983 is this emulator's doing: on overflow the quotient register keeps the counter's high word (14400 / 3 = 4800 days → 22 Feb 1983; 14445 / 3 = 4815 days → 9 Mar 1983). A real PDP-11 may show a different wrong date.
- The same file has `int nixonflg 1; /* Daylight time all year around */`. From day 5 of 1974 (6 January), 2 a.m., it applies daylight time for good, which matches the US emergency daylight saving time law. That is why every later date prints as EDT.
- The 7th Edition (1979) rewrote this code with 32-bit `long` arithmetic.

## Files
Names are Turkish, as shown in the video:
- `setup.sh`: installs both systems (copy all files to `/root/unix` on a throwaway server and run it there).
- `py3yap.py` ("make py3"): ports unix-jun72's two Python 2 helper scripts to Python 3.
- `surucu.py` ("driver"): types into the emulator console and records the session as an asciinema v2 `.cast`.
- `kaydet.sh` ("record"): runs a session on a virtual screen and records it to `.cast` and `.mp4`.
- `final_v1.py`, `final_v4.py`: the recorded steps for each system.
- `recordings/v1.cast`, `recordings/v4.cast`: the full sessions, every character with its time (`asciinema play recordings/v1.cast`).
- `frames/`: two frames from the screen recordings.

The step names in the scripts are Turkish:
- `bekle` = wait for
- `yaz` = type
- `ham` = send raw
- `uyu` = sleep
- `not` = marker

## Run it yourself
Only on a throwaway machine:
```
bash setup.sh
bash kaydet.sh v1
bash kaydet.sh v4
```

## Limits
- Everything ran in an emulator, not on a real PDP-11.
- The 1st Edition is a restoration.
- The 2nd and 3rd Editions (base 1 January 1972: "This guarantees a crisis every 2.26 years") were not run; for them there is only the manual.
- The clocks were set forward; time did not really pass.

If you know another clock bug in 1970s Unix, open an issue.
