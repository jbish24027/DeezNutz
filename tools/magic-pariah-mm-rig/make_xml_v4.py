"""FSMP xmls for Magic Pariah v4: Helga-style cloth on the skirt (psk_* grid, 14 x 7) and on both
sleeves (slvL_*/slvR_* grids, 8 x 4). Numbers are Fuse00's Helga_Dress.xml skirt values: light bones
(mass 0.13), high bone damping (0.75 / 0.85), gravity 0.7, zero-stiffness hinges with small angular
limits, and near-free horizontal tethers (+-2 units, +-1 rad) between neighbouring columns.

usage: python make_xml_v4.py [--install]   (writes skirt + top xml to scratch; --install copies them
       over the four live files with .bak-v3-20260906 backups)
"""
import os, shutil, sys
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\magic-pariah-mm-rig")
from graft import OUT_DIR
from build_v4 import SKIRT_COLS, SKIRT_ROWS_Z, SLEEVE_COLS
from make_xml import BODY_BONES as SKIRT_BODY_BONES

BAK = 'bak-v3-20260906'
MODS = r"C:\1. AUTHORIA\mods"
LIVE_SKIRT = [MODS + r"\Magic Pariah - Meadowlark Physics\meshes\clothes\magic pariah\MagicPariahSkirtHDT.xml",
              MODS + r"\Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah\magic pariah skirt HDT.xml"]
LIVE_TOP = [MODS + r"\Magic Pariah - Meadowlark Physics\meshes\clothes\magic pariah\MagicPariahTopHDT.xml",
            MODS + r"\Authoria - UBE Converter Output - Magic Pariah\meshes\!UBE\clothes\magic pariah\Magic Pariah Top.xml"]

TOP_BODY_BONES = [
    "NPC L Calf [LClf]", "NPC R Calf [RClf]", "NPC R Foot [Rft ]", "NPC L Foot [Lft ]", "NPC Head [Head]",
    "NPC L Clavicle [LClv]", "NPC R Clavicle [RClv]", "NPC L Forearm [LLar]", "NPC R Forearm [RLar]",
    "NPC L ForearmTwist1 [LLt1]", "NPC R ForearmTwist1 [RLt1]", "NPC L ForearmTwist2 [LLt2]", "NPC R ForearmTwist2 [RLt2]",
    "NPC L UpperArm [LUar]", "NPC R UpperArm [RUar]", "NPC L UpperarmTwist1 [LUt1]", "NPC R UpperarmTwist1 [RUt1]",
    "NPC L UpperarmTwist2 [LUt2]", "NPC R UpperarmTwist2 [RUt2]", "NPC Spine [Spn0]", "NPC Spine2 [Spn2]",
    "NPC Spine1 [Spn1]", "NPC Pelvis [Pelv]", "NPC Belly", "Belly", "NPC L Thigh [LThg]", "NPC R Thigh [RThg]",
    "NPC L FrontThigh", "NPC R FrontThigh", "NPC L RearCalf [LrClf]", "NPC R RearCalf [RrClf]", "NPC L RearThigh",
    "NPC R RearThigh", "NPC L Hand [LHnd]", "NPC R Hand [RHnd]", "NPC L PreBreast", "NPC R PreBreast",
    "NPC L Breast", "NPC R Breast", "NPC L Breast01", "NPC R Breast01", "L Breast00", "R Breast00", "L Breast01",
    "R Breast01", "L Breast02", "R Breast02", "L Breast03", "R Breast03", "L Breast04", "R Breast04",
    "NPC L PreButt", "NPC R PreButt", "NPC L Pussy01", "NPC R Pussy01", "NPC L Butt", "NPC R Butt",
    "NPC L Pussy02", "NPC R Pussy02", "Clitoral1", "NPC Anus Deep2", "RB Anus2", "RT Anus2", "LB Anus2",
    "LT Anus2", "VaginaB1", "VaginaDeep1",
]

HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="description.xsd">\n'

def bone_default(mass, inertia, lin_damp, ang_damp, gravity, roll, restit, margin_mult):
    return """	<bone-default>
		<mass>%s</mass>
		<inertia x="%s" y="%s" z="%s" />
		<centerOfMassTransform>
			<basis x="0" y="0" z="0" w="1" />
			<origin x="0" y="0" z="0" />
		</centerOfMassTransform>
		<linearDamping>%s</linearDamping>
		<angularDamping>%s</angularDamping>
		<gravity-factor>%s</gravity-factor>
		<friction>0</friction>
		<rollingFriction>%s</rollingFriction>
		<restitution>%s</restitution>
	</bone-default>
	<bone-default>
		<margin-multiplier>%s</margin-multiplier>
	</bone-default>
""" % (mass, inertia, inertia, inertia, lin_damp, ang_damp, gravity, roll, restit, margin_mult)

# per-row bone properties, Helga's skirt ladder (row 1 first)
ROW_PROPS = [(0.13, 1.8, 0.0, 1.0, 0.9), (0.13, 2.0, 0.1, 1.0, 0.8), (0.13, 2.1, 0.2, 1.0, 0.7), (0.13, 2.2, 0.3, 1.0, 0.6),
             (0.13, 2.3, 0.4, 1.0, 0.5), (0.13, 2.4, 0.7, 1.0, 0.5), (0.13, 2.5, 1.0, 0.5, 0.4), (0.13, 2.6, 1.0, 0.5, 0.3),
             (0.13, 2.7, 1.0, 0.6, 0.2)]

VERTICAL = """	<generic-constraint-default>
		<frameInB>
			<basis x="0" y="0" z="0" w="1" />
			<origin x="0" y="0" z="0" />
		</frameInB>
		<useLinearReferenceFrameA>false</useLinearReferenceFrameA>
		<linearLowerLimit x="0" y="0" z="0" />
		<linearUpperLimit x="0" y="0" z="0" />
		<angularLowerLimit x="-0.2" y="-0.3" z="-0.3" />
		<angularUpperLimit x="0.2" y="0.3" z="0.3" />
		<linearStiffness x="0" y="0" z="0" />
		<angularStiffness x="0" y="0" z="0" />
		<linearDamping x="0" y="0" z="0" />
		<angularDamping x="0" y="0" z="0" />
		<linearEquilibrium x="0" y="0" z="0" />
		<angularEquilibrium x="0" y="0" z="0" />
	</generic-constraint-default>
"""
HORIZONTAL = """	<generic-constraint-default>
		<frameInLerp>
			<translationLerp>0</translationLerp>
			<rotationLerp>0</rotationLerp>
		</frameInLerp>
		<linearLowerLimit x="-2" y="-2" z="-2" />
		<linearUpperLimit x="2" y="2" z="2" />
		<angularLowerLimit x="-1.0" y="-1.0" z="-1.0" />
		<angularUpperLimit x="1.0" y="1.0" z="1.0" />
		<linearStiffness x="0" y="0" z="0" />
		<angularStiffness x="0" y="0" z="0" />
	</generic-constraint-default>
"""

def grid_section(prefix, cols, nrows, comment):
    """bones (anchor row static, rows 1.. dynamic), vertical chains, horizontal rings."""
    name = lambda c, r: '%s_%s_%02d' % (prefix, c, r)
    L = ['<!-- %s: anchor row (static, rides the body bone) -->\n' % comment]
    for c in cols:
        L.append('\t<bone name="%s"/>\n' % name(c, 0))
    L.append('<!-- %s: cloth rows -->\n' % comment)
    for r in range(1, nrows):
        mass, inertia, roll, restit, mm = ROW_PROPS[min(r - 1, len(ROW_PROPS) - 1)]
        L.append(bone_default(mass, inertia, 0.75, 0.85, 0.7, roll, restit, mm))
        for c in cols:
            L.append('\t<bone name="%s"/>\n' % name(c, r))
    C = ['<!-- %s: vertical chains -->\n' % comment, VERTICAL, '\t<constraint-group>\n']
    for c in cols:
        for r in range(1, nrows):
            C.append('\t\t<generic-constraint bodyA="%s" bodyB="%s"/>\n' % (name(c, r), name(c, r - 1)))
    C.append('\t</constraint-group>\n')
    C += ['<!-- %s: horizontal tethers -->\n' % comment, HORIZONTAL, '\t<constraint-group>\n']
    ring = list(cols) + [cols[0]]
    for a, b in zip(ring[:-1], ring[1:]):
        for r in range(1, nrows):
            C.append('\t\t<generic-constraint bodyA="%s" bodyB="%s"/>\n' % (name(a, r), name(b, r)))
    C.append('\t</constraint-group>\n')
    dyn = [name(c, r) for r in range(1, nrows) for c in cols]
    return ''.join(L), ''.join(C), dyn


def skirt_xml():
    nrows = len(SKIRT_ROWS_Z)
    bones, cons, dyn = grid_section('psk', SKIRT_COLS, nrows, 'skirt')
    L = [HEAD, '<!-- Magic Pariah skirt, Authoria v4 (2026-09-06): Helga-style cloth grid, 14 columns x 7 rows,\n',
         '     numbers from Fuse00 Helga_Dress.xml. Generated by _tools\\magic-pariah-mm-rig\\make_xml_v4.py -->\n',
         '<!-- static body bones -->\n']
    for b in SKIRT_BODY_BONES:
        L.append('\t<bone name="%s"/>\n' % b)
    L.append(bones); L.append(cons)
    L.append("""<!-- colliders -->
	<per-vertex-shape name="CollThigh">
		<margin>0.8</margin>
		<penetration>0.2</penetration>
		<priority>100</priority>
		<shared>private</shared>
		<tag>Thigh</tag>
		<can-collide-with-tag>skirt</can-collide-with-tag>
		<weight-threshold bone="NPC R Thigh [RThg]">0.1</weight-threshold>
		<weight-threshold bone="NPC L Thigh [LThg]">0.1</weight-threshold>
	</per-vertex-shape>
	<per-vertex-shape name="CollCalves">
		<margin>1.7</margin>
		<penetration>1.1</penetration>
		<priority>100</priority>
		<shared>private</shared>
		<tag>Calves</tag>
		<can-collide-with-tag>skirt</can-collide-with-tag>
		<weight-threshold bone="NPC R Calf [RClf]">0.2</weight-threshold>
		<weight-threshold bone="NPC L Calf [LClf]">0.2</weight-threshold>
	</per-vertex-shape>
	<per-vertex-shape name="CollButt">
		<margin>1.2</margin>
		<penetration>0.3</penetration>
		<priority>100</priority>
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
	<per-triangle-shape name="MMSkirtProxy">
		<margin>0.3</margin>
		<penetration>-0.2</penetration>
		<shared>private</shared>
		<tag>skirt</tag>
		<can-collide-with-tag>Thigh</can-collide-with-tag>
		<can-collide-with-tag>Calves</can-collide-with-tag>
		<can-collide-with-tag>Butt</can-collide-with-tag>
		<no-collide-with-tag>skirt</no-collide-with-tag>
""")
    for b in dyn:
        L.append('\t\t<weight-threshold bone="%s">0.3</weight-threshold>\n' % b)
    L.append('\t</per-triangle-shape>\n</system>\n')
    return ''.join(L)


def top_xml():
    L = [HEAD, '<!-- Magic Pariah top, Authoria v4 (2026-09-06): Helga-style cloth grid on each sleeve, 8 columns x 4 rows\n',
         '     around the forearm, numbers from Fuse00 Helga_Dress.xml. Generated by make_xml_v4.py -->\n',
         '<!-- static body bones -->\n']
    for b in TOP_BODY_BONES:
        L.append('\t<bone name="%s"/>\n' % b)
    parts = [grid_section(prefix, SLEEVE_COLS, 5, label) for prefix, label in (('slvL', 'left sleeve'), ('slvR', 'right sleeve'))]
    # every anchor row (mass 0 = static, rides the forearm) MUST come before the first <bone-default>:
    # a <bone> declared after a mass>0 default becomes a free body and falls to the ground.
    for bones, cons, dyn in parts:
        L.append(bones[:bones.index('<bone-default>')].rstrip('\t'))
    for bones, cons, dyn in parts:
        L.append('\t' + bones[bones.index('<bone-default>'):])
    for bones, cons, dyn in parts:
        L.append(cons)
    L.append("""<!-- colliders -->
	<per-triangle-shape name="Cube">
		<margin>0.1</margin>
		<penetration>0.1</penetration>
		<priority>100</priority>
		<shared>private</shared>
		<tag>collide</tag>
		<can-collide-with-tag>sleeve</can-collide-with-tag>
	</per-triangle-shape>
	<per-triangle-shape name="Sleeves">
		<margin>0.1</margin>
		<penetration>0.1</penetration>
		<shared>private</shared>
		<tag>sleeve</tag>
		<can-collide-with-tag>collide</can-collide-with-tag>
		<no-collide-with-tag>sleeve</no-collide-with-tag>
	</per-triangle-shape>
</system>
""")
    return ''.join(L)


if __name__ == '__main__':
    import xml.dom.minidom as md
    os.makedirs(OUT_DIR, exist_ok=True)
    outs = {}
    for fn, text, live in (('MagicPariahSkirtHDT.v4.xml', skirt_xml(), LIVE_SKIRT), ('MagicPariahTopHDT.v4.xml', top_xml(), LIVE_TOP)):
        md.parseString(text.encode('utf-8'))
        p = os.path.join(OUT_DIR, fn)
        with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(text)
        print('wrote', p, len(text), 'chars; bones', text.count('<bone name='), 'constraints', text.count('<generic-constraint bodyA='), 'shapes', text.count('-shape name='))
        outs[p] = live
    if '--install' in sys.argv:
        for p, lives in outs.items():
            for live in lives:
                bak = live + '.' + BAK
                if not os.path.exists(bak):
                    shutil.copy2(live, bak)
                shutil.copy2(p, live)
                print('installed ->', live)
