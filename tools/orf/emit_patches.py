"""
Emit one *_ORF_KID.ini per mod for the whole Authoria load order.

The split rule (agreed 2026-08-19), forced by ORF testing WornHasKeyword, which
pools every equipped piece:

  COLOUR + CHARACTER -> outer garment only (must occupy biped slot 32)
  SHAPE + COVERAGE   -> whichever piece actually IS that thing, any slot

Colour comes from colour_final.json, read off the texture the game really
loads (retextures win). Everything else is derived from the record's name,
slot mask, armour class and rating.

Addressing is by FormID, not EditorID: the Reqtificator renames EditorIDs on
Requiem-touched gear and FormIDs survive that.
"""

import json, os, re, sys, collections

SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\a51f92a9-dc4d-4048-b276-0ba2edcd4eb4\scratchpad\orf'
OUT = r'C:\1. AUTHORIA\mods\Authoria - ORF Patches'

sys.path.insert(0, r'C:\1. AUTHORIA\_tools\orf')
import esp_mesh_map as E

BODY, HOOD, LOWER, UNDER = 32, {30, 31, 45}, {49, 52, 53, 54}, {44, 46, 56}


def rx(*w):
    return re.compile('(' + '|'.join(w) + ')', re.I)


R_HOOD = rx('hood', 'cowl', 'coif')
R_ROBE = rx('robe', 'vestment', 'habit', 'cassock')
R_DRESS = rx('dress', 'gown', 'sundress', 'cheongsam', 'ao dai', 'kimono', 'frock')
R_SHORTSK = rx('mini ?skirt', 'short skirt', 'micro skirt', 'miniskirt')
R_SKIRT = rx('skirt', 'kilt')
R_UNDIES = rx('underwear', 'panties', 'panty', 'briefs', 'thong', 'knickers',
              'smallclothes', 'small clothes', 'loincloth', 'shorts')
R_BRA = rx(r'\bbra\b', 'bralette', 'bandeau', 'pasties', 'nipple', 'bikini',
           'chest wrap', 'string bra')
R_SHEER = rx('sheer', 'transparent', 'see.?through', 'lace', 'veil', 'stocking')
R_LEATHER = rx('leather', 'hide armor', 'studded')
R_STURDY = rx('plate', 'ebony', 'daedric', 'dragonplate', 'dragonscale', 'orcish',
              'dwarven', 'stalhrim', 'nordic carved', 'lamellar', 'cuirass',
              'breastplate', 'brigandine', 'chainmail', 'steel')
R_SCRUFFY = rx('ragged', r'rags\b', 'tattered', 'torn', 'dirty', 'patched', 'beggar',
               'prisoner', 'shabby', 'ruined', 'damaged', 'filthy', 'worn ', 'rusty',
               'slave', 'vagrant')
R_CLASSY = rx('fine ', 'noble', 'royal', 'gilded', 'elegant', 'regal', 'court',
              'exquisite', 'ornate', 'aristocrat', 'gala', 'gown', 'finery',
              'emperor', 'archmage', 'arch-mage', 'wedding')
R_INTIMID = rx('daedric', 'ebony', 'bone ', 'necro', 'dread', 'vampire', 'chitin',
               'nightingale', 'deathbrand', 'miraak', 'falmer', 'draugr',
               'executioner', 'blood', 'death', 'void', 'cultist')
R_SKIMPY = rx('bikini', 'sling', 'lewd', 'slutty', 'naked', 'nude', 'micro', 'strap',
              'harness', 'pasties', 'thong', 'skimp', 'revealing', 'succubus',
              'leotard', 'swimsuit', 'bunny', 'open waist', 'virgin killer',
              'virgin destroyer', 'corset', 'romper')
R_TIGHT = rx('bodysuit', 'catsuit', 'latex', 'skin.?tight', 'leotard', 'corset',
             'swimsuit', 'tight')
R_MODERN = rx('tshirt', 't-shirt', 'blazer', 'hoodie', 'sweater', 'swimsuit',
              'cheerleader', 'bunny', 'leotard', 'minidress', 'turtleneck',
              'ao dai', 'sailor', 'tuxedo', 'harvard', 'cccp', 'asics', 'denim',
              'jacket', 'apron - ', 'school')

FROM_OTHER_GAME = {
    'Twilight Princess Armor.esp',
    'Twilight Princess Armor - Alt Textures and Cloth Addon.esp',
    'Dragon Age Isabella Outfit.esp',
    'Shanoa Armor.esp',
    'KW_SerasArmor.esp',
}
MODERN_MODS = {
    '[Caenarvon] Cosplay Pack.esp',
    '[Caenarvon] Cosplay Pack Casual.esp',
    'Sonders_CosplayCasualAddon.esp',
}


def derive(rec, colour_of_tex, tex, plug):
    name = rec.get('n') or ''
    slots = set(rec.get('slots') or [])
    hay = name + ' ' + (rec.get('e') or '')
    atype = (rec.get('type') or '').lower()
    ar = float(rec.get('ar') or 0)
    outer = BODY in slots
    kw = set()

    # ---- SHAPE / COVERAGE : any slot ----
    if R_HOOD.search(hay) and (slots & HOOD or outer):
        kw.add('ORF_Hooded')
    if outer and R_ROBE.search(hay):
        kw.add('ORF_Robes')
    if outer and R_DRESS.search(hay):
        kw.add('ORF_Dress')
    if R_SHORTSK.search(hay):
        kw.add('ORF_ShortSkirt')
    elif (slots & LOWER) and R_SKIRT.search(hay):
        kw.add('ORF_ShortSkirt')
    if R_UNDIES.search(hay) and not outer:
        kw.add('ORF_Underwear')
    if R_BRA.search(hay):
        kw.add('ORF_Bra')
    if R_SHEER.search(hay):
        kw.add('ORF_Transparent')
    if R_TIGHT.search(hay):
        kw.add('ORF_Tight')
    if R_SKIMPY.search(hay):
        kw.add('ORF_Revealing')
        if outer:
            kw.add('ORF_Cleavage')
        if re.search(r'pasties|nipple|string|sling|micro|naked|nude|thong', hay, re.I):
            kw.add('ORF_NearlyNaked')

    # ---- COLOUR + CHARACTER : outer garment only ----
    if outer:
        c = colour_of_tex.get(tex) if tex else None
        if c:
            kw.add(c)
        if R_LEATHER.search(hay):
            kw.add('ORF_Leather')
        if R_STURDY.search(hay) or (atype == 'heavyarmor' and ar >= 20):
            kw.add('ORF_Sturdy')
        if R_SCRUFFY.search(hay):
            kw.add('ORF_Scruffy')
        elif R_CLASSY.search(hay):
            kw.add('ORF_Classy')
        if R_INTIMID.search(hay):
            kw.add('ORF_Intimidating')
        if atype == 'clothing' and ar <= 1 and 'ORF_Revealing' in kw:
            kw.add('ORF_Flimsy')
        if plug in FROM_OTHER_GAME:
            kw.add('ORF_FromOtherGame')
        elif plug in MODERN_MODS and R_MODERN.search(hay):
            kw.add('ORF_OutOfPlace')

    return kw


ORDER = ['ORF_Hooded', 'ORF_Robes', 'ORF_Dress', 'ORF_ShortSkirt', 'ORF_Bra',
         'ORF_Underwear', 'ORF_Transparent', 'ORF_Tight', 'ORF_Cleavage',
         'ORF_Revealing', 'ORF_NearlyNaked', 'ORF_Flimsy', 'ORF_Leather',
         'ORF_Sturdy', 'ORF_Scruffy', 'ORF_Classy', 'ORF_Intimidating',
         'ORF_FromOtherGame', 'ORF_OutOfPlace',
         'ORF_Red', 'ORF_Blue', 'ORF_Green', 'ORF_Black', 'ORF_White', 'ORF_Brown',
         'ORF_Grey', 'ORF_Gold', 'ORF_Silver', 'ORF_Yellow', 'ORF_Pink',
         'ORF_Purple', 'ORF_Colourful']


def safe(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def main():
    census = json.load(open(os.path.join(SP, 'census_final.json')))
    texmap = json.load(open(os.path.join(SP, 'tex_map.json')))
    colour = json.load(open(os.path.join(SP, 'colour_final.json')))
    paths = json.load(open(os.path.join(SP, 'plugin_paths.json')))
    os.makedirs(OUT, exist_ok=True)

    written, stats = 0, collections.Counter()
    for plug, recs in census.items():
        ppath = paths.get(plug)
        if not ppath:
            continue
        armo, _arma, _txst = E.build_map(ppath)
        by_edid = {r['edid'].lower(): fid for fid, r in armo.items() if r['edid']}
        tm = texmap.get(plug, {})
        assign = collections.defaultdict(list)
        names = collections.defaultdict(set)
        for r in recs:
            if not r.get('n'):
                continue
            slots = set(r.get('slots') or [])
            if not (BODY in slots or slots & HOOD or slots & LOWER or slots & UNDER):
                continue
            fid = by_edid.get((r['e'] or '').lower())
            if fid is None:
                stats['record not in defining plugin'] += 1
                continue
            tex = (tm.get(r['e']) or {}).get('tex')
            kws = derive(r, colour, tex, plug)
            if not kws:
                stats['no keyword earned'] += 1
                continue
            tok = '0x%06X~%s' % (fid, plug)
            for k in kws:
                assign[k].append(tok)
                names[k].add(r['n'])
            stats['records tagged'] += 1
        if not assign:
            continue
        lines = ['; ' + '=' * 72,
                 ';  Outfit Recognition Framework  --  %s' % plug,
                 ';  Authored for the Authoria load order, 2026-08-19.',
                 ';',
                 ';  Colour and character keywords are on slot-32 outer garments ONLY.',
                 ';  ORF tests WornHasKeyword, which pools every worn piece, so colour on',
                 ';  boots or a helmet would make the whole outfit read as that colour.',
                 ';  Shape and coverage keywords go on whichever piece actually is that',
                 ';  thing, on any slot.',
                 ';',
                 ';  Colours were read off the texture this load order actually loads,',
                 ';  which is often a retexture rather than the mod author\'s own.',
                 ';  FormID addressing survives Reqtificator EditorID renames.',
                 '; ' + '=' * 72, '']
        for k in ORDER:
            ids = sorted(set(assign.get(k, [])))
            if not ids:
                continue
            sample = sorted(names[k])[:3]
            lines.append('; %s -- %d item(s): %s%s'
                         % (k, len(ids), ', '.join(s[:34] for s in sample),
                            ' ...' if len(names[k]) > 3 else ''))
            for i in range(0, len(ids), 6):
                lines.append('Keyword = %s|Armor|%s' % (k, ','.join(ids[i:i + 6])))
            lines.append('')
        fn = 'ORF - %s_ORF_KID.ini' % safe(plug.rsplit('.', 1)[0])
        open(os.path.join(OUT, fn), 'w', encoding='utf-8').write('\n'.join(lines))
        written += 1
        stats['keyword lines'] += sum(1 for l in lines if l.startswith('Keyword'))
    print('patch files written: %d' % written)
    for k, v in stats.most_common():
        print('   %-32s %d' % (k, v))


if __name__ == '__main__':
    main()
