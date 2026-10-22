"""Enumerate every record of the two outfit plugins with the fields Requiem cares about."""
import sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\requiem-clothing-patch")
from esp_tools import Plugin, parse_armo, parse_cobj, parse_book

PLUGINS = [r"C:\1. AUTHORIA\mods\Magic Pariah - Meadowlark Physics\Magic Pariah.esp",
           r"C:\1. AUTHORIA\mods\Burlesque Dress\Burlesque.esp"]
KW = {'06BBE3:Skyrim.esm': 'REQ_ArmorSet_Iron', '06BBE8:Skyrim.esm': 'ArmorClothing', '06BBE9:Skyrim.esm': 'ArmorJewelry',
      '08F959:Skyrim.esm': 'VendorItemArmor', '08F95B:Skyrim.esm': 'VendorItemClothing', '08F95A:Skyrim.esm': 'VendorItemJewelry',
      '0A8657:Skyrim.esm': 'ClothingBody', '0A865D:Skyrim.esm': 'ClothingRich', '0A865C:Skyrim.esm': 'ClothingPoor',
      '10CD11:Skyrim.esm': 'ClothingHead', '10CD12:Skyrim.esm': 'ClothingFeet', '10CD13:Skyrim.esm': 'ClothingHands',
      '06C0EC:Skyrim.esm': 'ArmorCuirass', '06C0ED:Skyrim.esm': 'ArmorBoots', '06C0EF:Skyrim.esm': 'ArmorGauntlets',
      '06C0EE:Skyrim.esm': 'ArmorHelmet', '06BBD2:Skyrim.esm': 'ArmorHeavy', '06BBD3:Skyrim.esm': 'ArmorLight',
      '10CD09:Skyrim.esm': 'ClothingRing', '10CD0A:Skyrim.esm': 'ClothingNecklace', '0A8664:Skyrim.esm': 'JewelryExpensive',
      '0ADB78:Skyrim.esm': 'CraftingSmithingArmorTable', '088105:Skyrim.esm': 'CraftingSmithingForge',
      '07BCFA:Skyrim.esm': 'CraftingTanningRack', '0A5CCE:Skyrim.esm': 'CraftingSmelter', '0A5CB3:Skyrim.esm': 'CraftingCookpot',
      '0A5CA3:Skyrim.esm': 'CraftingTanningRack?', '0AE0BE:Skyrim.esm': 'VendorItemBook', '0917E7:Skyrim.esm': 'VendorItemClutter'}


def kn(f):
    return KW.get(f, f)


for p in PLUGINS:
    pl = Plugin(p)
    print('=' * 100)
    print(pl.name, '| masters', pl.masters, '| records', len(pl.records),
          '| types', sorted(set(r.sig.decode() for r in pl.records)))
    print('-- ARMO')
    for r in pl.of(b'ARMO'):
        a = parse_armo(r, pl)
        print('  %s %-30s %-24s slots=%-8s %-10s AR=%-5s val=%-4s wt=%-4s flags=0x%X' % (
            a['formid'], a['edid'], a['name'], a['slots'], a['armor_type'], a['ar'], a['value'], a['weight'], a['flags']))
        print('       kw=%s  arma=%s ench=%s tmpl=%s' % ([kn(k) for k in a['keywords']], a['armature'], a['enchant'], a['template']))
    print('-- COBJ')
    for r in pl.of(b'COBJ'):
        c = parse_cobj(r, pl)
        conds = ['%s%s %s %s%s' % (c2['func'], '(%s)' % c2['p1_fmt'], ['==', '!=', '>', '>=', '<', '<='][c2['op']] if c2['op'] < 6 else c2['op'],
                                    c2['comp'], ' OR' if c2['or_'] else '') for c2 in c['conditions']]
        print('  %s %-42s -> %s x%s @%s items=%s conds=%s' % (
            c['formid'], c['edid'], c['created'], c['count'], kn(c['workbench']) if c['workbench'] else None,
            [(kn(i), n) for i, n in c['items']], conds))
    print('-- BOOK')
    for r in pl.of(b'BOOK'):
        b = parse_book(r, pl)
        print('  ', b, [kn(k) for k in b['keywords']])
    print('-- other types')
    for r in pl.records:
        if r.sig not in (b'ARMO', b'COBJ', b'BOOK'):
            print('  %s %s %s' % (r.sig.decode(), pl.fmt(r.formid), r.edid))
