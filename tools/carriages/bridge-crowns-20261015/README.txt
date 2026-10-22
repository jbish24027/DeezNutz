2026-10-15 bridge-crown fix for the Animated Carriage Terrain Fit patch.
bridges5.py   = loaders + facing-aware raycast (hits_facing) + the five chains as they were before the fix
audit_all.py  = every raised marker vs any non-roof surface above the cart (what found the five bridges)
profiles.py   = deck vs chord profile along a chain;  optimize.py / extra.py = height balancing + extra crown markers
final_check.py= residual as written;  create_markers.json / apply_ops.json = exactly what houseCARL wrote
All scripts read the 10-12 session pickles (near_refs.pkl, bases.pkl, elevated_res.pkl, model_src.json) from the OLD
scratchpad path hard-coded at the top of bridges5.py; copy those four files next to deck.py and point OLD at that folder
before rerunning. Rule: on a bridge with several upward surfaces, fit to the TOP non-roof one; then sample the chord and
add a marker at the crown if the sag exceeds ~10.
