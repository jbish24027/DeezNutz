ScriptName _Authoria_Init_PrismUI Hidden

Bool Function ShowNotice(String promptId, String payloadJson = "{}") Global Native
Bool Function ShowChoice(String promptId, String payloadJson = "{}") Global Native
Function Close() Global Native

Bool Function IsOpen() Global Native
Bool Function HasFocus() Global Native

Int Function GetPendingActionCount() Global Native
String Function ConsumeNextAction() Global Native

