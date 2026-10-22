Scriptname _Authoria_REQ_MajorFollowerBridge extends Quest
{Registers major custom follower aliases with Requiem's follower registry.}

REQ_FollowerRegistration Property REQ_FollowerControl Auto

ReferenceAlias Property InigoFollower Auto
ReferenceAlias Property KaidanFollower Auto
ReferenceAlias Property AuriFollower Auto
ReferenceAlias Property XelzazFollower Auto
ReferenceAlias Property MrissiFollower Auto
ReferenceAlias Property SaharaFollower Auto
ReferenceAlias Property ThograFollower Auto
ReferenceAlias Property YoanaFollower Auto
ReferenceAlias Property RemielFollower Auto
ReferenceAlias Property LucienFollower Auto
ReferenceAlias Property AsheFollower Auto
ReferenceAlias Property AstridFollower Auto
ReferenceAlias Property ValSeranoFollower Auto
ReferenceAlias Property JimothyFollower Auto

Float Property StartupDelay = 2.0 Auto
Float Property RetryDelay = 0.5 Auto
Int Property MaxRegistrationPasses = 10 Auto
Bool Property EnableTrace = True Auto

Bool RegistrationFinished = False
Int RegistrationPass = 0
Int RegisteredThisPass = 0

Event OnInit()
	RegisterForSingleUpdate(StartupDelay)
EndEvent

Event OnUpdate()
	If RegistrationFinished
		Return
	EndIf

	RegistrationPass = RegistrationPass + 1

	If REQ_FollowerControl == None
		Trace("REQ_FollowerControl is not filled.")
		RetryOrFinish(0)
		Return
	EndIf

	RegisteredThisPass = 0
	RegisterOne(InigoFollower, "Inigo")
	RegisterOne(KaidanFollower, "Kaidan")
	RegisterOne(AuriFollower, "Auri")
	RegisterOne(XelzazFollower, "Xelzaz")
	RegisterOne(MrissiFollower, "Mrissi")
	RegisterOne(SaharaFollower, "Sahara")
	RegisterOne(ThograFollower, "Thogra")
	RegisterOne(YoanaFollower, "Yoana")
	RegisterOne(RemielFollower, "Remiel")
	RegisterOne(LucienFollower, "Lucien")
	RegisterOne(AsheFollower, "Ashe")
	RegisterOne(AstridFollower, "Astrid")
	RegisterOne(ValSeranoFollower, "Val Serano")
	RegisterOne(JimothyFollower, "Jimothy")

	Trace("Registration pass " + RegistrationPass + " completed. Successful aliases: " + RegisteredThisPass)
	RetryOrFinish(RegisteredThisPass)
EndEvent

Function RegisterOne(ReferenceAlias followerAlias, String followerName)
	If followerAlias == None
		Trace(followerName + " alias is empty; skipped.")
		Return
	EndIf

	If REQ_FollowerControl.RegisterFollowerAlias(followerAlias)
		Trace(followerName + " alias registered: " + followerAlias)
		RegisteredThisPass = RegisteredThisPass + 1
		Return
	EndIf

	Trace(followerName + " alias was not registered. It may already be registered, or Requiem's alias storage may be full: " + followerAlias)
EndFunction

Function RetryOrFinish(Int registeredCount)
	If registeredCount > 0 || RegistrationPass >= MaxRegistrationPasses
		RegistrationFinished = True
		Return
	EndIf

	RegisterForSingleUpdate(RetryDelay)
EndFunction

Function Trace(String logText)
	If EnableTrace
		Debug.Trace("[Authoria_REQ_MajorFollowerBridge] " + logText)
	EndIf
EndFunction
