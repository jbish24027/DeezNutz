Scriptname BedRollForNPCs extends ActiveMagicEffect  


Formlist property SupportedBlankets auto
Formlist property SupportedBed auto
Formlist property SupportedBedroll auto
Formlist property OneSideBlanketDoubleBed auto
Formlist property SupportedNobleDouble auto
Formlist property SupportedNoblesingle auto
Formlist property SupportedDarkElfBeds Auto
Formlist property SupportedDarkElfDoubleBeds Auto
Formlist property SupportedDwemerfBeds Auto
Formlist property SupportedDwemerDoubleBeds Auto
Formlist property SupportedGreybeardBeds Auto
Formlist property SupportedOrcBeds Auto
Formlist property SupportedOrcDoubleBeds Auto
Formlist property SupportedUpperBeds Auto
Formlist property SupportedUpperDoubleBeds Auto
Formlist property SupportedCommonDoubleBeds Auto
Formlist property SupportedCampfire auto

ObjectReference BedRef
Weapon NoWeaponsInBed
Keyword Property ArmorHeavy Auto

ObjectReference DoubleBedsAndHowToFindThem
ObjectReference TheBedRoll
miscobject property bedroll auto
miscobject property BedBlanket auto
miscobject property DoubleBedBlanket_0 auto
miscobject property DoubleBedBlanket_1 auto
miscobject property bedroll_blanket_kid auto
miscobject property individualbed_kid_blanket auto
miscobject property individualnoblebed_kid_blanket auto
miscobject property IndividualNobleBed_blanket auto
miscobject property DoubleNobleBedBlanket_0 auto
miscobject property DoubleNobleBedBlanket_1 auto

miscobject property DoubleNobleBedBlanket_0_HA auto
miscobject property DoubleNobleBedBlanket_1_HA auto

miscobject property DoubleCommonBedBlanket_0_HA auto
miscobject property DoubleCommonBedBlanket_1_HA auto

miscobject property darkelf_kid_blanket auto
miscobject property Individualdarkelfbed_blanket auto
miscobject property DoubleDarkElfBedBlanket_0 auto
miscobject property DoubleDarkElfBedBlanket_1 auto

miscobject property DoubleDarkElfBedBlanket_0_HA auto
miscobject property DoubleDarkElfBedBlanket_1_HA auto

miscobject property individualdwemerbed_kid_blanket auto
miscobject property IndividualdwemerBed_blanket auto
miscobject property DoubledwemerBedBlanket_0 auto
miscobject property DoubledwemerBedBlanket_1 auto

miscobject property DoubledwemerBedBlanket_0_HA auto
miscobject property DoubledwemerBedBlanket_1_HA auto

miscobject property individualorcbed_kid_blanket auto
miscobject property IndividualorcBed_blanket auto
miscobject property DoubleorcBedBlanket_0 auto
miscobject property DoubleorcBedBlanket_1 auto

miscobject property DoubleorcBedBlanket_0_HA auto
miscobject property DoubleorcBedBlanket_1_HA auto

miscobject property individualupperbed_kid_blanket auto
miscobject property IndividualupperBed_blanket auto
miscobject property DoubleupperBedBlanket_0 auto
miscobject property DoubleupperBedBlanket_1 auto

miscobject property DoubleupperBedBlanket_0_HA auto
miscobject property DoubleupperBedBlanket_1_HA auto

miscobject property IndividualgreybeardBed_blanket auto
miscobject property BedRoll_Blanket_HA auto


;HA Variants;
miscobject property IndividualCommonBed_Blanket_HA auto
miscobject property IndividualNobleBed_blanket_HA auto
miscobject property Individualdarkelfbed_blanket_HA auto
miscobject property IndividualdwemerBed_blanket_HA auto
miscobject property IndividualorcBed_blanket_HA auto
miscobject property IndividualupperBed_blanket_HA auto
miscobject property IndividualgreybeardBed_blanket_HA auto
miscobject property CampfireBed auto

miscobject property IndividualCommonBed_Blanket_2 auto
miscobject property IndividualNobleBed_blanket_2 auto
miscobject property Individualdarkelfbed_blanket_2 auto
miscobject property IndividualdwemerBed_blanket_2 auto
miscobject property IndividualorcBed_blanket_2 auto
miscobject property IndividualupperBed_blanket_2 auto

float AngleTime
float Griega
float Equis
int attemptlimit 

Function OnEffectStart(Actor akTarget, Actor akCaster)

TheBedRoll = Game.FindClosestReferenceOfAnyTypeInList(SupportedBlankets, akTarget.GetPositionX(), akTarget.GetPositionY(), akTarget.GetPositionZ(), 75.0)
If TheBedRoll == None
;nothing, no proper bed found


else

	If TheBedRoll.IsDisabled()
attemptlimit = 0
		While TheBedRoll.IsDisabled() && attemptlimit < 10
		TheBedRoll = Game.FindRandomReferenceOfAnyTypeInList(SupportedBlankets, akTarget.GetPositionX(), akTarget.GetPositionY(), akTarget.GetPositionZ(), 75.0)
		attemptlimit = attemptlimit + 1
		endwhile
	endif

NoWeaponsInBed = aktarget.GetEquippedWeapon()
If NoWeaponsInBed != None
aktarget.unequipitem(NoWeaponsInBed, false, true)
EndIf
Form BedTypeForm = TheBedroll.getBaseObject()


if SupportedCampfire.HasForm(BedTypeForm)
Utility.wait(2.5)
	BedRef = TheBedRoll.PlaceAtMe(CampfireBed, 1, false, false)

elseif aktarget.WornHasKeyword(ArmorHeavy)

if SupportedBed.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualCommonBed_Blanket_HA, 1, false, false)

elseif SupportedBedroll.HasForm(BedTypeForm)
	BedRef= TheBedRoll.PlaceAtMe(BedRoll_Blanket_HA, 1, false, false)

elseif SupportedNobleSingle.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualNobleBed_blanket_HA, 1, false, false)

elseif SupportedDarkElfBeds.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualDarkElfBed_blanket_HA, 1, false, false)

elseif SupportedDwemerfBeds.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualDwemerBed_blanket_HA, 1, false, false)

elseif SupportedOrcBeds.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualORCBed_blanket_HA, 1, false, false)

elseif SupportedUpperBeds.HasForm(BedTypeForm)
	BedRef = TheBedRoll.PlaceAtMe(IndividualUPPERBed_blanket_HA, 1, false, false)

elseif SupportedGreybeardBeds.HasForm(TheBedRoll.GetBaseObject())
	BedRef = TheBedRoll.PlaceAtMe(IndividualGreybeardBed_blanket_HA, 1, false, false)


;;;;;;; HA DOUBLE BEDS START HERE ;;;;;;;

elseif SupportedCommonDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleCommonBedBlanket_1_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleCommonBedBlanket_0_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualCommonBed_Blanket_HA, 1, false, true)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif

elseif SupportedNobleDouble.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleNobleBedBlanket_1_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleNobleBedBlanket_0_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualnobleBed_blanket_HA, 1, false, true)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif

elseif SupportedUpperDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleUpperBedBlanket_1_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleUpperBedBlanket_0_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualupperBed_blanket_HA, 1, false, true)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif

elseif SupportedDarkElfDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDarkElfBedBlanket_0_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDarkElfBedBlanket_1_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualdarkelfBed_blanket_HA, 1, false, true)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif

elseif SupportedOrcDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleOrcBedBlanket_1_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleOrcBedBlanket_0_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualORCBed_blanket_HA, 1, false, true)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif

elseif SupportedDwemerDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDwemerBedBlanket_0_HA, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDwemerBedBlanket_1_HA, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualdwemerBed_blanket_HA, 1, false, false)
	AngleTime = aktarget.GetAngleZ()
		WeirdAngles()	
	BedRef.SetPosition(BedRef.GetPositionX() + Equis, BedRef.GetPositionY() + Griega, BedRef.GetPositionZ())
	BedRef.Enable()
	endif
endif





;;; LIGHT ARMOR+ KIDS START HERE ;;;;

elseif SupportedBedroll.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(bedroll_blanket_kid, 1, false, false)
	else
	BedRef= TheBedRoll.PlaceAtMe(Bedroll, 1, false, false)
	endif

elseif SupportedBed.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(individualbed_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(bedblanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualCommonBed_Blanket_2, 1, false, false)
endif
endif

elseif SupportedNobleSingle.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(individualnoblebed_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(IndividualNobleBed_blanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualNobleBed_blanket_2, 1, false, false)
endif
endif

elseif SupportedDarkElfBeds.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(darkelf_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(IndividualDarkElfBed_blanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualDarkElfBed_blanket_2, 1, false, false)
endif
endif

elseif SupportedDwemerfBeds.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(individualdwemerbed_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(IndividualDwemerBed_blanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualDwemerBed_blanket_2, 1, false, false)
endif
endif

elseif SupportedOrcBeds.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(individualORCbed_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(IndividualORCBed_blanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualORCBed_blanket_2, 1, false, false)
endif
endif

elseif SupportedUpperBeds.HasForm(BedTypeForm)
	If aktarget.IsChild()
	BedRef= TheBedRoll.PlaceAtMe(individualUPPERbed_kid_blanket, 1, false, false)
	else
Int Variation = Utility.RandomInt(1,3)
If Variation < 3
	BedRef = TheBedRoll.PlaceAtMe(IndividualUPPERBed_blanket, 1, false, false)
else
	BedRef = TheBedRoll.PlaceAtMe(IndividualUPPERBed_blanket_2, 1, false, false)
endif
endif

elseif SupportedGreybeardBeds.HasForm(TheBedRoll.GetBaseObject())
	BedRef = TheBedRoll.PlaceAtMe(IndividualGreybeardBed_blanket, 1, false, false)




;;;;;;;; LA DOUBLE BEDS START HERE ;;;;;;;;;

elseif SupportedCommonDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleBedBlanket_1, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleBedBlanket_0, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(BedBlanket, 1, false, false)
	endif

elseif SupportedNobleDouble.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleNobleBedBlanket_1, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleNobleBedBlanket_0, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualnobleBed_blanket, 1, false, false)
	endif

elseif SupportedUpperDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleUpperBedBlanket_1, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleUpperBedBlanket_0, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualupperBed_blanket, 1, false, false)
	endif

elseif SupportedDarkElfDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDarkElfBedBlanket_0, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDarkElfBedBlanket_1, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualdarkelfBed_blanket, 1, false, false)
	endif

elseif SupportedOrcDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleOrcBedBlanket_1, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleOrcBedBlanket_0, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualORCBed_blanket, 1, false, false)
	endif

elseif SupportedDwemerDoubleBeds.HasForm(BedTypeForm)

	If TheBedRoll.IsFurnitureMarkerInUse(0) && !TheBedRoll.IsFurnitureMarkerInUse(1)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDwemerBedBlanket_0, 1, false, false)

	elseif TheBedRoll.IsFurnitureMarkerInUse(1) && !TheBedRoll.IsFurnitureMarkerInUse(0)
	BedRef = TheBedRoll.PlaceAtMe(DoubleDwemerBedBlanket_1, 1, false, false)

	else 
	BedRef = aktarget.PlaceAtMe(IndividualdwemerBed_blanket, 1, false, false)
	endif
endif
endif
endfunction


Event OnEffectFinish(Actor akTarget, Actor akCaster)
	If NoWeaponsInBed == none
		;nothing
	else
	aktarget.equipitem(NoWeaponsInBed, false, true)
	endif


If BedRef && BedRef.Is3DLoaded()
BedRef.Disable()
BedRef.Setposition(-100, -100, -100)
BedRef.Delete()
BedRef = None
endif

EndEvent



Function WeirdAngles()

;The below is all thanks to the mysterious VictorF! Thank you for the following formula! You're amazing! May you always walk on warm sands.
; PS: My math teacher would be proud of you. I know I am!

Equis = math.sin(angletime) * 10
Griega = math.cos(angletime) * 10

endfunction
