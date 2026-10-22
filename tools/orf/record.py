"""
Record eyeballed colour decisions against the review sheets.

Keyed by CELL NUMBER, never by texture. Two earlier bugs live here as scar
tissue:
  1. The sheets are built from a SORTED, flattened list; indexing the unsorted
     colour_manual.json attaches every answer to the wrong texture. The truth
     is review_index.json, which stores the exact cell -> texture order drawn.
  2. Keying the store by texture silently dropped answers whenever two cells
     shared a texture (the same file used by two mods).
"""
import json, os, sys

SP = r'C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\a51f92a9-dc4d-4048-b276-0ba2edcd4eb4\scratchpad\orf'
DEC = os.path.join(SP, 'colour_decisions.json')
IDX = os.path.join(SP, 'review_index.json')

SHORT = {'k': 'ORF_Black', 'w': 'ORF_White', 'e': 'ORF_Grey', 'r': 'ORF_Red',
         'o': 'ORF_Brown', 'g': 'ORF_Green', 'b': 'ORF_Blue', 'y': 'ORF_Yellow',
         'd': 'ORF_Gold', 's': 'ORF_Silver', 'p': 'ORF_Pink', 'v': 'ORF_Purple',
         'c': 'ORF_Colourful', '-': None}


def cell_map():
    out = {}
    for sh in json.load(open(IDX)):
        for i, tex in enumerate(sh['cells']):
            out[sh['first'] + i] = {'tex': tex, 'name': sh['names'][i],
                                    'plug': sh['plugs'][i]}
    return out


def load():
    return json.load(open(DEC)) if os.path.exists(DEC) else {}


def put(spec):
    cm = cell_map()
    dec = load()
    # store keyed by texture for downstream use, but resolve THROUGH the cell map
    for n, code in spec.items():
        n = int(n)
        info = cm[n]
        kw = SHORT[code] if code in SHORT else code
        dec[info['tex']] = {'kw': kw, 'name': info['name'], 'plug': info['plug'],
                            'cell': n, 'src': 'eye'}
    json.dump(dec, open(DEC, 'w'), indent=1)
    return dec


def answered_cells():
    """Cell numbers that currently have an answer, via the cell map."""
    cm = cell_map()
    dec = load()
    have = set()
    for t, d in dec.items():
        have.add(d['cell'])
    return cm, have


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'missing':
        cm, have = answered_cells()
        miss = sorted(set(cm) - have)
        print('cells still unanswered: %d' % len(miss))
        import collections
        bysheet = collections.defaultdict(list)
        for c in miss:
            bysheet[(c - 1) // 12 + 1].append(c)
        for s in sorted(bysheet):
            print('  r%03d: %s' % (s, ' '.join(str(x) for x in bysheet[s])))
    else:
        dec = put(json.loads(sys.argv[1]))
        cm, have = answered_cells()
        print('recorded. %d/%d cells answered' % (len(have), len(cm)))
