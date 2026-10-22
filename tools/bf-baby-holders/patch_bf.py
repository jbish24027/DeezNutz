"""Authoria: let a BF baby item held by a registered holder (Kaidan, a crib)
still count as the player's. Re-run against fresh BF sources after a BF update:
    python -I patch_bf.py <BF Source\\Scripts dir> <out dir>
"""
import os, sys

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)

HELPERS = r'''
; Authoria: the player can hand her baby item to a holder (Kaidan, a crib).
; Holders are ObjectReferences kept in the global StorageUtil list
; "Authoria.BabyHolders"; a baby any of them holds still counts as hers.
int function BabyHeldByHolders(Form armBase) global
	int total = 0
	int n = StorageUtil.FormListCount(none, "Authoria.BabyHolders")
	while n > 0
		n -= 1
		ObjectReference h = StorageUtil.FormListGet(none, "Authoria.BabyHolders", n) as ObjectReference
		if h
			total += h.GetItemCount(armBase)
		endif
	endwhile
	return total
endFunction

; How many of this baby item the actor has, counting holders for the player.
int function BabyItemCount(actor Carrier, Form armBase) global
	if !Carrier || !armBase
		return 0
	endif
	int c = Carrier.GetItemCount(armBase)
	if Carrier == Game.GetPlayer()
		c += BabyHeldByHolders(armBase)
	endif
	return c
endFunction

; Take one of this baby item back from whichever holder has it.
bool function RemoveBabyFromHolders(Form armBase) global
	int n = StorageUtil.FormListCount(none, "Authoria.BabyHolders")
	while n > 0
		n -= 1
		ObjectReference h = StorageUtil.FormListGet(none, "Authoria.BabyHolders", n) as ObjectReference
		if h && h.GetItemCount(armBase) > 0
			Actor a = h as Actor
			if a
				a.UnequipItem(armBase, false, true)
			endif
			h.RemoveItem(armBase, 1, true)
			return true
		endif
	endwhile
	return false
endFunction
'''

def edit(name, pairs, append=None):
    raw = open(os.path.join(src, name), 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    s = raw.decode('utf-8-sig')
    for a, b in pairs:
        if s.count(a) != 1:
            sys.exit(f'{name}: expected 1 match, found {s.count(a)}: {a!r}')
        s = s.replace(a, b)
    if append:
        s = s.rstrip('\r\n') + '\r\n' + append.replace('\r\n', '\n').replace('\n', '\r\n')
    data = s.encode('utf-8')
    open(os.path.join(out, name), 'wb').write((b'\xef\xbb\xbf' if bom else b'') + data)
    print('patched', name)

edit('FWUtility.psc', [
    ('\t\t\tif rank > Carrier.GetItemCount(armBase)\r\n',
     '\t\t\tif rank > BabyItemCount(Carrier, armBase)\r\n'),
], append=HELPERS)

edit('FWAbilityBeeingFemale.psc', [
    ('\t\t\tif childArmor && PlayerRef.GetItemCount(childArmor) > 0\r\n',
     '\t\t\tif childArmor && FWUtility.BabyItemCount(PlayerRef, childArmor) > 0\r\n'),
    ('\t\t\tmother.UnequipItem(arm)\r\n\t\t\tmother.RemoveItem(arm, 1, true)\r\n',
     '\t\t\tif mother.GetItemCount(arm) > 0\r\n'
     '\t\t\t\tmother.UnequipItem(arm)\r\n\t\t\t\tmother.RemoveItem(arm, 1, true)\r\n'
     '\t\t\telse\r\n\t\t\t\tFWUtility.RemoveBabyFromHolders(arm)\r\n\t\t\tendif\r\n'),
])

edit('FWSystem.psc', [
    ('\t\t\t\telseif (frm as Armor) && PlayerRef.GetItemCount(frm) > 0\r\n',
     '\t\t\t\telseif (frm as Armor) && FWUtility.BabyItemCount(PlayerRef, frm) > 0\r\n'),
])

edit('FWSystemConfig.psc', [
    ('\t\t\tif babyItem && PlayerRef.GetItemCount(babyItem) > 0\r\n',
     '\t\t\tif babyItem && FWUtility.BabyItemCount(PlayerRef, babyItem) > 0\r\n'),
])
