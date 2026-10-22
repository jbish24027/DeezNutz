"""Generate the Devotion choices file: every option whose files are present in the installed folder."""
import os, io, sys
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\mod-install-helpers')
import fomod_tool as F

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ARCH = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\d28e33fc-d149-4807-b06a-e5dc283cde4d\scratchpad\ex\devotion_new'
INST = r'C:\1. AUTHORIA\mods\Devotion'
OUT = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\d28e33fc-d149-4807-b06a-e5dc283cde4d\scratchpad\choices_devotion.txt'

res = F.parse(ARCH)
idx = F.installed_index(INST)

chosen = []
skipped = []
for label, fmap in F.all_options(res):
    if label == 'REQUIRED' or label.startswith('COND'):
        continue
    real = [d for d, v in fmap.items() if v[0] is not None]
    if not real:
        # zero-file option (a "skip"/informational entry) - not needed
        continue
    present = [d for d in real if d in idx]
    if present and len(present) == len(real):
        chosen.append(label)
    elif present:
        chosen.append(label)
        print('!! PARTIAL (%d/%d present) - included: %s' % (len(present), len(real), label))
    else:
        skipped.append(label)

with open(OUT, 'w', encoding='ascii', newline='\n') as f:
    for c in chosen:
        f.write(c + '\n')

print('chosen : %d' % len(chosen))
print('skipped: %d' % len(skipped))
print('written -> %s' % OUT)
print()
print('=== skipped (quest mods not in the load order) ===')
for s in skipped:
    print('   ', s)
