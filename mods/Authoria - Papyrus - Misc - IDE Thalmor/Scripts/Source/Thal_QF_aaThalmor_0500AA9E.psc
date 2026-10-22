;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 3
Scriptname Thal_QF_aaThalmor_0500AA9E Extends Quest Hidden

;BEGIN ALIAS PROPERTY Valmir
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Valmir Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Igmund
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Igmund Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Shavari
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Shavari Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Player
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Player Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY JdatharrReal
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_JdatharrReal Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Ondolemar
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Ondolemar Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Jdatharr
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Jdatharr Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Elenwen
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Elenwen Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Estormo
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Estormo Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Rulindil
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Rulindil Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY SoldierForelhost
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_SoldierForelhost Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY xMarkerVoice
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_xMarkerVoice Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Gissur
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Gissur Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Lorcalin
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Lorcalin Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Ancano
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Ancano Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Tullius
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Tullius Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY MarkarthThrone
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_MarkarthThrone Auto
;END ALIAS PROPERTY

;BEGIN FRAGMENT Fragment_0
Function Fragment_0()
;BEGIN CODE
Actor RulindilRef = Alias_Rulindil.GetActorRef()
Actor LorcalinRef = Alias_Lorcalin.GetActorRef()
Actor ShavariRef = Alias_Shavari.GetActorRef()
Actor GissurRef = Alias_Gissur.GetActorRef()
Actor JdatharrRealRef = Alias_JdatharrReal.GetActorRef()
Actor JdatharrRef = Alias_Jdatharr.GetActorRef()
Actor EstormoRef = Alias_Estormo.GetActorRef()
Actor AncanoRef = Alias_Ancano.GetActorRef()

if MQ201.GetStage() < 100 && RulindilRef
RulindilRef.Enable()
RulindilRef.MoveTo(ThalmorHQ)
RulindilRef.EvaluatePackage()
endif

if SolitudeFreeform07.GetStage() < 10 && LorcalinRef
LorcalinRef.Enable()
LorcalinRef.MoveTo(ThalmorHQ)
LorcalinRef.RemoveFromFaction(WePlayerEnemy)
LorcalinRef.SetAV("Aggression", 0)
LorcalinRef.EvaluatePackage()
endif

if ShavariRef
if ShavariRef.IsDead() == 0
ShavariRef.Enable()
endif
if MQ202.GetStage() < 10 && ShavariRef.GetActorBase().IsEssential() == 0
ShavariRef.GetActorBase().SetEssential()
elseif MQ202.GetStage() >= 10 && ShavariRef.GetActorBase().IsEssential() == 1
ShavariRef.GetActorBase().SetEssential(0)
endif
endif

if GissurRef
if GissurRef.IsDead() == 0
GissurRef.Enable()
endif
if MQ201.GetStage() < 100 && GissurRef.GetActorBase().IsEssential() == 0
GissurRef.GetActorBase().SetEssential()
elseif MQ201.GetStage() >= 100 && GissurRef.GetActorBase().IsEssential() == 1
GissurRef.GetActorBase().SetEssential(0)
endif
endif

if JdatharrRealRef && ShavariRef && JdatharrRef && JdatharrRealRef.IsDead() == 0 && ShavariRef.IsDead() == 0
JdatharrRef.Enable()
JdatharrRef.MoveTo(ShavariRef)
endif

if MG06.GetStage() < 40 && EstormoRef && AncanoRef
EstormoRef.Enable()
EstormoRef.MoveTo(AncanoRef)
EstormoRef.GetActorBase().SetEssential()
EstormoRef.SetAV("Assistance", 2)
EstormoRef.SetRelationshipRank(AncanoRef, 2)
EstormoRef.EvaluatePackage()
endif
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

ObjectReference Property ThalmorHQ  Auto  

Quest Property MQ201  Auto  

Faction Property WEPlayerEnemy  Auto  

Quest Property SolitudeFreeform07  Auto  

Quest Property MQ202  Auto  

Quest Property MQ201Malborn  Auto  

Quest Property mg06  Auto  
