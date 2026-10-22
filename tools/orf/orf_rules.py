"""
ORF keyword derivation engine.

Two classes of keyword, per the split rule agreed 2026-08-19:

  COLOUR + CHARACTER  -> outer garment only. Hard gate: the record must occupy
                         the Body bit (FirstPersonFlags & 4). Never boots,
                         gloves, helmets, circlets, capes.
  SHAPE + COVERAGE    -> whichever piece actually IS that thing, any slot.

Why the gate matters: ORF tests WornHasKeyword, which pools every equipped
piece. Colour on boots makes the whole outfit read as that colour.

Slot values are from the verified biped-slot table (slot N = bit N-30).
Modder slots (44-49, 52-60) carry no engine-enforced meaning, so shape is
driven by NAME, never by slot number alone. Slot is used only to decide
"is this the outer garment" (Body bit) and "is this definitely not" .
"""

import re

BODY      = 1 << 2      # slot 32
HEAD      = 1 << 0      # slot 30
HAIR      = 1 << 1      # slot 31
HANDS     = 1 << 3      # slot 33
FOREARMS  = 1 << 4      # slot 34
AMULET    = 1 << 5      # slot 35
RING      = 1 << 6      # slot 36
FEET      = 1 << 7      # slot 37
CALVES    = 1 << 8      # slot 38
SHIELD    = 1 << 9      # slot 39
CIRCLET   = 1 << 12     # slot 42

# Accessory bits that must never receive colour even if they also set Body
# (they don't, but keep the intent explicit).
NEVER_COLOUR_ONLY = HANDS | FOREARMS | AMULET | RING | FEET | CALVES | SHIELD | CIRCLET

COLOURS = ['ORF_Red','ORF_Blue','ORF_Green','ORF_Black','ORF_White','ORF_Brown',
           'ORF_Grey','ORF_Gold','ORF_Silver','ORF_Yellow','ORF_Pink','ORF_Purple',
           'ORF_Colourful']
CHARACTER = ['ORF_Classy','ORF_Scruffy','ORF_Flimsy','ORF_Sturdy','ORF_Intimidating',
             'ORF_Leather']
SHAPE = ['ORF_Hooded','ORF_Robes','ORF_Dress','ORF_ShortSkirt','ORF_Cleavage',
         'ORF_Tight','ORF_Revealing','ORF_Transparent','ORF_NearlyNaked',
         'ORF_Bra','ORF_Underwear']
SITUATIONAL = ['ORF_FromOtherGame','ORF_OutOfPlace','ORF_Inappropriate']

def _rx(*words):
    return re.compile(r'(' + '|'.join(words) + r')', re.I)

RE_HOOD     = _rx('hood','cowl','coif')
RE_ROBE     = _rx('robe','vestment','habit','cassock','frock coat')
RE_DRESS    = _rx('dress','gown','sundress','cheongsam','ao dai','kimono','qipao')
RE_SKIRT    = _rx('skirt','miniskirt','mini-skirt')
RE_SHORTSK  = _rx('mini ?skirt','short skirt','micro skirt')
RE_UNDIES   = _rx('underwear','panties','panty','briefs','thong','knickers',
                  'smallclothes','small clothes','loincloth','undergarment')
RE_BRA      = _rx('\\bbra\\b','bralette','bandeau','pasties','nipple','bikini top',
                  'chest wrap','breast')
RE_SHEER    = _rx('sheer','transparent','see.?through','lace','mesh','veil','silk stocking')
RE_LEATHER  = _rx('leather','hide','studded')
RE_STURDY   = _rx('plate','ebony','daedric','dragonplate','dragonscale','orcish',
                  'dwarven','stalhrim','nordic carved','steel plate','lamellar',
                  'cuirass','breastplate','brigandine')
RE_SCRUFFY  = _rx('ragged','rags\\b','tattered','torn','dirty','patched','beggar',
                  'prisoner','worn ','shabby','ruined','damaged','filthy')
RE_CLASSY   = _rx('fine','noble','royal','gilded','elegant','regal','court',
                  'exquisite','ornate','aristocrat','gala','ball ','couture')
RE_INTIMID  = _rx('daedric','ebony','bone','necro','dread','vampire','chitin',
                  'nightingale','deathbrand','miraak','falmer','draugr','executioner')
RE_SKIMPY   = _rx('bikini','sling','lewd','slutty','naked','nude','micro','strap',
                  'harness','pasties','thong','open ','bare','skimp','revealing',
                  'succubus','leotard','swimsuit','bunny')
RE_TIGHT    = _rx('bodysuit','catsuit','latex','skintight','skin.?tight','leotard',
                  'corset','tight')


def slot_list(mask):
    """Decode a FirstPersonFlags mask to the slot numbers it occupies."""
    return [30 + b for b in range(32) if mask & (1 << b)]


def is_outer_garment(mask, name):
    """Colour eligibility. Must occupy the Body slot."""
    if mask & BODY:
        return True
    # A dress/robe/gown that somehow skips slot 32 is still the outer garment.
    if RE_DRESS.search(name) or RE_ROBE.search(name):
        return True
    return False


def derive(rec, mod_flags=None):
    """
    rec: {"e": editorid, "n": name, "slot": int mask, "type": ArmorType,
          "ar": armor rating, "v": value, "w": weight}
    mod_flags: per-mod situational keywords, e.g. {"ORF_FromOtherGame": True}

    Returns (keywords:set, needs_eye:set) -- the second set names the keywords
    that this record is a CANDIDATE for but which must be confirmed by looking
    at the texture. Nothing in needs_eye is emitted until confirmed.
    """
    name = rec.get('n') or ''
    eid  = rec.get('e') or ''
    hay  = name + ' ' + eid
    mask = int(rec.get('slot') or 0)
    atype = (rec.get('type') or '').lower()
    ar = float(rec.get('ar') or 0)
    val = float(rec.get('v') or 0)

    kw, eye = set(), set()
    outer = is_outer_garment(mask, hay)

    # ---------- SHAPE / COVERAGE : any slot, driven by name ----------
    if RE_HOOD.search(hay):
        kw.add('ORF_Hooded')
    if outer and RE_ROBE.search(hay):
        kw.add('ORF_Robes')
    if outer and RE_DRESS.search(hay):
        kw.add('ORF_Dress')
    if RE_SHORTSK.search(hay):
        kw.add('ORF_ShortSkirt')
    elif RE_SKIRT.search(hay):
        eye.add('ORF_ShortSkirt')          # is the hem actually short?
    if RE_UNDIES.search(hay):
        kw.add('ORF_Underwear')
    if RE_BRA.search(hay):
        kw.add('ORF_Bra')
    if RE_SHEER.search(hay):
        eye.add('ORF_Transparent')
    if RE_TIGHT.search(hay):
        eye.add('ORF_Tight')
    if RE_SKIMPY.search(hay):
        eye.add('ORF_Revealing'); eye.add('ORF_Cleavage'); eye.add('ORF_NearlyNaked')
    elif outer:
        # every outer garment is a candidate for the coverage keywords
        eye.add('ORF_Revealing'); eye.add('ORF_Cleavage')

    # ---------- CHARACTER : outer garment only ----------
    if outer:
        if RE_LEATHER.search(hay):
            kw.add('ORF_Leather')
        if RE_STURDY.search(hay) or (atype == 'heavy' and ar >= 20):
            kw.add('ORF_Sturdy')
        if RE_SCRUFFY.search(hay):
            kw.add('ORF_Scruffy')
        if RE_CLASSY.search(hay) or (atype == 'clothing' and val >= 400):
            kw.add('ORF_Classy')
        if RE_INTIMID.search(hay):
            kw.add('ORF_Intimidating')
        # ORF_Flimsy means NOTABLY flimsy, not merely "is clothing". The mod's
        # own vanilla file ships this line commented out, so be sparing: it
        # needs unarmoured AND skimpy/thin, confirmed by eye.
        if atype == 'clothing' and ar <= 1 and not RE_CLASSY.search(hay):
            eye.add('ORF_Flimsy')
        # colour is never derived from data -- always by eye
        eye.add('COLOUR')

    # ---------- SITUATIONAL : decided once per mod ----------
    for k, on in (mod_flags or {}).items():
        if on and outer:
            kw.add(k)

    # Scruffy and Classy are contradictory; name evidence wins over the value band.
    if 'ORF_Scruffy' in kw and 'ORF_Classy' in kw:
        kw.discard('ORF_Classy' if RE_SCRUFFY.search(hay) else 'ORF_Scruffy')

    return kw, eye


def emit(mod_name, assignments, header_notes=''):
    """
    assignments: {keyword: [editorid, ...]}
    Returns the text of a _KID.ini.
    """
    order = SHAPE + CHARACTER + COLOURS + SITUATIONAL
    lines = [
        '; ' + '=' * 72,
        ';  Outfit Recognition Framework - %s' % mod_name,
        ';  Authored for the Authoria load order. Colour is on outer garments',
        ';  only, because ORF tests WornHasKeyword and pools every worn piece.',
    ]
    if header_notes:
        for n in header_notes.splitlines():
            lines.append(';  ' + n)
    lines.append('; ' + '=' * 72)
    lines.append('')
    for k in order:
        ids = assignments.get(k)
        if not ids:
            continue
        # keep lines readable: wrap at ~8 ids
        ids = sorted(set(ids))
        for i in range(0, len(ids), 8):
            lines.append('Keyword = %s|Armor|%s' % (k, ','.join(ids[i:i + 8])))
    lines.append('')
    return '\n'.join(lines)
