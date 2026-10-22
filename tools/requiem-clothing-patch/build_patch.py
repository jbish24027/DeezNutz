"""Build + verify the Requiem patch for Burlesque Dress (Magic Pariah needs none: its four
pieces are already Clothing / AR 0 / clothing keywords with no armor-set keyword).

Convention (memory 'authoria-armor-requiem-convention' = the load order's own Armor Folder
patch, cross-checked against Requiem's REQ_Cloth_* / REQ_Amulet_* pieces read live today):
  every piece -> BodyTemplate Clothing, ArmorRating 0, iron armor-set keyword stripped
  body (32)         value 20   weight 1.0   ArmorClothing + VendorItemClothing + ClothingBody
  hands (33/34)     value 10   weight 0.5   ... + ClothingHands
  feet (37)         value 10   weight 1.0   ... + ClothingFeet
  head (30/31/42)   value 10   weight 0.5   ... + ClothingHead
  other slots       value 10   weight 1.0   ArmorClothing + VendorItemClothing
  ClothingRich flavour keyword kept where the author set it
  necklace (35)     Requiem silver-garnet tier: 440 / 0.25 / ArmorJewelry + VendorItemJewelry
                    + JewelryExpensive + ClothingNecklace
  bracelet (60)     same tier, without ClothingNecklace
Recipes:
  19 tempering recipes -> WorkbenchKeyword REQ_DisableRecipe (Requiem's rule for clothing)
  15 clothing forge recipes -> keep inputs, add HasPerk(Craftsmanship) like every Requiem forge recipe
  4 jewelry forge recipes -> inputs = 1 silver ingot + 2 flawless garnets, add
                             HasPerk(Advanced Blacksmithing) - cloned from REQ_Forge_Amulet_SilverGarnet
Also fixes a mod bug: the red bracelet's armature list carried the vanilla GoldAmuletAA.
"""
import os, struct, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\requiem-clothing-patch")
from esp_tools import Plugin, parse_armo, parse_cobj, rewrite_subs, build_subrecords, write_patch, zstr

SRC = r"C:\1. AUTHORIA\mods\Burlesque Dress\Burlesque.esp"
OUT_DIR = r"C:\1. AUTHORIA\mods\Authoria - Magic Pariah and Burlesque - Requiem Clothing"
OUT_NAME = "Authoria - Burlesque Dress - Requiem Clothing.esp"
DESC = "Requiem clothing frames, disabled tempering, Requiem-gated recipes for Burlesque Dress (Nexus 171116). Authoria 2026-09-03."

# Skyrim.esm forms (master index 0 in the patch)
K = dict(ArmorClothing=0x06BBE8, ArmorJewelry=0x06BBE9, VendorItemClothing=0x08F95B, VendorItemJewelry=0x08F95A,
         ClothingBody=0x0A8657, ClothingHands=0x10CD13, ClothingFeet=0x10CD12, ClothingHead=0x10CD11,
         ClothingNecklace=0x10CD0A, JewelryExpensive=0x0A8664, ClothingRich=0x0A865D, ClothingPoor=0x0A865C)
PERK_CRAFTSMANSHIP = 0x0CB40D
PERK_ADV_BLACKSMITH = 0x05218E
INGOT_SILVER = 0x05ACE3
GEM_GARNET_FLAWLESS = 0x068521
REQ_DISABLE_RECIPE = 0xAD3B01          # Requiem.esp
CTDA_HASPERK = 448


def frame_for(a):
    s = set(a['slots'])
    flav = [K[n] for n in ('ClothingRich', 'ClothingPoor') if ('%06X:Skyrim.esm' % K[n]) in a['keywords']]
    cloth = [K['ArmorClothing'], K['VendorItemClothing']]
    jewel = [K['ArmorJewelry'], K['VendorItemJewelry'], K['JewelryExpensive']]
    if 32 in s:
        return 20, 1.0, cloth + [K['ClothingBody']] + flav, 'body'
    if 35 in s:
        return 440, 0.25, jewel + [K['ClothingNecklace']], 'necklace'
    if s & {33, 34}:
        return 10, 0.5, cloth + [K['ClothingHands']] + flav, 'hands'
    if 37 in s:
        return 10, 1.0, cloth + [K['ClothingFeet']] + flav, 'feet'
    if s & {30, 31, 42}:
        return 10, 0.5, cloth + [K['ClothingHead']] + flav, 'head'
    if 'Jewelry' in a['edid']:
        return 440, 0.25, jewel, 'bracelet'
    return 10, 1.0, cloth + flav, 'accessory'


def hasperk_ctda(template, perk_formid):
    """Clone an engine-written HasPerk CTDA and point it at another perk."""
    d = bytearray(template)
    assert struct.unpack_from('<H', d, 8)[0] == CTDA_HASPERK
    struct.pack_into('<I', d, 12, perk_formid)
    d[0] = 0                                   # EqualTo, no OR / no flags
    return bytes(d)


def main():
    pl = Plugin(SRC)
    masters = list(pl.masters) + [pl.name, 'Requiem.esp']
    src_idx = masters.index(pl.name); req_idx = masters.index('Requiem.esp')
    assert src_idx == len(pl.masters), 'source index must equal its own master count (no-remap rule)'
    # template HasPerk CTDA from one of the mod's own tempering recipes (second condition)
    tmpl = None
    for r in pl.of(b'COBJ'):
        if r.edid.startswith('TemperArmor'):
            ct = r.subs_all(b'CTDA')
            for d in ct:
                if struct.unpack_from('<H', d, 8)[0] == CTDA_HASPERK:
                    tmpl = bytes(d); break
            break
    assert tmpl is not None and struct.unpack_from('<I', tmpl, 12)[0] == PERK_ADV_BLACKSMITH

    recs = []; log = []
    expect = {}
    for r in pl.of(b'ARMO'):
        a = parse_armo(r, pl)
        assert r.flags & 0x4 == 0 and a['enchant'] is None and a['template'] is None, a['edid']
        value, weight, kws, part = frame_for(a)
        bod = r.sub(b'BOD2'); assert bod is not None and len(bod) == 8
        subs = rewrite_subs(r.subs, replace={b'DATA': struct.pack('<If', int(value), float(weight)),
                                             b'DNAM': struct.pack('<I', 0), b'BOD2': bod[:4] + struct.pack('<I', 2)},
                            keywords=kws)
        # drop armature links that are not the mod's own ArmorAddons (stray vanilla GoldAmuletAA)
        dropped = []
        cleaned = []
        for sig, d in subs:
            if sig == b'MODL' and len(d) == 4 and (struct.unpack_from('<I', d, 0)[0] >> 24) != src_idx:
                dropped.append(pl.fmt(struct.unpack_from('<I', d, 0)[0])); continue
            cleaned.append((sig, d))
        recs.append((b'ARMO', r.flags, r.formid, r.tail, build_subrecords(cleaned)))
        expect[r.formid] = dict(kind='ARMO', value=value, weight=weight, kws=sorted(kws), part=part)
        log.append('ARMO %-28s %-9s slots=%-6s %s AR%s val%s wt%.1f  ->  Clothing AR0 val%s wt%s kw%d%s' % (
            a['edid'], part, a['slots'], a['armor_type'], a['ar'], a['value'], a['weight'], value, weight, len(kws),
            ('  dropped stray armature %s' % dropped) if dropped else ''))

    for r in pl.of(b'COBJ'):
        c = parse_cobj(r, pl)
        e = c['edid']
        if e.startswith('TemperArmor'):
            subs = rewrite_subs(r.subs, replace={b'BNAM': struct.pack('<I', (req_idx << 24) | REQ_DISABLE_RECIPE)})
            recs.append((b'COBJ', r.flags, r.formid, r.tail, build_subrecords(subs)))
            expect[r.formid] = dict(kind='TEMPER')
            log.append('COBJ %-42s tempering -> REQ_DisableRecipe' % e)
        elif e.startswith('RecipeArmor'):
            jewelry = 'Jewelry' in e
            perk = PERK_ADV_BLACKSMITH if jewelry else PERK_CRAFTSMANSHIP
            new = []
            for sig, d in r.subs:
                if jewelry and sig == b'COCT':
                    new.append((b'COCT', struct.pack('<I', 2))); continue
                if jewelry and sig == b'CNTO':
                    if not any(s2 == b'CNTO' for s2, _ in new):
                        new.append((b'CNTO', struct.pack('<II', INGOT_SILVER, 1)))
                        new.append((b'CNTO', struct.pack('<II', GEM_GARNET_FLAWLESS, 2)))
                    continue
                new.append((sig, d))
                if sig == b'CTDA':
                    new.append((b'CTDA', hasperk_ctda(tmpl, perk)))
            assert sum(1 for s2, _ in new if s2 == b'CTDA') == 2, e
            recs.append((b'COBJ', r.flags, r.formid, r.tail, build_subrecords(new)))
            expect[r.formid] = dict(kind='CRAFT', perk=perk, jewelry=jewelry)
            log.append('COBJ %-42s forge: + HasPerk(%s)%s' % (e, 'AdvancedBlacksmithing' if jewelry else 'Craftsmanship',
                                                              '  items -> 1 silver ingot + 2 flawless garnets' if jewelry else ''))
        else:
            log.append('COBJ %-42s left as authored (book recipe at the tanning rack)' % e)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, OUT_NAME)
    n = write_patch(out, masters, recs, author='Authoria', description=DESC, esl=True)
    print('wrote %s: %d bytes, %d records, masters %s' % (OUT_NAME, n, len(recs), masters))
    for l in log:
        print('  ', l)

    # ------------------------------------------------------------- verify
    p = Plugin(out)
    d = open(out, 'rb').read()
    flags = struct.unpack_from('<I', d, 8)[0]; fv = struct.unpack_from('<H', d, 20)[0]
    assert flags & 0x200, 'ESL flag missing'
    assert fv == 44, 'form version %d' % fv
    assert p.masters == masters, p.masters
    assert len(p.records) == len(recs) == len(expect), (len(p.records), len(recs), len(expect))
    src_by = pl.by_formid()
    fails = 0
    for r in p.records:
        ex = expect[r.formid]
        s = src_by[r.formid]
        if ex['kind'] == 'ARMO':
            a = parse_armo(r, p); a0 = parse_armo(s, pl)
            kws = sorted(int(k.split(':')[0], 16) for k in a['keywords'] if k.endswith('Skyrim.esm'))
            ok = (a['armor_type'] == 'Clothing' and a['ar'] == 0 and a['value'] == ex['value']
                  and abs(a['weight'] - ex['weight']) < 1e-6 and kws == ex['kws']
                  and all(k.endswith('Skyrim.esm') for k in a['keywords'])
                  and '06BBE3:Skyrim.esm' not in a['keywords']
                  and all(arm.endswith(pl.name) for arm in a['armature'])
                  and a['name'] == a0['name'] and a['slots'] == a0['slots'] and a['edid'] == a0['edid']
                  and r.sub(b'DESC') == s.sub(b'DESC') and r.subs_all(b'MOD2') == s.subs_all(b'MOD2'))
        elif ex['kind'] == 'TEMPER':
            c = parse_cobj(r, p); c0 = parse_cobj(s, pl)
            ok = c['workbench'] == 'AD3B01:Requiem.esp' and c['created'] == c0['created'] and c['items'] == c0['items'] \
                and len(c['conditions']) == len(c0['conditions'])
        else:
            c = parse_cobj(r, p); c0 = parse_cobj(s, pl)
            conds = c['conditions']
            ok = (c['workbench'] == c0['workbench'] and c['created'] == c0['created'] and len(conds) == 2
                  and conds[0]['func'] == 'GetItemCount' and conds[0]['p1_fmt'] == '000857:Burlesque.esp'
                  and conds[1]['func'] == 'HasPerk' and conds[1]['p1'] == ex['perk'] and not conds[1]['or_'])
            if ex['jewelry']:
                ok = ok and c['items'] == [('05ACE3:Skyrim.esm', 1), ('068521:Skyrim.esm', 2)] and r.sub(b'COCT') == struct.pack('<I', 2)
            else:
                ok = ok and c['items'] == c0['items']
        if not ok:
            fails += 1; print('  FAIL', p.fmt(r.formid), r.edid)
    # full-plugin reconciliation
    total = len(pl.records)
    armo = len(pl.of(b'ARMO')); cobj = len(pl.of(b'COBJ')); arma = len(pl.of(b'ARMA')); txst = len(pl.of(b'TXST')); book = len(pl.of(b'BOOK'))
    patched_cobj = sum(1 for e in expect.values() if e['kind'] != 'ARMO')
    print('verify: %d records re-read, %d failures' % (len(p.records), fails))
    print('reconcile: %d total = ARMO %d patched + COBJ %d patched + COBJ %d kept (book recipe) + ARMA %d cosmetic + TXST %d cosmetic + BOOK %d skipped' % (
        total, armo, patched_cobj, cobj - patched_cobj, arma, txst, book))
    assert armo + patched_cobj + (cobj - patched_cobj) + arma + txst + book == total
    assert fails == 0
    print('PATCH OK')


if __name__ == '__main__':
    main()
