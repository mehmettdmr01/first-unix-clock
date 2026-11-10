"""Ports the two Python 2 helpers of unix-jun72 (tools/fixaout.py, tools/mktape.py) to Python 3.
Usage: python3 py3yap.py <jun72>/tools   (expects fixaout.py.orig and mktape.py.orig next to them)
Only the code is touched; the permission table in mktape.py (the first triple-quoted block) stays as it is."""
import re, sys
from pathlib import Path
T = Path(sys.argv[1])

def octal(code):
    return re.sub(r"(?<![\w.])0([0-7]+)\b", r"0o\1", code)

f = (T / "fixaout.py.orig").read_text()
f = f.replace("#!/usr/bin/env python", "#!/usr/bin/env python3", 1)
f = f.replace("len(bs) / 2", "len(bs) // 2").replace("file(fn, ", "open(fn, ")
f = f.replace("[0405,", "[0o405,")
(T / "fixaout.py").write_text(f)

m = (T / "mktape.py.orig").read_text()
parts = m.split('"""')            # 0: shebang, 1: docstring, 2: kod, 3: tablo, 4: kod
assert len(parts) == 5, len(parts)
head, code = parts[2], parts[4]
code = octal(code)
code = re.sub(r'print "([^"]*)" % (.+)', r'print("\1" % \2)', code)
code = re.sub(r'print "([^"]*)"', r'print("\1")', code)
code = code.replace("print sMode(mode), uid, fn", "print(sMode(mode), uid, fn)")
code = code.replace('return d + ("\\0" * m)', 'return d + (b"\\0" * m)')
code = code.replace('pack("<HBB", len(d), mode, uid) + fn', 'pack("<HBB", len(d), mode, uid) + fn.encode("latin-1")')
code = code.replace('wrFile(out, "", "", 0, 0)', 'wrFile(out, "", b"", 0, 0)')
code = code.replace("file(fn, 'rb')", "open(fn, 'rb')").replace('file("tape", "wb")', 'open("tape", "wb")')
code = code.replace('f.write("\\0" * (512 * 65))', 'f.write(b"\\0" * (512 * 65))')
code = code.replace("ps = filter(None, ps.split(\"\\n\"))", "ps = [p for p in ps.split(\"\\n\") if p]")
parts[0] = parts[0].replace("#!/usr/bin/env python", "#!/usr/bin/env python3", 1)
parts[4] = code
(T / "mktape.py").write_text('"""'.join(parts))
print("tamam")
