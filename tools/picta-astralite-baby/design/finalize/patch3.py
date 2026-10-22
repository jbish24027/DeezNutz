import os
d = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(d, 'final2_model.py'); s = open(p, encoding='utf-8').read()
old = "WL_SCAT_SUN=25.0, WL_CLOUD_MEAN=0.0, CW_SCAT_SUN=1.0, SCAT_ITERS=6, SCAT_DAMP=1.0)"
new = "WL_SCAT_SUN=100.0, WL_CLOUD_MEAN=10.0, CW_SCAT_SUN=1.0, SCAT_ITERS=6, SCAT_DAMP=1.0, CFS_SHARE=0.0, WL_SCAT=100.0)"
assert old in s; s = s.replace(old, new)
old = "HUE_LO=90.0, HUE_HI=150.0"
new = "HUE_LO=120.0, HUE_HI=170.0"
assert old in s; s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
e = os.path.join(d, 'exp1.py'); t = open(e, encoding='utf-8').read()
t = t.replace("'cmean10': dict(WL_CLOUD_MEAN=10.0)}", "'cmean10': dict(WL_CLOUD_MEAN=10.0), 'purearc': dict(HUE_LO=179.0, HUE_HI=180.0), 'hue90_150': dict(HUE_LO=90.0, HUE_HI=150.0), 'alb2': dict(WL_ALB=2.0), 'alb20': dict(WL_ALB=20.0), 'cmean20': dict(WL_CLOUD_MEAN=20.0)}")
open(e, 'w', encoding='utf-8').write(t)
print('ok')
