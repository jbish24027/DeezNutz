"""Extract every texture the body pieces use, thumbnail it, and build per-mod contact sheets."""

import sys, os, json, pickle, subprocess, collections, shutil
sys.path.insert(0, r'C:\1. AUTHORIA\_tools\orf')
import mo2_vfs, bsa
from PIL import Image, ImageDraw

SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\a51f92a9-dc4d-4048-b276-0ba2edcd4eb4\scratchpad\orf'
WORK = os.path.join(SP, 'texwork')
THUMB = os.path.join(SP, 'thumbs')
SHEETS = os.path.join(SP, 'sheets')
TEXCONV = r'C:\1. AUTHORIA\tools\xEdit\Edit Scripts\Texconv.exe'

v = mo2_vfs.Vfs()
v._index = pickle.load(open(os.path.join(SP, 'vfsindex.pkl'), 'rb'))
bi = bsa.BsaIndex()
bi.map = pickle.load(open(os.path.join(SP, 'bsaindex.pkl'), 'rb'))


def slug(t):
    """Stable, collision-free stem for a texture path, no extension.

    texconv names its output after the input stem, so the .dds we write and the
    .PNG we look up must share exactly this stem. Getting that wrong silently
    renders every cell as the 'missing' placeholder instead of the texture.
    """
    import hashlib
    base = t.replace('\\', '_').replace('/', '_').replace(':', '_')
    if base.lower().endswith('.dds'):
        base = base[:-4]
    return base[-90:] + '_' + hashlib.md5(t.lower().encode('utf-8')).hexdigest()[:8]


def thumb_path(t):
    return os.path.join(THUMB, slug(t) + '.PNG')


def work_path(t):
    return os.path.join(WORK, slug(t) + '.dds')


def extract_all():
    os.makedirs(WORK, exist_ok=True)
    inv = pickle.load(open(os.path.join(SP, 'texinv.pkl'), 'rb'))
    got, miss = {}, []
    for t in inv:
        dst = work_path(t)
        if os.path.exists(dst):
            got[t] = dst
            continue
        mod, ab = v.resolve(t)
        data = None
        if ab:
            try:
                data = open(ab, 'rb').read()
            except OSError:
                data = None
        if data is None:
            data, mod = bi.read(t)
        if not data:
            miss.append(t)
            continue
        with open(dst, 'wb') as fh:
            fh.write(data)
        got[t] = dst
    print('textures extracted: %d   missing: %d' % (len(got), len(miss)))
    for m in miss[:8]:
        print('   MISSING', m)
    return got, miss


def convert(got):
    os.makedirs(THUMB, exist_ok=True)
    todo = [p for t, p in got.items() if not os.path.exists(thumb_path(t))]
    print('converting %d textures' % len(todo))
    B = 60
    for i in range(0, len(todo), B):
        batch = todo[i:i + B]
        cmd = [TEXCONV, '-ft', 'png', '-w', '384', '-h', '384', '-y', '-o', THUMB] + batch
        subprocess.run(cmd, capture_output=True)
    n = len([f for f in os.listdir(THUMB) if f.lower().endswith('.png')])
    print('thumbnails present: %d' % n)


def sheets_for_mod(plug, entries, out_dir, per_sheet=12):
    """entries: [(texture, n_items, [sample names])]"""
    os.makedirs(out_dir, exist_ok=True)
    made = []
    C, PAD, COLS = 300, 34, 4
    for si in range(0, len(entries), per_sheet):
        chunk = entries[si:si + per_sheet]
        rows = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new('RGB', (COLS * C, rows * (C + PAD)), (22, 22, 24))
        d = ImageDraw.Draw(sheet)
        for i, (tex, cnt, names) in enumerate(chunk):
            png = thumb_path(tex)
            x, y = (i % COLS) * C, (i // COLS) * (C + PAD)
            if os.path.exists(png):
                try:
                    im = Image.open(png).convert('RGB').resize((C, C))
                    sheet.paste(im, (x, y + PAD))
                except Exception:
                    d.rectangle([x, y + PAD, x + C, y + C + PAD], fill=(60, 20, 20))
            else:
                d.rectangle([x, y + PAD, x + C, y + C + PAD], fill=(60, 20, 20))
            d.text((x + 4, y + 3), '%d) %s' % (si + i + 1, (names[0] if names else '?')[:44]),
                   fill=(240, 240, 240))
            d.text((x + 4, y + 17), '   %d items' % cnt, fill=(150, 190, 150))
        p = os.path.join(out_dir, '%s_%02d.png' % (slug(plug).replace('.esp', '').replace('.esm', ''), si // per_sheet))
        sheet.save(p)
        made.append(p)
    return made


def main():
    got, miss = extract_all()
    convert(got)
    tex_map = json.load(open(os.path.join(SP, 'tex_map.json')))
    os.makedirs(SHEETS, exist_ok=True)
    plan = {}
    for plug, items in tex_map.items():
        by = collections.defaultdict(list)
        for e, dd in items.items():
            if dd['tex']:
                by[dd['tex']].append(dd['n'])
        if not by:
            continue
        entries = sorted(((t, len(ns), sorted(set(ns))) for t, ns in by.items()),
                         key=lambda x: -x[1])
        plan[plug] = [{'tex': t, 'count': c, 'names': n[:6]} for t, c, n in entries]
    json.dump(plan, open(os.path.join(SP, 'sheet_plan.json'), 'w'), indent=1)
    tot = sum(len(v_) for v_ in plan.values())
    print('mods with sheets to build: %d   texture cells total: %d' % (len(plan), tot))


if __name__ == '__main__':
    main()
