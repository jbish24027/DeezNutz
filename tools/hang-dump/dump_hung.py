"""Write a small minidump (thread contexts + stacks + module list) of a running process.
Made for a hung SkyrimSE.exe: run it BEFORE the game is killed, then read the dump with read_dump.py.
Usage: python dump_hung.py [process-name-or-pid] [out.dmp]     (default: SkyrimSE.exe -> hang-<time>.dmp)
Full-memory dumps are not taken (the game holds ~40 GB private); this one is a few MB.
"""
import sys, os, ctypes, ctypes.wintypes as W, datetime, subprocess
name = sys.argv[1] if len(sys.argv) > 1 else "SkyrimSE.exe"
out  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "hang-%s.dmp" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
if name.isdigit(): pid = int(name)
else:
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq " + name, "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout.strip().splitlines()
    rows = [l for l in r if l.startswith('"')]
    if not rows: print("no process named", name); sys.exit(1)
    pid = int(rows[0].split('","')[1])
k32 = ctypes.windll.kernel32; dbg = ctypes.windll.dbghelp
PROCESS_QUERY_INFORMATION, PROCESS_VM_READ = 0x400, 0x10
h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
if not h: print("OpenProcess failed", ctypes.get_last_error(), k32.GetLastError()); sys.exit(1)
GENERIC_WRITE, CREATE_ALWAYS = 0x40000000, 2
f = k32.CreateFileW(out, GENERIC_WRITE, 0, None, CREATE_ALWAYS, 0x80, None)
MiniDumpNormal, WithThreadInfo, WithUnloadedModules, WithIndirect, WithHandleData = 0x0, 0x1000, 0x20, 0x40, 0x4
dbg.MiniDumpWriteDump.restype = W.BOOL
ok = dbg.MiniDumpWriteDump(h, pid, f, MiniDumpNormal | WithThreadInfo | WithUnloadedModules | WithIndirect | WithHandleData, None, None, None)
err = k32.GetLastError(); k32.CloseHandle(f); k32.CloseHandle(h)
print(("wrote %s (%d bytes) for pid %d" % (out, os.path.getsize(out), pid)) if ok else ("MiniDumpWriteDump failed, error 0x%08X" % (err & 0xFFFFFFFF)))
sys.exit(0 if ok else 2)
