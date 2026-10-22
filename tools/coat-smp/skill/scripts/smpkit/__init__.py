"""smpkit - script HDT-SMP / FSMP cloth physics onto Skyrim SE armour meshes (see ../../SKILL.md).

Settings (machine-specific, set once): environment variables, else smpkit/settings.json next to this file:
  PYNIFLY_DIR   the io_scene_nifly folder of a PyNifly release (holds pyn/ and NiflyDLL.dll)
  SKELETON_NIF  a Skyrim SE skeleton nif, e.g. <BodySlide>/CalienteTools/BodySlide/res/skeleton_female_sse.nif"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))


def setting(key):
    v = os.environ.get(key)
    if v: return v
    p = os.path.join(HERE, 'settings.json')
    if os.path.exists(p):
        return json.load(open(p, encoding='utf-8')).get(key)
    return None


def setup_pynifly(path=None):
    """make PyNifly importable as `pyn`"""
    path = path or setting('PYNIFLY_DIR')
    if not path:
        raise RuntimeError('PyNifly not configured: set PYNIFLY_DIR (environment or smpkit/settings.json) to the io_scene_nifly folder')
    path = os.path.abspath(path)
    if not os.path.exists(os.path.join(path, 'pyn', 'pynifly.py')):
        raise RuntimeError(f'{path} has no pyn/pynifly.py - PYNIFLY_DIR must be the io_scene_nifly folder of PyNifly')
    if path not in sys.path: sys.path.insert(0, path)
    return path


def init():
    """configure PyNifly + the skeleton, import and return the core module"""
    setup_pynifly()
    from smpkit import core
    sk = setting('SKELETON_NIF')
    if not sk: raise RuntimeError('SKELETON_NIF not configured (environment or smpkit/settings.json)')
    if not core.SKEL: core.set_skeleton(sk)
    return core


def load_design(path):
    """a design file is Python that defines DESIGN = dict(...); see designs/example_design.py"""
    import runpy
    ns = runpy.run_path(path)
    if 'DESIGN' not in ns: raise RuntimeError(f'{path} defines no DESIGN')
    d = ns['DESIGN']
    for k in ('name', 'prefix', 'title', 'stage', 'targets'):
        if k not in d: raise RuntimeError(f'{path}: DESIGN has no {k!r}')
    d['stage'] = d['stage'].replace(os.sep, '/').rstrip('/') + '/'
    d['work'] = (d.get('work') or os.path.join(os.path.dirname(os.path.abspath(path)), 'out')).replace(os.sep, '/').rstrip('/') + '/'
    os.makedirs(d['work'], exist_ok=True)
    for g, t in d['targets'].items():
        if t.get('mode') not in ('nif', 'bodyslide'): raise RuntimeError(f'{path}: target {g!r} needs mode "nif" or "bodyslide"')
    return d
