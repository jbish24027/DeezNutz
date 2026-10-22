Scriptname _W_QuestScript extends Quest  

GlobalVariable Property _W_Global_ChanceInjury Auto
GlobalVariable Property _W_Global_ChanceArmLeft Auto
GlobalVariable Property _W_Global_ChanceArmRight Auto
GlobalVariable Property _W_Global_ChanceHead Auto
GlobalVariable Property _W_Global_ChanceLegLeft Auto
GlobalVariable Property _W_Global_ChanceLegRight Auto
GlobalVariable Property _W_Global_ChanceTorso Auto

GlobalVariable Property _W_Global_ArmorOffset Auto
GlobalVariable Property _W_Global_MaxInjury Auto
GlobalVariable Property _W_Global_MinSpeed Auto
GlobalVariable Property _W_Global_SpeedBuff Auto
GlobalVariable Property _W_Global_UpdateInterval Auto

GlobalVariable Property _W_GlobalBrok_ChanceInjury Auto
GlobalVariable Property _W_GlobalBruis_ChanceInjury Auto
GlobalVariable Property _W_GlobalCut_ChanceInjury Auto
GlobalVariable Property _W_GlobalCut_ChanceInfection Auto
GlobalVariable Property _W_GlobalConc_ChanceInjury Auto

GlobalVariable Property _W_GlobalBrok_TimeReq Auto
GlobalVariable Property _W_GlobalBruis_TimeReq Auto
GlobalVariable Property _W_GlobalConc_TimeReq Auto
GlobalVariable Property _W_GlobalCut_TimeReq Auto

GlobalVariable Property ldiLastHitBodyPartGlobal Auto
GlobalVariable Property ldiDisableAdditinalArmorSlotsGlobal Auto

FormList Property _W_ListInjuriesBrok Auto
FormList Property _W_ListInjuriesBruis Auto
FormList Property _W_ListInjuriesConcHead Auto
FormList Property _W_ListInjuriesCut Auto
FormList Property _W_ListInjuriesCutDesc Auto
FormList Property _W_ListInfections Auto

FormList Property _W_ListKeywordsInjuryBrok Auto
FormList Property _W_ListKeywordsInjuryBruis Auto
FormList Property _W_ListKeywordsInjuryConc Auto
FormList Property _W_ListKeywordsInjuryCut Auto

FormList Property _W_ListMsgBrok Auto
FormList Property _W_ListMsgBruis Auto
FormList Property _W_ListMsgConc Auto
FormList Property _W_ListMsgCut Auto

FormList Property _W_ListMsgHealFailBrok Auto
FormList Property _W_ListMsgHealFailCut Auto
FormList Property _W_ListMsgHealSuccBrok Auto
FormList Property _W_ListMsgHealSuccBruis Auto
FormList Property _W_ListMsgHealSuccConc Auto
FormList Property _W_ListMsgHealSuccCut Auto
FormList Property _W_ListMsgHealFailInjury Auto
FormList Property _W_ListMsgHealSuccInjury Auto

Message Property _W_MsgTest1 Auto
Message Property _W_MsgTest2 Auto

Keyword Property _W_KeywordBrok Auto
Keyword Property _W_KeywordBruis Auto
Keyword Property _W_KeywordConc Auto
Keyword Property _W_KeywordCut Auto
Keyword Property _W_KeywordInfection Auto
Keyword Property _W_KeywordLaud Auto

FormList Property _W_ListGlobalInjuriesBrok Auto
FormList Property _W_ListGlobalInjuriesCut Auto
FormList Property _W_ListGlobalInjuriesCutInfection Auto
FormList Property _W_ListInjuriesCutInfection Auto

FormList Property _W_ListMiscAlcohol Auto
FormList Property _W_ListMiscBandage Auto
FormList Property _W_ListMiscBrace Auto
FormList Property _W_ListMiscCauterize Auto
FormList Property _W_ListMiscFire Auto
FormList Property _W_ListMiscPacking Auto
FormList Property _W_ListMiscStitching Auto
FormList Property _W_ListMiscTorch Auto

FormList Property _W_ListMsgCutBanDirty Auto
FormList Property _W_ListMsgTreatCut Auto
FormList Property _W_ListMsgTreatBrok Auto

Message Property _W_MsgTreat Auto
Message Property _W_MsgTreatCut Auto
Message Property _W_MsgTreatCutNoAlcohol Auto
Message Property _W_MsgTreatCutNoBandage Auto
Message Property _W_MsgTreatCutNoCauterize Auto
Message Property _W_MsgTreatCutNoPacking Auto
Message Property _W_MsgTreatCutNoStitching Auto
Message Property _W_MsgTreatBrok Auto
Message Property _W_MsgTreatBrokNoBrace Auto

int InfResistBan = 15
int InfResistPac = 25
int InfResistSti = 30
int InfResistCau = 50

Actor Property PlayerRef Auto
GlobalVariable Property GameDaysPassed Auto
Keyword Property ActorTypeCreature Auto
Keyword Property MagicArmorSpell Auto
Keyword Property MagicWard Auto

string WoundEvent = "WoundEvent"
string WoundHealEvent = "WoundHeal"
string WoundInfectEvent = "WoundInfect"
string WoundOpenEvent = "WoundOpen"

string InfectionEvent = "InfectionEvent"
string InfectionHealEvent = "InfectionHeal"
Spell Property _W_SpellInfection Auto

;BodyParts
;0=Head
;1=Torso
;2=Right Arm
;3=Left Arm
;4=Right Leg
;5=Left Leg

float [] LastHealBrok
float LastHealBrokHead = 0.0
float LastHealBrokTorso = 0.0
float LastHealBrokArmRight = 0.0
float LastHealBrokArmLeft = 0.0
float LastHealBrokLegRight = 0.0
float LastHealBrokLegLeft = 0.0

float [] LastHealBruis
float LastHealBruisHead = 0.0
float LastHealBruisTorso = 0.0
float LastHealBruisArmRight = 0.0
float LastHealBruisArmLeft = 0.0
float LastHealBruisLegRight = 0.0
float LastHealBruisLegLeft = 0.0

float LastHealConc = 0.0

float [] LastHealCut
float LastHealCutTorso = 0.0
float LastHealCutArmRight = 0.0
float LastHealCutArmLeft = 0.0
float LastHealCutLegRight = 0.0
float LastHealCutLegLeft = 0.0

Event OnInit()
	RegisterForUpdateGameTime(_W_Global_UpdateInterval.GetValue())
	
	LastHealBrok = new float[6]
	LastHealBrok[0] = LastHealBrokHead
	LastHealBrok[1] = LastHealBrokTorso
	LastHealBrok[2] = LastHealBrokArmRight
	LastHealBrok[3] = LastHealBrokArmLeft
	LastHealBrok[4] = LastHealBrokLegRight
	LastHealBrok[5] = LastHealBrokLegLeft
	
	LastHealBruis = new float[6]
	LastHealBruis[0] = LastHealBruisHead
	LastHealBruis[1] = LastHealBruisTorso
	LastHealBruis[2] = LastHealBruisArmRight
	LastHealBruis[3] = LastHealBruisArmLeft
	LastHealBruis[4] = LastHealBruisLegRight
	LastHealBruis[5] = LastHealBruisLegLeft
	
	LastHealCut = new float[6]
	LastHealCut[1] = LastHealCutTorso
	LastHealCut[2] = LastHealCutArmRight
	LastHealCut[3] = LastHealCutArmLeft
	LastHealCut[4] = LastHealCutLegRight
	LastHealCut[5] = LastHealCutLegLeft
endEvent

Event OnUpdateGameTime()
	if(PlayerRef.HasMagicEffectWithKeyword(_W_KeywordBrok))
		int BodyPart = 0
		while(BodyPart <= 5)
			Keyword InjuryKeyword = _W_ListKeywordsInjuryBrok.GetAt(BodyPart) as Keyword
			if(PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
				float TimeReq = GetAdjustedTime(_W_GlobalBrok_TimeReq.GetValue())
				float TimePas = GameDaysPassed.GetValue() - LastHealBrok[BodyPart]
				Debug.Trace("[Wounds] Broken Bones Update, Body Part:" + BodyPart + ", " + TimePas + "/" + TimeReq)
				
				if(TimePas > TimeReq)
					LastHealBrok[BodyPart] = GameDaysPassed.GetValue()
					FormList InjuryList = _W_ListInjuriesBrok.GetAt(BodyPart) as FormList
					GlobalVariable BracedGlobal =  (_W_ListGlobalInjuriesBrok.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable
					bool HealFailed = false

					int Rank = InjuryList.GetSize() - 1
					while(!HealFailed && Rank >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
						Spell TempSpell = InjuryList.GetAt(Rank) as Spell
						if(PlayerRef.HasSpell(TempSpell))
							if(BracedGlobal.GetValue() == 1 || Rank < 2 || BodyPart == 0 || BodyPart == 1)
								LatentRemoveSpell(TempSpell, InjuryKeyword)
							else
								HealFailed = true
							endIf
						endIf
						Rank -= 1
					endWhile

					if(!HealFailed)
						if(Rank >= 0)
							PlayerRef.AddSpell(InjuryList.GetAt(Rank) as Spell, false)
						elseif(BracedGlobal.GetValue() >= 1)
							PlayerRef.AddItem(_W_ListMiscBrace.GetAt(BracedGlobal.GetValue() as int - 1))
						endIf
						(_W_ListMsgHealSuccBrok.GetAt(BodyPart) as Message).Show()
						SendWoundEvent(WoundHealEvent, 0, BodyPart, Rank)
					else
						(_W_ListMsgHealFailBrok.GetAt(BodyPart) as Message).Show()
					endIf
				endIf
			endIf
			BodyPart += 1
		endWhile
	endIf
	if(PlayerRef.HasMagicEffectWithKeyword(_W_KeywordBruis))
		int BodyPart = 0
		while(BodyPart <= 5)
			Keyword InjuryKeyword = _W_ListKeywordsInjuryBruis.GetAt(BodyPart) as Keyword
			if(PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
				float TimeReq = GetAdjustedTime(_W_GlobalBruis_TimeReq.GetValue())
				float TimePas = GameDaysPassed.GetValue() - LastHealBruis[BodyPart]
				Debug.Trace("[Wounds] Bruises Update, Body Part:" + BodyPart + ", " + TimePas + "/" + TimeReq)
			
				if(TimePas > TimeReq)
					LastHealBruis[BodyPart] = GameDaysPassed.GetValue()
					FormList InjuryList = _W_ListInjuriesBruis.GetAt(BodyPart) as FormList
					int Rank = InjuryList.GetSize() - 1
					while(Rank >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
						Spell TempSpell = InjuryList.GetAt(Rank) as Spell
						if(PlayerRef.HasSpell(TempSpell))
							LatentRemoveSpell(TempSpell, InjuryKeyword)
						endIf
						Rank -= 1
					endWhile
					if(Rank >= 0)
						PlayerRef.AddSpell(InjuryList.GetAt(Rank) as Spell, false)
					endIf
					(_W_ListMsgHealSuccBruis.GetAt(BodyPart) as Message).Show()
					SendWoundEvent(WoundHealEvent, 1, BodyPart, Rank)
				endIf
			endIf
			BodyPart += 1
		endWhile
	endIf
	if(PlayerRef.HasMagicEffectWithKeyword(_W_KeywordConc))
		float TimeReq = GetAdjustedTime(_W_GlobalConc_TimeReq.GetValue())
		float TimePas = GameDaysPassed.GetValue() - LastHealConc
		Debug.Trace("[Wounds] Concussions Update " + TimePas + "/" + TimeReq)
		
		if(TimePas > TimeReq)
			LastHealConc = GameDaysPassed.GetValue()
			Keyword InjuryKeyword = _W_ListKeywordsInjuryConc.GetAt(0) as Keyword
			if(PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
				int Rank = _W_ListInjuriesConcHead.GetSize() - 1
				while(Rank >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
					Spell TempSpell = _W_ListInjuriesConcHead.GetAt(Rank) as Spell
					if(PlayerRef.HasSpell(TempSpell))
						LatentRemoveSpell(TempSpell, InjuryKeyword)
					endIf
					Rank -= 1
				endWhile
				if(Rank >= 0)
					PlayerRef.AddSpell(_W_ListInjuriesConcHead.GetAt(Rank) as Spell, false)
				endIf
				(_W_ListMsgHealSuccConc.GetAt(0) as Message).Show()
				SendWoundEvent(WoundHealEvent, 2, 0, Rank)
			endIf
		endIf
	endIf
	if(PlayerRef.HasMagicEffectWithKeyword(_W_KeywordCut))
		int BodyPart = 1
		while(BodyPart <= 5)
			Keyword InjuryKeyword = _W_ListKeywordsInjuryCut.GetAt(BodyPart) as Keyword
			if(PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
				float TimeReq = GetAdjustedTime(_W_GlobalCut_TimeReq.GetValue())
				float TimePas = GameDaysPassed.GetValue() - LastHealCut[BodyPart]
				Debug.Trace("[Wounds] Cuts Update, Body Part:" + BodyPart + ", " + TimePas + "/" + TimeReq)
			
				if(TimePas > TimeReq)
					LastHealCut[BodyPart] = GameDaysPassed.GetValue()
					FormList InjuryList = _W_ListInjuriesCut.GetAt(BodyPart) as FormList
					GlobalVariable BanGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable
					GlobalVariable CauGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(1) as GlobalVariable
					GlobalVariable PacGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(2) as GlobalVariable
					GlobalVariable StiGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(3) as GlobalVariable
					GlobalVariable InfGlobal = _W_ListGlobalInjuriesCutInfection.GetAt(BodyPart - 1) as GlobalVariable
					bool HealFailed = false

					int Rank = InjuryList.GetSize() - 1
					while(!HealFailed && Rank >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
						Spell TempSpell = InjuryList.GetAt(Rank) as Spell
						if(PlayerRef.HasSpell(TempSpell))
							float InfSusc = GetInfection(Rank)
							InfSusc -= InfResistBan * BanGlobal.GetValue()
							InfSusc -= InfResistCau * CauGlobal.GetValue()
							InfSusc -= InfResistPac * PacGlobal.GetValue()
							InfSusc -= InfResistSti * StiGlobal.GetValue()

							Debug.Trace("[Wounds] Cuts Update, Injury Rank:" + Rank + " Infection Possibility:" + InfSusc)
							if(Utility.RandomInt() > InfSusc)
								LatentRemoveSpell(TempSpell, InjuryKeyword)
							else
								InfGlobal.Mod(1)
								HealFailed = true
								SendWoundEvent(WoundInfectEvent, 3, BodyPart, Rank)
							endIf
						endIf
						Rank -= 1
					endWhile

					if(BanGlobal.GetValue() > 1)
						BanGlobal.Mod(-1)
					endIf

					if(!HealFailed)
						if(Rank >= 0)
							PlayerRef.AddSpell(InjuryList.GetAt(Rank) as Spell, false)
						elseif(BanGlobal.GetValue() >= 1)
							PlayerRef.AddItem(_W_ListMiscBandage.GetAt(BanGlobal.GetValue() as int - 1))
						endIf
						if(Rank < 3)
							CauGlobal.SetValue(0)
						endIf
						(_W_ListMsgHealSuccCut.GetAt(BodyPart) as Message).Show()
						SendWoundEvent(WoundHealEvent, 3, BodyPart, Rank)
					else
						(_W_ListMsgHealFailCut.GetAt(BodyPart) as Message).Show()
					endIf

					if(Rank >= 0 && BanGlobal.GetValue() == 1)
						(_W_ListMsgCutBanDirty.GetAt(BodyPart) as Message).Show()
					endIf

					Spell DescSpell = _W_ListInjuriesCutDesc.GetAt(BodyPart - 1) as Spell
					Spell InfectionSpell = _W_ListInjuriesCutInfection.GetAt(BodyPart - 1) as Spell
					if(!HealFailed && Rank < 0)
						if(PlayerRef.HasSpell(DescSpell))
							PlayerRef.RemoveSpell(DescSpell)
						endIf
						if(PlayerRef.HasSpell(InfectionSpell))
							PlayerRef.RemoveSpell(InfectionSpell)
						endIf
						if(PlayerRef.HasSpell(_W_SpellInfection as Spell))
							PlayerRef.RemoveSpell(_W_SpellInfection as Spell)
						endIf
					endIf
				endIf
			endIf
			BodyPart += 1
		endWhile
	endIf
endEvent

Function TreatWounds()
	int Wound = _W_MsgTreat.Show()
	if(Wound == 0)
		int BodyPart = _W_MsgTreatBrok.Show()
		int Treatment = (_W_ListMsgTreatBrok.GetAt(BodyPart) as Message).Show()
		if(Treatment == 0)		;Brace
			GlobalVariable BracedGlobal =  (_W_ListGlobalInjuriesBrok.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable

			int Brace = FindAndRemove(_W_ListMiscBrace, 1)
			if(Brace < 0)
				_W_MsgTreatBrokNoBrace.Show()
			else
				BracedGlobal.SetValue(1)
			endIf
		elseif(Treatment == 1)	;Remove Brace
			GlobalVariable BracedGlobal =  (_W_ListGlobalInjuriesBrok.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable

			PlayerRef.AddItem(_W_ListMiscBrace.GetAt(0))
			BracedGlobal.SetValue(0)
		endIf
	elseif(Wound == 1)
		int BodyPart = _W_MsgTreatCut.Show()
		int Treatment = (_W_ListMsgTreatCut.GetAt(BodyPart) as Message).Show()
		if(Treatment == 0)		;Clean Wounds
			GlobalVariable InfGlobal = _W_ListGlobalInjuriesCutInfection.GetAt(BodyPart - 1) as GlobalVariable

			if(FindAndRemove(_W_ListMiscAlcohol, 1) < 0)
				_W_MsgTreatCutNoAlcohol.Show()
			else
				if(InfGlobal.GetValue() > 2)
					FormList InjuryList = _W_ListInjuriesCut.GetAt(BodyPart) as FormList
					Keyword InjuryKeyword = _W_ListKeywordsInjuryCut.GetAt(BodyPart) as Keyword
					int CurRank = 0
					while(CurRank < InjuryList.GetSize() && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
						Spell TempSpell = InjuryList.GetAt(CurRank) as Spell
						if(PlayerRef.HasSpell(TempSpell))
							LatentRemoveSpell(TempSpell, InjuryKeyword)
						endIf
						CurRank += 1
					endWhile
					PlayerRef.AddSpell(InjuryList.GetAt(GetMin(CurRank, InjuryList.GetSize() - 1) as int) as Spell, false)
					SendWoundEvent(WoundOpenEvent, 3, BodyPart, GetMin(CurRank, InjuryList.GetSize() - 1) as int)
				endIf
				InfGlobal.SetValue(0)
			endIf
		elseif(Treatment == 1)	;Bandage Wounds
			GlobalVariable BanGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable

			int Bandage = FindAndRemove(_W_ListMiscBandage, 1)
			if(Bandage < 0)
				_W_MsgTreatCutNoBandage.Show()
			else
				BanGlobal.SetValue(Bandage + 1)
			endIf
		elseif(Treatment == 2)	;Remove Bandage
			GlobalVariable BanGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable

			PlayerRef.AddItem(_W_ListMiscBandage.GetAt(BanGlobal.GetValue() as int - 1))
			BanGlobal.SetValue(0)
		elseif(Treatment == 3)	;Pack Wounds
			GlobalVariable PacGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(2) as GlobalVariable

			if(FindAndRemove(_W_ListMiscPacking, 3) < 0)
				_W_MsgTreatCutNoPacking.Show()
			else
				PacGlobal.SetValue(1)
			endIf
		elseif(Treatment == 4)	;Stitch Close Wounds
			GlobalVariable StiGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(3) as GlobalVariable
			GlobalVariable PacGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(2) as GlobalVariable

			if(!HasItemInList(_W_ListMiscStitching))
				_W_MsgTreatCutNoStitching.Show()
			else
				if(Utility.RandomInt() < 25)
					FindAndRemove(_W_ListMiscStitching, 1)
				endIf
				StiGlobal.SetValue(1)
				PacGlobal.SetValue(0)
			endIf
		elseif(Treatment == 5)	;Remove Stitching
			GlobalVariable StiGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(3) as GlobalVariable
			StiGlobal.SetValue(0)
		elseif(Treatment == 6)	;Cauterize
			GlobalVariable CauGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(1) as GlobalVariable
			GlobalVariable PacGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(2) as GlobalVariable

			if(!HasItemInList(_W_ListMiscTorch) && !HasSpellInList(_W_ListMiscFire) && FindAndRemove(_W_ListMiscCauterize, 1) < 0)
				_W_MsgTreatCutNoCauterize.Show()
			else
				CauGlobal.SetValue(1)
				PacGlobal.SetValue(0)
			endIf
		endIf
	endIf
endFunction

Function UpdateSpeed()
	float SpeedBuff = _W_Global_MinSpeed.GetValue() - PlayerRef.GetActorValue("SpeedMult")
	if(PlayerRef.HasMagicEffectWithKeyword(_W_KeywordLaud))
		SpeedBuff = GetMin(SpeedBuff + 20, 100)
	endIf
	_W_Global_SpeedBuff.SetValue(GetMin(GetMax(0, 1 + _W_Global_SpeedBuff.GetValue() + (SpeedBuff/10) as int), 10))
endFunction

Function ApplyHit(Actor akAggressor, Weapon akSource, bool abPowerAttack, bool abBashAttack, bool abHitBlocked)
	if((PlayerRef.HasMagicEffectWithKeyword(MagicArmorSpell) || PlayerRef.HasMagicEffectWithKeyword(MagicArmorSpell)) && Utility.RandomInt() < 75)
		Debug.Trace("[Wounds] Magic Spell Prevented Injury")
	elseif(Utility.RandomInt() < _W_Global_ChanceInjury.GetValue())
		float Damage = GetDamage(akAggressor, akSource)
		if(Damage > 0)
			int BodyPart = GetBodyPart(abHitBlocked, akAggressor)
			Armor BodyArmor = GetArmor(BodyPart)
			float Rating = GetRating(BodyArmor, BodyPart)
			float Protection = GetProtection(BodyArmor, abHitBlocked)
			bool IsWereBeast = PlayerRef.HasKeyword(ActorTypeCreature)
			bool IsCreature = akAggressor.HasKeyword(ActorTypeCreature)
			int Rank = (((5 * (Damage - Rating)/Damage)) - Protection) as int 
			if(IsWereBeast)
				Rank -= 3
			endIf
			if(abPowerAttack)
				Rank += 1
			endIf
			Rank = GetMin(Rank, _W_Global_MaxInjury.GetValue()) as int ; 3
			
			bool IsCut = Rank >= 0 && !abBashAttack && BodyPart != 0 && Protection < 2 && Utility.RandomInt() < _W_GlobalCut_ChanceInjury.GetValue() && (IsCreature || (akSource && (akSource.IsBattleaxe() || akSource.IsBow() || akSource.IsDagger() || akSource.IsGreatsword() || akSource.IsSword() || akSource.IsWarAxe())))
			bool IsBruised = Rank >= 0 && !IsCut && Utility.RandomInt() < _W_GlobalBruis_ChanceInjury.GetValue()
			bool IsBroken = Rank >= 0 && Utility.RandomInt() < _W_GlobalBrok_ChanceInjury.GetValue() && (IsCreature || (akSource && (akSource.IsBattleaxe() || akSource.IsGreatsword() || akSource.IsMace() || akSource.IsWarhammer())))
			bool IsConcussed = Rank >= 0 && BodyPart == 0 && Utility.RandomInt() < _W_GlobalConc_ChanceInjury.GetValue()
			
			if(IsBroken)
				int BrokenRank = GetMin(Rank, _W_Global_MaxInjury.GetValue()/1.5) as int
				AddInjury(BrokenRank, _W_ListKeywordsInjuryBrok.GetAt(BodyPart) as Keyword, _W_ListInjuriesBrok.GetAt(BodyPart) as FormList, _W_ListMsgBrok.GetAt(BodyPart) as Message, _W_ListGlobalInjuriesBrok.GetAt(BodyPart) as FormList)
				LastHealBrok[BodyPart] = GameDaysPassed.GetValue()
				SendWoundEvent(WoundOpenEvent, 0, BodyPart, BrokenRank)
			endIf
			if(IsBruised)
				int BruiseRank = GetMin(Rank, _W_Global_MaxInjury.GetValue() * 2) as int
				AddInjury(BruiseRank, _W_ListKeywordsInjuryBruis.GetAt(BodyPart) as Keyword, _W_ListInjuriesBruis.GetAt(BodyPart) as FormList, _W_ListMsgBruis.GetAt(BodyPart) as Message, None)
				LastHealBruis[BodyPart] = GameDaysPassed.GetValue()
				SendWoundEvent(WoundOpenEvent, 1, BodyPart, BruiseRank)
			endIf
			if(IsConcussed)
				int ConcussedRank = GetMin(Rank, _W_Global_MaxInjury.GetValue() * 1.5) as int
				AddInjury(ConcussedRank, _W_ListKeywordsInjuryConc.GetAt(BodyPart) as Keyword, _W_ListInjuriesConcHead, _W_ListMsgConc.GetAt(BodyPart) as Message, None)
				LastHealConc = GameDaysPassed.GetValue()
				SendWoundEvent(WoundOpenEvent, 2, BodyPart, ConcussedRank)
			endIf
			if(IsCut)
				int CutRank = GetMin(Rank, _W_Global_MaxInjury.GetValue()) as int
				AddInjury(CutRank, _W_ListKeywordsInjuryCut.GetAt(BodyPart) as Keyword, _W_ListInjuriesCut.GetAt(BodyPart) as FormList, _W_ListMsgCut.GetAt(BodyPart) as Message, _W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList)
				LastHealCut[BodyPart] = GameDaysPassed.GetValue()
				Spell DescSpell = _W_ListInjuriesCutDesc.GetAt(BodyPart - 1) as Spell
				if(!PlayerRef.HasSpell(DescSpell))
					PlayerRef.AddSpell(DescSpell, false)
					;Debug.Trace("Wounds: Adding Cut Description Spell")
				endIf
				Spell InfectionSpell = _W_ListInjuriesCutInfection.GetAt(BodyPart - 1) as Spell
				if(!PlayerRef.HasSpell(InfectionSpell))
					PlayerRef.AddSpell(InfectionSpell, false)
				endIf
				SendWoundEvent(WoundOpenEvent, 3, BodyPart, CutRank)
			endIf
			if(akSource)
				Debug.Trace("[Wounds] Hit by " + akAggressor.GetFormID() + ", Hit with " + akSource.GetFormID() + ", Body Part: " + BodyPart + ", Damage: " + Damage + ", Armor Rating:" + Rating + ", Protection:" + Protection + ", Player Werebeast:" + IsWereBeast + ", Enemy Creature:" + IsCreature + ", Injry Rank:" + Rank + ", IsBroken:" + IsBroken + ", IsBruised:" + IsBruised + ", IsConcussed:" + IsConcussed + ", IsCut:" + IsCut)
			else
				Debug.Trace("[Wounds] Hit by " + akAggressor.GetFormID() + ", Hit with " + None + ", Body Part: " + BodyPart + ", Damage: " + Damage + ", Armor Rating:" + Rating + ", Protection:" + Protection + ", Player Werebeast:" + IsWereBeast + ", Enemy Creature:" + IsCreature + ", Injry Rank:" + Rank + ", IsBroken:" + IsBroken + ", IsBruised:" + IsBruised + ", IsConcussed:" + IsConcussed + ", IsCut:" + IsCut)
			endIf
		endIf
	endIf
endFunction

Function AddInjury(int Rank, Keyword InjuryKeyword, FormList InjuryList, Message InjuryMsg, FormList GlobalList)
	int CurRank = 0
	;Debug.Trace("Wounds: Removing Other Injuries")
	while(CurRank < InjuryList.GetSize() - 1 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
		Spell TempSpell = InjuryList.GetAt(CurRank) as Spell
		if(PlayerRef.HasSpell(TempSpell))
			LatentRemoveSpell(TempSpell, InjuryKeyword)
			Utility.WaitMenuMode(0.1)
		endIf
		CurRank += 1
	endWhile
	if(GlobalList)
		int CurGlobal = 0
		while(CurGlobal < GlobalList.GetSize())
			GlobalVariable TreatGlobal = GlobalList.GetAt(CurGlobal) as GlobalVariable
			if(TreatGlobal)
				TreatGlobal.SetValue(0)
			endIf
			CurGlobal += 1
		endWhile
	endIf
	Rank += CurRank
	;Debug.Trace("Wounds: Injury Rank:" + Rank)
	Spell InjurySpell = InjuryList.GetAt(GetMin(Rank, InjuryList.GetSize() - 1) as int) as Spell
	;Debug.Trace("Wounds: Adding Injury " + InjurySpell + " to PlayerRef: " + PlayerRef + ", Game.GetPlayer: " + Game.GetPlayer())
	if(!PlayerRef.HasSpell(InjurySpell))
		PlayerRef.AddSpell(InjurySpell, false)
	endIf
	InjuryMsg.Show()
endFunction

Function RemoveInjuries(int Injury, int BodyPart)
	if(Injury == 0)		;Broken
		Keyword InjuryKeyword = _W_ListKeywordsInjuryBrok.GetAt(BodyPart) as Keyword
		FormList InjuryList = _W_ListInjuriesBrok.GetAt(BodyPart) as FormList
	
		int Index = InjuryList.GetSize() - 1
		while(Index >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
			Spell InjurySpell = InjuryList.GetAt(Index) as Spell
			if(PlayerRef.HasSpell(InjurySpell))
				LatentRemoveSpell(InjurySpell, InjuryKeyword)
			endIf
			Index -= 1
		endWhile
		GlobalVariable BracedGlobal =  (_W_ListGlobalInjuriesBrok.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable
		if(BracedGlobal.GetValue() >= 1)
			PlayerRef.AddItem(_W_ListMiscBrace.GetAt(BracedGlobal.GetValue() as int - 1))
			BracedGlobal.SetValue(0)
		endIf
		SendWoundEvent(WoundHealEvent, Injury, BodyPart, -1)
	elseif(Injury == 1)	;Bruises
		Keyword InjuryKeyword = _W_ListKeywordsInjuryBruis.GetAt(BodyPart) as Keyword
		FormList InjuryList = _W_ListInjuriesBruis.GetAt(BodyPart) as FormList
	
		int Index = InjuryList.GetSize() - 1
		while(Index >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
			Spell InjurySpell = InjuryList.GetAt(Index) as Spell
			if(PlayerRef.HasSpell(InjurySpell))
				LatentRemoveSpell(InjurySpell, InjuryKeyword)
			endIf
			Index -= 1
		endWhile
		SendWoundEvent(WoundHealEvent, Injury, BodyPart, -1)
	elseif(Injury == 2)	;Concussions
		Keyword InjuryKeyword = _W_KeywordConc
		FormList InjuryList = _W_ListInjuriesConcHead
	
		int Index = InjuryList.GetSize() - 1
		while(Index >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
			Spell InjurySpell = InjuryList.GetAt(Index) as Spell
			if(PlayerRef.HasSpell(InjurySpell))
				LatentRemoveSpell(InjurySpell, InjuryKeyword)
			endIf
			Index -= 1
		endWhile
		SendWoundEvent(WoundHealEvent, Injury, BodyPart, -1)
	elseif(Injury == 3)	;Cuts
		Keyword InjuryKeyword = _W_ListKeywordsInjuryCut.GetAt(BodyPart) as Keyword
		FormList InjuryList = _W_ListInjuriesCut.GetAt(BodyPart) as FormList
		
		int Index = InjuryList.GetSize() - 1
		while(Index >= 0 && PlayerRef.HasMagicEffectWithKeyword(InjuryKeyword))
			Spell InjurySpell = InjuryList.GetAt(Index) as Spell
			if(PlayerRef.HasSpell(InjurySpell))
				LatentRemoveSpell(InjurySpell, InjuryKeyword)
			endIf
			Index -= 1
		endWhile
		
		Spell DescSpell = _W_ListInjuriesCutDesc.GetAt(BodyPart - 1) as Spell
		
		if(PlayerRef.HasSpell(DescSpell))
			PlayerRef.RemoveSpell(DescSpell)
		endIf
		GlobalVariable BanGlobal = (_W_ListGlobalInjuriesCut.GetAt(BodyPart) as FormList).GetAt(0) as GlobalVariable
		if(BanGlobal.GetValue() >= 1)
			PlayerRef.AddItem(_W_ListMiscBandage.GetAt(BanGlobal.GetValue() as int - 1))
			BanGlobal.SetValue(0)
		endIf
		GlobalVariable InfGlobal = _W_ListGlobalInjuriesCutInfection.GetAt(BodyPart - 1) as GlobalVariable
		if(InfGlobal)
			InfGlobal.SetValue(0)
		endIf
		Spell InfectionSpell = _W_ListInjuriesCutInfection.GetAt(BodyPart - 1) as Spell
		if(InfectionSpell && PlayerRef.HasSpell(InfectionSpell))
			PlayerRef.RemoveSpell(InfectionSpell)
		endIf
		if(PlayerRef.HasSpell(_W_SpellInfection as Spell))
			PlayerRef.RemoveSpell(_W_SpellInfection as Spell)
		endIf
		SendWoundEvent(WoundHealEvent, Injury, BodyPart, -1)
	endIf
endFunction

Function RemoveInfections(int Injury, int BodyPart)
	int Part = 1
	while(Part <= 5)
		GlobalVariable InfGlobal = _W_ListGlobalInjuriesCutInfection.GetAt(Part - 1) as GlobalVariable
		if(InfGlobal)
			InfGlobal.SetValue(0)
		endIf
		Spell InfectionSpell = _W_ListInjuriesCutInfection.GetAt(Part - 1) as Spell
		if(InfectionSpell && PlayerRef.HasSpell(InfectionSpell))
			PlayerRef.RemoveSpell(InfectionSpell)
		endIf
		Part += 1
	endWhile
	if(PlayerRef.HasSpell(_W_SpellInfection as Spell))
		PlayerRef.RemoveSpell(_W_SpellInfection as Spell)
	endIf
	SendWoundEvent(WoundHealEvent, Injury, BodyPart, -1)
endFunction

int Function GetBodyPart(bool abHitBlocked, Actor akAggressor)
	if(abHitBlocked)
		if(PlayerRef.GetEquippedShield())
			return 3
		else
			float Choice = Utility.RandomFloat(0.0, _W_Global_ChanceArmLeft.GetValue() + _W_Global_ChanceArmRight.GetValue())
			if(Choice < _W_Global_ChanceArmLeft.GetValue())
				return 3
			else
				return 2
			endIf
		endIf
	else
		Int BodyPart = ldiLastHitBodyPartGlobal.GetValueInt()
		ldiLastHitBodyPartGlobal.SetValueInt(-1)
		If (BodyPart >= 0)
			return BodyPart
		EndIf

		float ChanceArmLeft = _W_Global_ChanceArmLeft.GetValue()
		float ChanceArmRight = _W_Global_ChanceArmRight.GetValue()
		float ChanceHead = _W_Global_ChanceHead.GetValue()
		float ChanceLegLeft = _W_Global_ChanceLegLeft.GetValue()
		float ChanceLegRight = _W_Global_ChanceLegRight.GetValue()
		float ChanceTorso = _W_Global_ChanceTorso.GetValue()

		float AttackAngle = PlayerRef.getAngleZ() - akAggressor.getAngleZ()
		If (AttackAngle < 0.0)
			AttackAngle = 360.0 + AttackAngle
		EndIf

		If (AttackAngle >= 30.0 && AttackAngle <= 150.0)
			ChanceArmLeft = 0.0
			ChanceLegLeft = 0.0
		ElseIf (AttackAngle >= 210.0 && AttackAngle <= 330.0)
			ChanceArmRight = 0.0
			ChanceLegRight = 0.0
		EndIf

		;String ChancesDebug
		;ChancesDebug += "Left Arm: " + ChanceArmLeft + "\n"
		;ChancesDebug += "Left Leg: " + ChanceLegLeft + "\n"
		;ChancesDebug += "Right Arm: " + ChanceArmRight + "\n"
		;ChancesDebug += "Right Leg: " + ChanceLegRight + "\n"
		;ChancesDebug += "Torso: " + ChanceTorso + "\n"
		;ChancesDebug += "Head: " + ChanceHead + "\n\n"
		;ChancesDebug += "Player's height: " + PlayerRef.getHeight() + "\n"
		;ChancesDebug += "Attacker's height: " + akAggressor.getHeight() + "\n"
		;Debug.MessageBox(ChancesDebug)

		float Choice = Utility.RandomFloat(0.0, ChanceArmLeft + ChanceArmRight + ChanceHead + ChanceLegLeft + ChanceLegRight + ChanceTorso)
		if(Choice < ChanceArmLeft)
			return 3
		elseif(Choice < ChanceArmLeft + ChanceArmRight)
			return 2
		elseif(Choice < ChanceArmLeft + ChanceArmRight + ChanceHead)
			return 0
		elseif(Choice < ChanceArmLeft + ChanceArmRight + ChanceHead + ChanceLegLeft)
			return 5
		elseif(Choice < ChanceArmLeft + ChanceArmRight + ChanceHead + ChanceLegLeft + ChanceLegRight)
			return 4
		else
			return 1
		endIf
	endIf
endFunction

float Function GetDamage(Actor akAggressor, Weapon akSource)
	if(akSource && akSource.GetBaseDamage() > 0)
		return akSource.GetBaseDamage()
	else
		return akAggressor.GetActorValue("UnarmedDamage")
	endIf
endFunction

Armor Function GetArmor(int BodyPart)
	Armor BodyArmor = None
	if(BodyPart == 0)						;Head
		BodyArmor = PlayerRef.GetWornForm(0x00000001) as Armor
		if(!BodyArmor)
			BodyArmor = PlayerRef.GetWornForm(0x00000002) as Armor
		endIf
		if(!BodyArmor)
			BodyArmor = PlayerRef.GetWornForm(0x00000800) as Armor
		endIf
		if(!BodyArmor)
			BodyArmor = PlayerRef.GetWornForm(0x00001000) as Armor
		endIf
	elseif(BodyPart == 1)					;Torso
		BodyArmor = PlayerRef.GetWornForm(0x00000004) as Armor
	elseif(BodyPart == 2 || BodyPart == 3)	;Arms
		BodyArmor = PlayerRef.GetWornForm(0x00000008) as Armor
	elseif(BodyPart == 4 || BodyPart == 5)	;Legs
		BodyArmor = PlayerRef.GetWornForm(0x00000080) as Armor
	endIf

	If (!BodyArmor && ldiDisableAdditinalArmorSlotsGlobal.GetValueInt() == 0)
		; Additional armor slots
		; See https://www.creationkit.com/index.php?title=Slot_Masks_-_Armor
		Armor AdditionalArmor = None
		if(BodyPart == 0) ;Head
			
		elseif(BodyPart == 1) ;Torso
			BodyArmor = PlayerRef.GetWornForm(0x00010000) as Armor
			If (!BodyArmor)
				BodyArmor = PlayerRef.GetWornForm(0x00080000) as Armor
				If (!BodyArmor)
					BodyArmor = PlayerRef.GetWornForm(0x00400000) as Armor
					If (!BodyArmor)
						BodyArmor = PlayerRef.GetWornForm(0x04000000) as Armor
						If (!BodyArmor)
							BodyArmor = PlayerRef.GetWornForm(0x00080000) as Armor
						EndIf
					EndIf
				EndIf
			EndIf
		elseif(BodyPart == 4 || BodyPart == 5) ;Legs
			BodyArmor = PlayerRef.GetWornForm(0x00800000) as Armor
		elseif(BodyPart == 2) ;Right Arm
			BodyArmor = PlayerRef.GetWornForm(0x08000000) as Armor
		elseif(BodyPart == 3) ;Left Arm
			BodyArmor = PlayerRef.GetWornForm(0x10000000) as Armor
			If (!BodyArmor)
				BodyArmor = PlayerRef.GetWornForm(0x00040000) as Armor
			EndIf
		endIf
	EndIf

	return BodyArmor
endFunction

float Function GetRating(Armor BodyArmor, int BodyPart)
	float Rating = 0.0
	if(BodyArmor)
		Rating += BodyArmor.GetArmorRating()
	endIf	
	if(BodyPart == 0)			;Head
		Rating += 0.2 * PlayerRef.GetActorValue("DamageResist")
	elseif(BodyPart != 1)		;Limbs
		Rating += 0.125 * PlayerRef.GetActorValue("DamageResist")
	else						;Torso
		Rating += 0.3 * PlayerRef.GetActorValue("DamageResist")
	endIf

	If (ldiDisableAdditinalArmorSlotsGlobal.GetValueInt() == 0)
		; Additional armor slots
		; See https://www.creationkit.com/index.php?title=Slot_Masks_-_Armor
		Armor AdditionalArmor = None
		if(BodyPart == 0) ;Head
			
		elseif(BodyPart == 1) ;Torso
			AdditionalArmor = PlayerRef.GetWornForm(0x00010000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			AdditionalArmor = PlayerRef.GetWornForm(0x00080000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			AdditionalArmor = PlayerRef.GetWornForm(0x00400000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			AdditionalArmor = PlayerRef.GetWornForm(0x04000000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			AdditionalArmor = PlayerRef.GetWornForm(0x00080000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			;Debug.MessageBox(Rating)
		elseif(BodyPart == 4 || BodyPart == 5) ;Legs
			AdditionalArmor = PlayerRef.GetWornForm(0x00800000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
		elseif(BodyPart == 2) ;Right Arm
			AdditionalArmor = PlayerRef.GetWornForm(0x08000000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
		elseif(BodyPart == 3) ;Left Arm
			AdditionalArmor = PlayerRef.GetWornForm(0x10000000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
			AdditionalArmor = PlayerRef.GetWornForm(0x00040000) as Armor
			If (AdditionalArmor)
				Rating += AdditionalArmor.GetArmorRating()
			EndIf
		endIf
	EndIf

	return (Rating + _W_Global_ArmorOffset.GetValue()) * GetMax(0.25, Math.Sqrt(PlayerRef.GetActorValuePercentage("Stamina") * PlayerRef.GetActorValuePercentage("Magicka")))
endFunction

int Function GetProtection(Armor BodyArmor, bool abHitBlocked)
	int Protection = 0
	if(BodyArmor)
		if(BodyArmor.IsHeavyArmor())
			Protection += 2
		elseIf(BodyArmor.IsLightArmor())
			Protection += 1
		endIf
	endIf
	if(abHitBlocked)
		if(PlayerRef.GetEquippedShield())
			Protection += 2
		else
			Protection += 1
		endIf
	endIf
	return Protection
endFunction

int Function FindAndRemove(FormList ItemList, int Count)
	int Index = ItemList.GetSize() - 1
	while(Index >= 0)
		int ItemCount = PlayerRef.GetItemCount(ItemList.GetAt(Index))
		if(ItemCount >= Count)
			PlayerRef.RemoveItem(ItemList.GetAt(Index), Count)
			return Index
		endIf
		Index -= 1
	endWhile
	return -1
endFunction

bool Function HasItemInList(FormList ItemList)
	int Index = ItemList.GetSize() - 1
	while(Index >= 0)
		if(PlayerRef.GetItemCount(ItemList.GetAt(Index)) > 0)
			return True
		endIf
		Index -= 1
	endWhile
	return false
endFunction

bool Function HasSpellInList(FormList SpellList)
	int Index = SpellList.GetSize() - 1
	while(Index >= 0)
		if(PlayerRef.HasSpell(SpellList.GetAt(Index)))
			return True
		endIf
		Index -= 1
	endWhile
	return false
endFunction

float Function GetAdjustedTime(float Time)
	Time = Time/Math.Pow(GetMax(0.5, (PlayerRef.GetActorValue("DiseaseResist") + 100.0)/100.0), 0.5)
	Time = Time/Math.Pow(GetMax(0.5, (PlayerRef.GetActorValue("PoisonResist") + 100.0)/100.0), 0.5)
	Time = Time/GetMax(0.5, (PlayerRef.GetActorValue("HealRate") + 100.0)/100.0)
	Time = Time/GetMax(0.5, PlayerRef.GetActorValue("HealRateMult")/100.0)
	return Time
endFunction

float Function GetInfection(int Rank)
	float Inf = _W_GlobalCut_ChanceInfection.GetValue() * (Rank/3.0)
	Inf = Inf/GetMax(0.5, (PlayerRef.GetActorValue("DiseaseResist") + 100.0)/100.0)
	Inf = Inf/GetMax(0.5, (PlayerRef.GetActorValue("PoisonResist") + 100.0)/100.0)
	Inf = GetMin(Inf, 175)
	return Inf
endFunction

Function SendWoundEvent(String EventName, int WoundType, int BodyPart, int WoundRank)
	int WoundValues = (100 * WoundType) + (10 * BodyPart) + (WoundRank)
	SendModEvent(WoundEvent, EventName)
endFunction

Function SendInfectionEvent(String EventName, int WoundType, int BodyPart, int WoundRank)
	int WoundValues = (100 * WoundType) + (10 * BodyPart) + (WoundRank)
	SendModEvent(InfectionEvent, EventName)
endFunction

Function LatentRemoveSpell(Spell ToRemove, Keyword EffectKeyword)
	PlayerRef.RemoveSpell(ToRemove)
	int TryCount = 100
	while(TryCount > 0 && PlayerRef.HasMagicEffectWithKeyword(EffectKeyword))
		TryCount -= 1
		Utility.WaitMenuMode(0.01)
	endWhile
endFunction

float Function GetMax(float val1, float val2)
	if(val1 > val2)
		return val1
	else
		return val2
	endIf
endFunction

float Function GetMin(float val1, float val2)
	if(val1 < val2)
		return val1
	else
		return val2
	endIf
endFunction
