"""Write the FSMP xml for the grafted skirt: Meandering Meadowlark's skirt rig
(bones, constraints, collision) with rows 1-4 only, plus the Authoria tune.

TUNE history (numbers per row: angular lower / upper, stiffness, damping):
  v1 (2026-09-03, MM verbatim): rows 2-3 x -0.03..0.3 y +-0.03 z +-0.05 at stiffness 60 damping 0.9,
     row 4 x -0.05..0.3 at 50/45/40 damping 0.7, rings at stiffness 50-100. Too rigid.
  v2 (2026-09-03 "loose"): joints x -0.25..0.5, y/z +-0.2..0.3, springs 15/10/6, rings 20/15/12.
     Still too rigid; butt poked through the static hip band.
  v3 (2026-09-06 "flowy"): joints x -0.45..0.9, y/z +-0.3..0.4, springs 6/4/2, damping 0.3->0.15,
     rings 12/9/7 with wider angular play, bone damping halved, gravity 1.0; NEW per-vertex
     collider CollButt (the body's rear hips, cut into the nif by build_v3.py) that the skirt
     proxy collides with; NPC L/R Butt declared as static bones.
usage: python make_xml.py            -> writes OUT_DIR/MagicPariahSkirtHDT.xml (scratch)
       python make_xml.py --install  -> also copies it over both live xmls (backup .bak-v2-20260906)
"""
import os, shutil, sys
from graft import COLUMNS, sk_name, PROXY_NAME, OUT_DIR

TUNE = 'v3'
LIVE = [r"C:\1. AUTHORIA\mods\Magic Pariah - Meadowlark Physics\meshes\clothes\magic pariah\MagicPariahSkirtHDT.xml",
        r"C:\1. AUTHORIA\mods\Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah\magic pariah skirt HDT.xml"]
BAK_TAG = 'bak-v2-20260906'

BODY_BONES = [
    "NPC L Calf [LClf]", "NPC R Calf [RClf]", "NPC R Foot [Rft ]", "NPC L Foot [Lft ]",
    "NPC L Toe0 [LToe]", "NPC R Toe0 [RToe]", "NPC Head [Head]",
    "NPC L Clavicle [LClv]", "NPC R Clavicle [RClv]", "NPC L Forearm [LLar]", "NPC R Forearm [RLar]",
    "NPC L ForearmTwist1 [LLt1]", "NPC R ForearmTwist1 [RLt1]", "NPC L ForearmTwist2 [LLt2]", "NPC R ForearmTwist2 [RLt2]",
    "NPC L UpperArm [LUar]", "NPC R UpperArm [RUar]", "NPC L UpperarmTwist1 [LUt1]", "NPC R UpperarmTwist1 [RUt1]",
    "NPC L UpperarmTwist2 [LUt2]", "NPC R UpperarmTwist2 [RUt2]",
    "NPC Spine [Spn0]", "NPC Spine2 [Spn2]", "NPC Spine1 [Spn1]", "NPC Pelvis [Pelv]",
    "NPC L Thigh [LThg]", "NPC R Thigh [RThg]", "NPC L FrontThigh", "NPC R FrontThigh",
    "NPC L RearCalf [LrClf]", "NPC R RearCalf [RrClf]", "NPC L RearThigh", "NPC R RearThigh",
    "NPC L Hand [LHnd]", "NPC R Hand [RHnd]",
    "NPC L Butt", "NPC R Butt",                       # v3: the butt collider rides these too
]
# ring order used by MM for the horizontal constraints (closes the loop)
RING = ['front', 'frontA.l', 'frontB.l', 'side.l', 'backB.l', 'backA.l', 'back',
        'backA.r', 'backB.r', 'side.r', 'frontB.r', 'frontA.r', 'front']

def bone_default(mass, inertia, lin_damp, ang_damp, gravity):
    return """	<bone-default>
		<mass>%s</mass>
		<inertia x="%s" y="%s" z="%s" />
		<centerOfMassTransform>
			<basis x="0" y="0" z="0" w="1" />
			<origin x="0" y="0" z="0" />
		</centerOfMassTransform>
		<linearDamping>%s</linearDamping>
		<angularDamping>%s</angularDamping>
		<friction>0.85</friction>
		<restitution>0</restitution>
		<gravity-factor>%s</gravity-factor>
		<rollingFriction>0</rollingFriction>
	</bone-default>
""" % (mass, inertia, inertia, inertia, lin_damp, ang_damp, gravity)

def vdefault(ang_lo, ang_hi, stiff, damp):
    return """	<generic-constraint-default>
		<frameInB>
			<basis x="0" y="0" z="0" w="1" />
			<origin x="0" y="0" z="0" />
		</frameInB>
		<useLinearReferenceFrameA>false</useLinearReferenceFrameA>
		<linearLowerLimit x="0.0" y="0.0" z="0.0" />
		<linearUpperLimit x="0.0" y="0.0" z="0.0" />
		<angularLowerLimit x="%s" y="%s" z="%s" />
		<angularUpperLimit x="%s" y="%s" z="%s" />
		<linearStiffness x="%s" y="%s" z="%s" />
		<angularStiffness x="%s" y="%s" z="%s" />
		<linearDamping x="%s" y="%s" z="%s" />
		<angularDamping x="%s" y="%s" z="%s" />
		<linearEquilibrium x="0" y="0" z="0" />
		<angularEquilibrium x="0" y="0" z="0" />
	</generic-constraint-default>
""" % (ang_lo + ang_hi + stiff + stiff + damp + damp)

def hdefault(lin, ang, stiff, damp):
    return """	<generic-constraint-default>
		<frameInB>
			<basis x="0" y="0" z="0" w="1" />
			<origin x="0" y="0" z="0" />
		</frameInB>
		<useLinearReferenceFrameA>false</useLinearReferenceFrameA>
		<linearLowerLimit x="-%s" y="-%s" z="-%s" />
		<linearUpperLimit x="%s" y="%s" z="%s" />
		<angularLowerLimit x="-%s" y="-%s" z="-%s" />
		<angularUpperLimit x="%s" y="%s" z="%s" />
		<linearStiffness x="%s" y="%s" z="%s" />
		<angularStiffness x="%s" y="%s" z="%s" />
		<linearDamping x="%s" y="%s" z="%s" />
		<angularDamping x="%s" y="%s" z="%s" />
		<linearEquilibrium x="-0" y="-0" z="-0" />
		<angularEquilibrium x="-0" y="-0" z="-0" />
	</generic-constraint-default>
""" % ((lin,) * 6 + ang + ang + stiff + stiff + damp + damp)

TUNES = {
    'v2': dict(
        bones=(("1", "50", "0.1", "0.5", "0.9"), ("0.65", "33", "0.3", "0.5", "1")),
        joints={2: (("-0.25", "-0.2", "-0.2"), ("0.4", "0.2", "0.2"), ("15", "15", "12"), ("0.5", "0.4", "0.4")),
                3: (("-0.3", "-0.25", "-0.25"), ("0.45", "0.25", "0.25"), ("10", "10", "8"), ("0.4", "0.3", "0.3")),
                4: (("-0.35", "-0.3", "-0.3"), ("0.5", "0.3", "0.3"), ("6", "6", "5"), ("0.3", "0.25", "0.25"))},
        rings={2: ("24.0", ("0.08", "0.08", "0.12"), ("20", "20", "20"), ("0.1", "0.1", "0.1")),
               3: ("19.0", ("0.12", "0.12", "0.18"), ("15", "15", "15"), ("0.1", "0.1", "0.1")),
               4: ("25.0", ("0.15", "0.15", "0.20"), ("12", "20", "12"), ("0.15", "0.15", "0.15"))},
        butt=False),
    'v3': dict(
        bones=(("1", "50", "0.05", "0.3", "1"), ("0.65", "33", "0.15", "0.3", "1")),
        joints={2: (("-0.45", "-0.3", "-0.3"), ("0.7", "0.3", "0.3"), ("6", "6", "5"), ("0.3", "0.25", "0.25")),
                3: (("-0.5", "-0.35", "-0.35"), ("0.8", "0.35", "0.35"), ("4", "4", "3"), ("0.25", "0.2", "0.2")),
                4: (("-0.55", "-0.4", "-0.4"), ("0.9", "0.4", "0.4"), ("2", "2", "2"), ("0.2", "0.15", "0.15"))},
        rings={2: ("24.0", ("0.12", "0.12", "0.18"), ("12", "12", "12"), ("0.1", "0.1", "0.1")),
               3: ("19.0", ("0.18", "0.18", "0.25"), ("9", "9", "9"), ("0.1", "0.1", "0.1")),
               4: ("25.0", ("0.22", "0.22", "0.30"), ("7", "12", "7"), ("0.15", "0.15", "0.15"))},
        butt=True),
}

def build(tune=TUNE):
    T = TUNES[tune]
    L = []
    L.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    L.append('<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">\n')
    L.append('<!-- Magic Pariah skirt on the Meandering Meadowlark skirt rig (both by blickRARRI).\n')
    L.append('     Rig and leg colliders are MM\'s MMDress.xml, rows 1-4 only (the MP skirt ends at the knee),\n')
    L.append('     grafted 2026-09-03. Authoria tune %s (see _tools\\magic-pariah-mm-rig\\make_xml.py). -->\n' % tune)
    L.append('<!-- bones -->\n <!-- static -->\n  <!-- body -->\n')
    for b in BODY_BONES:
        L.append('\t<bone name="%s"/>\n' % b)
    L.append(' <!-- anchor (row 1, rides the pelvis) -->\n')
    for c in COLUMNS:
        L.append('\t<bone name="%s"/>\n' % sk_name(c, 1))
    L.append(' <!-- cloth -->\nSKIRT\n')
    L.append(bone_default(*T['bones'][0]))
    for r in (2, 3):
        for c in COLUMNS:
            L.append('\t<bone name="%s"/>\n' % sk_name(c, r))
    L.append(bone_default(*T['bones'][1]))
    for c in COLUMNS:
        L.append('\t<bone name="%s"/>\n' % sk_name(c, 4))
    L.append('<!-- constraints -->\nSKIRT VERTICAL\n')
    for r in (2, 3, 4):
        L.append(vdefault(*T['joints'][r]))
        for c in COLUMNS:
            L.append('\t<generic-constraint bodyA="%s" bodyB="%s"/>\n' % (sk_name(c, r), sk_name(c, r - 1)))
    L.append('SKIRT HORIZONTAL\n')
    for r in (2, 3, 4):
        L.append(hdefault(*T['rings'][r]))
        for a, b in zip(RING[:-1], RING[1:]):
            L.append('\t<generic-constraint bodyA="%s" bodyB="%s"/>\n' % (sk_name(a, r), sk_name(b, r)))
    L.append('<!-- colliders -->\n <!-- static -->\n')
    L.append("""	<per-vertex-shape name="CollThigh">
		<margin>0.8</margin>
		<penetration>0.2</penetration>
		<shared>private</shared>
		<tag>Thigh</tag>
		<can-collide-with-tag>skirt</can-collide-with-tag>
		<weight-threshold bone="NPC R Thigh [RThg]">0.1</weight-threshold>
		<weight-threshold bone="NPC L Thigh [LThg]">0.1</weight-threshold>
	</per-vertex-shape>
	<per-vertex-shape name="CollCalves">
		<margin>1.7</margin>
		<penetration>1.1</penetration>
		<shared>private</shared>
		<tag>Calves</tag>
		<can-collide-with-tag>skirt</can-collide-with-tag>
		<weight-threshold bone="NPC R Calf [RClf]">0.2</weight-threshold>
		<weight-threshold bone="NPC L Calf [LClf]">0.2</weight-threshold>
	</per-vertex-shape>
""")
    if T['butt']:
        L.append("""	<per-vertex-shape name="CollButt">
		<margin>1.2</margin>
		<penetration>0.3</penetration>
		<shared>private</shared>
		<tag>Butt</tag>
		<can-collide-with-tag>skirt</can-collide-with-tag>
		<weight-threshold bone="NPC Pelvis [Pelv]">0.05</weight-threshold>
		<weight-threshold bone="NPC L Thigh [LThg]">0.05</weight-threshold>
		<weight-threshold bone="NPC R Thigh [RThg]">0.05</weight-threshold>
		<weight-threshold bone="NPC L Butt">0.02</weight-threshold>
		<weight-threshold bone="NPC R Butt">0.02</weight-threshold>
		<weight-threshold bone="NPC L RearThigh">0.05</weight-threshold>
		<weight-threshold bone="NPC R RearThigh">0.05</weight-threshold>
	</per-vertex-shape>
""")
    L.append(' <!-- dynamic -->\n')
    L.append('\t<per-triangle-shape name="%s">\n' % PROXY_NAME)
    L.append("""		<margin>0.3</margin>
		<penetration>-0.1</penetration>
		<shared>private</shared>
		<tag>skirt</tag>
		<can-collide-with-tag>Thigh</can-collide-with-tag>
		<can-collide-with-tag>Calves</can-collide-with-tag>
""")
    if T['butt']:
        L.append('\t\t<can-collide-with-tag>Butt</can-collide-with-tag>\n')
    L.append('\t\t<no-collide-with-tag>skirt</no-collide-with-tag>\n')
    for r, thr in ((2, "0.5"), (3, "0.4"), (4, "0.4")):
        for c in COLUMNS:
            L.append('\t\t<weight-threshold bone="%s">%s</weight-threshold>\n' % (sk_name(c, r), thr))
    L.append('\t</per-triangle-shape>\n</system>\n')
    return ''.join(L)

if __name__ == '__main__':
    xml = build()
    os.makedirs(OUT_DIR, exist_ok=True)
    p = os.path.join(OUT_DIR, 'MagicPariahSkirtHDT.xml')
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(xml)
    import xml.dom.minidom as md
    # the MM style puts bare words (SKIRT / SKIRT VERTICAL) between elements; FSMP ignores text
    # nodes, but check the element structure parses.
    md.parseString(xml.encode('utf-8'))
    print('wrote', p, len(xml), 'chars; bones', xml.count('<bone name='), 'constraints', xml.count('<generic-constraint bodyA='),
          'shapes', xml.count('-shape name='))
    if '--install' in sys.argv:
        for live in LIVE:
            bak = live + '.' + BAK_TAG
            if not os.path.exists(bak):
                shutil.copy2(live, bak)
            shutil.copy2(p, live)
            print('installed ->', live)
