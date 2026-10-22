Scriptname SC_CompatibilitySCRIPT extends Quest

; Authoria inert override.
; The master sequence drives Starting Choices directly (SC_Main.Start() after RaceMenu),
; so this legacy compatibility quest must NEVER register for MQ101 or auto-start SC_Main.
; Empty OnInit severs the vanilla "MQ101 stage 800" (Helgen cave-exit) trigger regardless
; of whether the quest starts. Properties kept only so the quest's existing VMAD bindings
; resolve without warnings.

GlobalVariable Property SC_ASLAL Auto
Quest Property SC_Main Auto

Event OnInit()
    ; intentionally inert
EndEvent
