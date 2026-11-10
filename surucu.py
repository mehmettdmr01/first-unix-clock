"""Drives the console of an old Unix and records the session with its timing (run only on the throwaway server).
The recording is asciinema v2 (.cast): each line is [seconds, "o", text on screen]; "i" lines are what was typed,
"m" lines are markers that split the session into parts.
Usage: python3 surucu.py <steps.py> <out.cast>
steps.py defines CWD (working directory), CMD (emulator command), STEPS (list), optionally TITLE, TIMEOUT.
Steps:
  ("bekle", r"login:")        wait until this pattern is on screen
  ("yaz", "root\r", 0.08)     type letter by letter (seconds between letters, default 0.08)
  ("ham", "\x05")             send at once (Ctrl-E stops the emulator)
  ("uyu", 12)                 wait this many seconds, keep recording
  ("not", "text")             drop a marker into the recording"""
import json, runpy, sys, time
import pexpect

cfg = runpy.run_path(sys.argv[1])
out = open(sys.argv[2], "w")
t0 = time.time()
out.write(json.dumps({"version": 2, "width": 80, "height": 24, "timestamp": int(t0), "title": cfg.get("TITLE", "")}) + "\n")


def event(kind, text):
    out.write(json.dumps([round(time.time() - t0, 3), kind, text]) + "\n")
    out.flush()


class Screen:
    def write(self, s):
        if s:
            event("o", s)
            sys.stdout.write(s)
            sys.stdout.flush()

    def flush(self):
        pass


p = pexpect.spawn(cfg["CMD"], cwd=cfg["CWD"], encoding="latin-1", timeout=cfg.get("TIMEOUT", 90), dimensions=(24, 80))
p.logfile_read = Screen()


def drain(seconds):
    end = time.time() + seconds
    while time.time() < end:
        try:
            p.expect(pexpect.TIMEOUT, timeout=min(0.2, max(0.01, end - time.time())))
        except pexpect.EOF:
            return


for step in cfg["STEPS"]:
    kind, arg = step[0], step[1]
    if kind == "bekle":
        p.expect(arg)
    elif kind == "yaz":
        gap = step[2] if len(step) > 2 else 0.08
        for ch in arg:
            event("i", ch)
            p.send(ch)
            drain(gap)
    elif kind == "ham":
        event("i", arg)
        p.send(arg)
    elif kind == "uyu":
        drain(arg)
    elif kind == "not":
        event("m", arg)
drain(1)
p.close(force=True)
print(f"\n[surucu] {time.time() - t0:.1f} sn kaydedildi -> {sys.argv[2]}")
