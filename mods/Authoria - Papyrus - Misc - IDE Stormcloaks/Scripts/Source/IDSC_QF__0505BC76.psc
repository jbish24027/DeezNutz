;BEGIN FRAGMENT CODE - Do not edit anything between this and the end comment
;NEXT FRAGMENT INDEX 22
Scriptname IDSC_QF__0505BC76 Extends Quest Hidden

;BEGIN ALIAS PROPERTY NewLocation
;ALIAS PROPERTY TYPE LocationAlias
LocationAlias Property Alias_NewLocation Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Vidrald
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Vidrald Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Thalmor3
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Thalmor3 Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Thalmor2
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Thalmor2 Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Thalmor1
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Thalmor1 Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Player
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Player Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY OldLocation
;ALIAS PROPERTY TYPE LocationAlias
LocationAlias Property Alias_OldLocation Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Avulstein
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Avulstein Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Thorald
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Thorald Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY CenterMarker
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_CenterMarker Auto
;END ALIAS PROPERTY

;BEGIN ALIAS PROPERTY Geirlund
;ALIAS PROPERTY TYPE ReferenceAlias
ReferenceAlias Property Alias_Geirlund Auto
;END ALIAS PROPERTY

;BEGIN FRAGMENT Fragment_19
Function Fragment_19()
;BEGIN CODE
if CWObj.IsCompleted() == 0
Alias_Avulstein.GetActorRef().Enable()
Alias_Avulstein.GetActorRef().MoveTo(Alias_CenterMarker.GetRef())
Alias_Avulstein.GetActorRef().EvaluatePackage()
endif

Alias_Thorald.GetActorRef().Enable()
Alias_Thorald.GetActorRef().MoveTo(Alias_CenterMarker.GetRef())
Alias_Thorald.GetActorRef().EvaluatePackage()

if Alias_Geirlund.GetActorRef() != None && CWObj.IsCompleted() == 0
Alias_Geirlund.GetActorRef().Enable()
Alias_Geirlund.GetActorRef().MoveTo(Alias_CenterMarker.GetRef())
Alias_Geirlund.GetActorRef().EvaluatePackage()
endif

if Alias_Vidrald.GetActorRef() != None
Alias_Vidrald.GetActorRef().Enable()
Alias_Vidrald.GetActorRef().MoveTo(Alias_CenterMarker.GetRef())
Alias_Vidrald.GetActorRef().EvaluatePackage()
endif

aaSonsGrayManeCD.Value = 1
aaSonsGrayMane.RegisterForSingleUpdateGameTime(60)
;END CODE
EndFunction
;END FRAGMENT

;BEGIN FRAGMENT Fragment_6
Function Fragment_6()
;BEGIN CODE
Actor Thalmor1Ref = Alias_Thalmor1.GetActorRef()
Actor Thalmor2Ref = Alias_Thalmor2.GetActorRef()
Actor Thalmor3Ref = Alias_Thalmor3.GetActorRef()

if Thalmor1Ref
Thalmor1Ref.DeleteWhenAble()
endif
if Thalmor2Ref
Thalmor2Ref.DeleteWhenAble()
endif
if Thalmor3Ref
Thalmor3Ref.DeleteWhenAble()
endif

if CWObj.IsCompleted() == 0
Alias_Avulstein.GetActorRef().Disable()
Alias_Thorald.GetActorRef().Disable()

if Alias_Geirlund.GetActorRef() != None
Alias_Geirlund.GetActorRef().Disable()
endif

if Alias_Vidrald.GetActorRef() != None
Alias_Vidrald.GetActorRef().Disable()
endif
endif
;END CODE
EndFunction
;END FRAGMENT

;END FRAGMENT CODE - Do not edit anything between this and the begin comment

GlobalVariable Property aaSonsGrayManeCD  Auto  

IDSCGrayManeScript Property aaSonsGrayMane  Auto  

Quest Property CWObj  Auto  
