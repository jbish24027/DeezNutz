ScriptName SkyrimFairOutsideShow extends ObjectReference
{The Wanderer's Fair from outside its Tamriel walls: the fair's Songs2, faintly, one after another,
and at night a volley of fireworks over it now and then. Runs only while its cell is attached.}

int song = 0
int instance = 0
float songEnds = 0.0
float nextVolley = 0.0
bool running = false
int volley = 0

objectreference[] Property FireworkSites Auto

globalvariable Property FireworksOn Auto

globalvariable Property MusicEnabled Auto

sound[] Property Songs2 Auto

float Property SongGap = 20.0 Auto

float[] Property SongLengths2 Auto

float Property FireworkEvery = 150.0 Auto

spell[] Property FireworkShells Auto

objectreference[] Property FireworkAims Auto

ObjectReference Property Speaker Auto

float Property FireworkStagger = 0.6 Auto

Event OnCellAttach()
    Begin()
EndEvent

Event OnLoad()
    Begin()
EndEvent

Event OnCellDetach()
    Halt()
EndEvent

Event OnUnload()
    Halt()
EndEvent

Function Begin()
    if running
        return
    endif
    running = true
    songEnds = 0.0
    nextVolley = utility.GetCurrentRealTime() + 15.0
    RegisterForSingleUpdate(1.0)
EndFunction

Function Halt()
    running = false
    UnregisterForUpdate()
    if instance
        sound.StopInstance(instance)
        instance = 0
    endif
EndFunction

Event OnUpdate()
    if !running
        return
    endif
    float now = utility.GetCurrentRealTime()
    if Songs2.Length > 0 && now >= songEnds && (!MusicEnabled || MusicEnabled.GetValue() > 0.5)
        if instance
            sound.StopInstance(instance)
        endif
        sound hated = game.GetFormFromFile(0x050005, "SkyrimFair.esp") as sound
        if hated && Songs2.Length > 1 && Songs2[song] == hated
            song = (song + 1) % Songs2.Length
        endif
        instance = Songs2[song].Play(Speaker)
        songEnds = now + SongLengths2[song] + SongGap
        song = (song + 1) % Songs2.Length
    endif
    if now >= nextVolley
        nextVolley = now + FireworkEvery * utility.RandomFloat(0.8, 1.3)
        if IsNight()
            volley()
        endif
    endif
    if running
        RegisterForSingleUpdate(2.0)
    endif
EndEvent

bool Function IsNight()
    float t = utility.GetCurrentGameTime()
    float hour = (t - math.Floor(t)) * 24.0
    return hour >= 20.0 || hour < 5.0
EndFunction

Function volley()
    if FireworksOn && FireworksOn.GetValue() < 0.5 || FireworkShells.Length == 0
        return
    endif
    int k = 0
    while k < FireworkSites.Length && k < FireworkAims.Length
        spell shell = FireworkShells[(volley + k) % FireworkShells.Length]
        if shell && FireworkSites[k] && FireworkAims[k]
            shell.Cast(FireworkSites[k], FireworkAims[k])
        endif
        k = k + 1
        if k < FireworkSites.Length
            utility.Wait(FireworkStagger)
        endif
    endwhile
    volley = volley + 1
EndFunction

