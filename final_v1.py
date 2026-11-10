# The recorded run on the 1st Edition (1971): login, date, 31 December 23:59 → "Dec 32", then a four-line program in
# 1971's own assembler sets the counter 512 ticks (8.5 s) before 2^32 sixtieths, and the clock wraps.
# The disk images are restored from the clean build before each run (kaydet.sh).
CWD = "/root/unix/jun72b"
CMD = "/root/unix/jun72b/tools/pdp11 simh.cfg"
TITLE = "UNIX First Edition (unix-jun72 restoration) on SIMH 3.12-5"
TIMEOUT = 120
K = 0.12   # seconds between typed letters
STEPS = [
    ("not", "acilis"), ("bekle", r"login:"), ("uyu", 1.5), ("yaz", "root\r", K), ("uyu", 2),
    ("not", "ilk-date"), ("yaz", "date\r", K), ("uyu", 2.5),
    ("yaz", "ls -l\r", K), ("uyu", 3),
    ("not", "dec32-kur"), ("yaz", "date 12312359\r", K), ("uyu", 2.5),
    ("yaz", "date\r", K), ("uyu", 14), ("yaz", "date\r", K), ("uyu", 14), ("yaz", "date\r", K), ("uyu", 10),
    ("yaz", "date\r", K), ("uyu", 3), ("yaz", "date\r", K), ("uyu", 1.2), ("yaz", "date\r", K), ("uyu", 1.2),
    ("not", "dec32"), ("yaz", "date\r", K), ("uyu", 1.2), ("yaz", "date\r", K), ("uyu", 1.2), ("yaz", "date\r", K), ("uyu", 2),
    ("yaz", "date\r", K), ("uyu", 3),
    ("not", "program"), ("yaz", "ed t.s\r", K), ("uyu", 1), ("yaz", "a\r", K),
    ("yaz", "mov $177777,*$177302\r", K), ("yaz", "mov $177000,*$177304\r", K),
    ("yaz", "sys stime\r", K), ("yaz", "sys exit\r", K), ("yaz", ".\r", K), ("yaz", "w\r", K), ("uyu", 1), ("yaz", "q\r", K), ("uyu", 1),
    ("yaz", "as t.s\r", K), ("uyu", 4),
    ("not", "tasma-kur"), ("yaz", "a.out\r", K), ("uyu", 0.3),
    ("yaz", "date\r", K), ("uyu", 1), ("yaz", "date\r", K), ("uyu", 1), ("yaz", "date\r", K), ("uyu", 1),
    ("yaz", "date\r", K), ("uyu", 0.6), ("not", "tasma"), ("yaz", "date\r", K), ("uyu", 0.6), ("yaz", "date\r", K), ("uyu", 0.6),
    ("yaz", "date\r", K), ("uyu", 1.5), ("yaz", "date\r", K), ("uyu", 3),
    ("not", "kapanis"), ("ham", "\x05"), ("bekle", r"sim>"), ("uyu", 1), ("yaz", "q\r", K), ("uyu", 1),
]
