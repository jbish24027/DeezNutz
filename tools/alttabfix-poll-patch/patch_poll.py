"""Alt-Tab Stuck Key Fix (AltTabFix.dll 1.3.1) - remove the off-thread keyboard Poll.

ResetInput() runs on the window-message thread (WM_ACTIVATEAPP / WM_ENABLE /
WM_SHOWWINDOW) and calls BSInputDevice::Poll(0) on the keyboard device, i.e. the
same BSWin32KeyboardDevice::Process the engine runs on its input job thread.
Both walk one shared 10-entry DirectInput buffer with no lock; the race ends in
SkyrimSE.exe+0CDE0A2 (curState[dwOfs], dwOfs garbage).  Crash logs 2026-08-26
and 2026-09-08.  Everything else the mod does (state clear, message flush, event
queue clear, frame sinkhole, Main::Update Alt+Tab-guard NOP) is kept.

Site: RVA 0x240F7  `call qword ptr [rax+0x10]`  = FF 50 10  ->  90 90 90
Usage:  python patch_poll.py            apply (keeps AltTabFix.dll.bak-<date>)
        python patch_poll.py --check    report patched / unpatched / unknown
Re-run --check after any update of the mod; a new DLL needs the site re-found.
"""
import sys, os, shutil, datetime, pefile
DLL = r"C:\1. AUTHORIA\mods\Alt-Tab Stuck Key Fix\SKSE\Plugins\AltTabFix.dll"
RVA = 0x240F7
ORIG = bytes.fromhex("ff5010")
PATCH = b"\x90\x90\x90"
# context that must surround the site, so a different build fails loudly
BEFORE = bytes.fromhex("488b030f57c9488bcb")   # mov rax,[rbx]; xorps xmm1,xmm1; mov rcx,rbx  (9 bytes)
AFTER  = bytes.fromhex("660f1f440000")         # nop word ptr [rax+rax]  (6 bytes)
def main():
    pe = pefile.PE(DLL, fast_load=True)
    off = pe.get_offset_from_rva(RVA); pe.close()   # release the mapping before rewriting the file
    data = bytearray(open(DLL, "rb").read())
    site = bytes(data[off:off+3]); ctx_ok = bytes(data[off-9:off]) == BEFORE and bytes(data[off+3:off+9]) == AFTER
    state = "patched" if site == PATCH else "unpatched" if site == ORIG else "unknown"
    print(f"AltTabFix.dll size {len(data)}  site RVA 0x{RVA:X} (file 0x{off:X}) = {site.hex()}  context {'ok' if ctx_ok else 'MISMATCH'}  -> {state}")
    if "--check" in sys.argv:
        sys.exit(0 if state == "patched" and ctx_ok else 1)
    if not ctx_ok or state == "unknown":
        print("refusing to patch: unexpected bytes (new build?)"); sys.exit(2)
    if state == "patched":
        print("already patched"); return
    bak = DLL + ".bak-" + datetime.date.today().strftime("%Y%m%d")
    if not os.path.exists(bak): shutil.copy2(DLL, bak); print("backup:", bak)
    data[off:off+3] = PATCH
    open(DLL, "wb").write(data)
    print("patched. verify:"); sys.argv.append("--check"); main()
if __name__ == "__main__": main()
