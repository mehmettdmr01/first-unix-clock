# The recorded run on the 4th Edition (1973, the University of Utah tape): install from the clean tape, boot, date,
# a C program that prints the raw counter, a C program that sets the clock 10 s before 27 Nov 1999 15:59:59 EDT
# (where ctime's 16-bit division overflows), and date set to 31 Dec 1999 23:59.
CWD = "/root/unix/v4"
CMD = "/root/unix/simh/BIN/pdp11 install.ini"
TITLE = "UNIX Fourth Edition (University of Utah tape) on Open SIMH"
TIMEOUT = 120
K = 0.12
def prog(name, lines):
    s = [("yaz", f"ed {name}.c\r", K), ("uyu", 1), ("yaz", "a\r", K)]
    s += [("yaz", l + "\r", K) for l in lines]
    s += [("yaz", ".\r", K), ("yaz", "w\r", K), ("uyu", 1), ("yaz", "q\r", K), ("uyu", 1),
          ("yaz", f"cc {name}.c\r", K), ("uyu", 8), ("yaz", f"mv a.out {name}\r", K), ("uyu", 1)]
    return s
STEPS = [
    ("not", "kurulum"), ("bekle", r"\n="), ("yaz", "mcopy\r", K), ("bekle", r"for rk"), ("uyu", 0.5), ("yaz", "k", K),
    ("bekle", r"disk offset"), ("yaz", "0\r", K), ("bekle", r"tape offset"), ("yaz", "75\r", K),
    ("bekle", r"count"), ("yaz", "4000\r", K), ("bekle", r"\n="), ("yaz", "uboot\r", K), ("uyu", 2),
    ("not", "acilis"), ("yaz", "k", K), ("uyu", 1), ("yaz", "unix\r", K),
    ("bekle", r"login:"), ("uyu", 1.5), ("yaz", "root\r", K), ("uyu", 2),
    ("not", "uyanis-saati"), ("yaz", "date\r", K), ("uyu", 2.5),
    ("yaz", "ls -l /\r", K), ("uyu", 3),
    ("not", "ham-sayac-programi"),
] + prog("r", ["main() {", "\tint t[2];", "\ttime(t);", "\tprintf(\"%d %d\\n\", t[0], t[1]);", "}"]) + [
    ("yaz", "r\r", K), ("uyu", 2),
    ("not", "1999-programi"),
] + prog("s", ["main() {", "\tint t[2];", "\tt[0] = 14400;", "\tt[1] = 14390;", "\tstime(t);", "}"]) + [
    ("not", "1999-kur"), ("yaz", "s\r", K), ("uyu", 0.3), ("yaz", "date\r", K), ("uyu", 0.8), ("yaz", "r\r", K), ("uyu", 1),
    ("yaz", "date\r", K), ("uyu", 1.2), ("yaz", "date\r", K), ("uyu", 1.2), ("yaz", "date\r", K), ("uyu", 0.6),
    ("not", "1999-sinir"), ("yaz", "date\r", K), ("uyu", 0.6), ("yaz", "date\r", K), ("uyu", 1), ("yaz", "r\r", K), ("uyu", 1.5),
    ("yaz", "date\r", K), ("uyu", 3),
    ("not", "date-1999-denemesi"), ("yaz", "date 1231235999\r", K), ("uyu", 2.5), ("yaz", "r\r", K), ("uyu", 2.5),
    ("yaz", "date\r", K), ("uyu", 3),
    ("not", "kapanis"), ("yaz", "sync\r", K), ("uyu", 2), ("ham", "\x05"), ("bekle", r"sim>"), ("uyu", 1), ("yaz", "q\r", K), ("uyu", 1),
]
