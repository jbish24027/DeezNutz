"""The DBVO .fuz filename rule, corrected 2026-08-28.

Derived from the installed pack, not assumed:

  1. Strip a trailing parenthetical tag - "(Persuade)", "(Sex)", "(Cancel Quest)",
     "(<BribeCost> gold)". It is a UI hint, not something the player says. The pack
     uses the stripped name 2,225 times against 13 for the full one.
     Only when a space precedes the '(': "you... (Persuade)" loses the tag,
     "you...(<BribeCost> gold)" keeps it.
  2. Trim.
  3. Space and the Windows-illegal characters \\ / : * ? " < > | become '_'.
  4. Append .fuz.

Everything else stays verbatim, curly quotes and ellipses included.
"""
import re

B = chr(92)
BAD = set(' ' + B + '/:*?"<>|')
TAG = re.compile(r'\s+\([^()]*\)\s*$')


def strip_tag(line, repeat=False):
    """Drop the trailing (tag). With repeat=True, keep dropping while one is left."""
    while True:
        s = TAG.sub('', line)
        if s == line or not s.strip():
            return line
        line = s
        if not repeat:
            return line


def dbvo_name(line, repeat=False):
    return ''.join('_' if c in BAD else c for c in strip_tag(line, repeat).strip()) + '.fuz'


def markup(line):
    """Text the game rewrites at runtime, judged AFTER the tag is stripped."""
    s = strip_tag(line)
    return ('<' in s and '>' in s) or s.count('*') >= 2 or '[' in s or ']' in s
