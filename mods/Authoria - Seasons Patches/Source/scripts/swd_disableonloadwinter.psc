Scriptname SWD_DisableOnLoadWinter extends ObjectReference

GlobalVariable Property InGameMonth Auto

Event OnLoad()
	; GameMonth is 0–11 (0=Jan ... 11=Dec)
	int Month = 0

	if InGameMonth
		Month = InGameMonth.GetValueInt()
	else
		return
	endif

	; Winter = Dec (11) + Jan (0) + Feb (1)
	if (Month == 11 || Month == 0 || Month == 1)
		Self.Disable()
	endif
EndEvent