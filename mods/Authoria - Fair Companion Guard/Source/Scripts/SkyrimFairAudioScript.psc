ScriptName SkyrimFairAudioScript extends Quest
{The Wanderer's Fair's stage set: song, cheer, a breath, the next song, round the
playlist, while the player is at the fair. It also sets the level of the fair's crowd
ambience, which plays by itself from placed sound markers, and ducks it under a song.

It also leads the band: the bards take up their instruments when a song starts and put
them away when it ends, as vanilla's bard scenes do (PlayIdle IdleLuteStart, IdleStop).
And as the fair's only controller, it sets the archers back on their stands on every
arrival and load: without navmesh their training package doesn't pick up again by itself.

Every property is written by the generator from fair.config.json (fairWorld.audio);
see docs/AUDIO.md. Sounds do not survive a save or a load, so the player alias calls
Recover() on every load and the set starts over cleanly: nothing is left playing twice.}

bool moreDancesFound = false
bool[] archerHeld
int cheerInstance = 0
int singMode = 1
int seatLayoutDone = 0
int[] dancePlays
int[] danceMode
int runUpSeated = 0
float phaseEnds = 0.0
int appliedTier = -1
float[] singerNext
bool holding = false
float songStarted = 0.0
float danceWake = 0.0
bool reseating = false
float lastGame = 0.0
float lastReal = 0.0
bool[] cameoPlaying
float singerWake = 0.0
int phase = 0
bool[] orchestraPlaying
bool[] bandPlaying
int crowdMode = 0
float[] cameoMoveNext
float holdEnds = 0.0
float cameoWake = 0.0
float ambienceLevel = -1.0
float stepDone = 0.0
bool[] cameoExiting
bool[] inMoreDance
int[] cameoIdleNow
bool[] archerPending
float stepNext = 0.0
int nextSection = -1
float bandUntil = 0.0
int[] cameoPlays
bool singing = true
bool moreDancesChecked = false
bool stepOn = false
float stepApplied = 0.0
int stepAt = 0
int[] singerPlays
int[] playLevel
int danceTick = 0
int endLine = -1
bool runUpClose = false
int nextLine = -1
int songsPlayed = 0
bool folkOn = false
float[] danceEnds
bool[] dancing
bool bandOn = false
int songInstance = 0
float runUpTalkAt = -100.0
string runUpLogged = ""
int retiredDone = 0
float folkNext = 0.0
int track = 0
int tailInstance = 0
int drumLevel = 1
float[] cameoNext
bool runUpHeld = false
int endSection = -1
float showDays = 0.0

idle[] Property BandIdles Auto
{For each bard, the idle that brings out their instrument and plays it.}

actor[] Property Cameos Auto
{The named ambient characters (Garrick Sol V, Claudius Vale; FairCameos.cs). They wander on their
own sandbox; every so often, when free, each plays his next idle and stops it after its hold.}

idle[] Property CheerIdles Auto

globalvariable Property TimeScale Auto
{Vanilla's TimeScale, to turn game time into seconds.}

int[] Property SectionCrowd2 Auto
{0 the dancers dance, 1 they clap, 2 they cheer.}

int[] Property SongCheers2 Auto
{Index into Cheers played after each song; -1 for none.}

float Property PassportWatchPoll = 0.25 Auto

float[] Property CameoEveryMax3 Auto
{Seconds between one cameo's idles, at random between the two.}

actor[] Property Archers Auto
{The archery range's archers, each linked (unkeyed) to the stand it shoots from.}

perk Property FairTalk Auto
{The fair's talk perk (SkyrimFairTalkDuck): pressing E on anyone at the fair ducks the music while
they answer. Given to the player at the fair; its conditions keep it to the fair.}

float Property SingerFirstStep = 6.0 Auto
{Seconds into a song before the first step.}

float[] Property SingerFacing Auto
{Each singer's heading, in degrees from the anchor's.}

globalvariable Property CameoDuckUntil Auto
{Set by each cameo line's begin fragment (SkyrimFairCameoLine): the real time its line ends.}

idle Property BandStop Auto
{Puts an instrument away.}

objectreference[] Property CrowdLayers Auto
{Each crowd layer's enable-parent marker, the most wanted first.}

globalvariable[] Property InstrumentTempo Auto
{Each instrument's tempo global (InstrumentIdles order), held at its level: 0 rest, 1 normal,
2 fast, 3 away. Open Animation Replacer plays a held loop for the fair's musicians while it's
0 and a faster one while it's 2.}

string Property MoreDancesPlugin = "Dance.esp" Auto

float[] Property SingerRestLengths Auto
{While the singers rest (a song's singers timeline), these instead (clapping along).}

float Property SteadySingerLoop Auto
{In the steady show, the sing move's real length (the Mixamo cheer's clip, 2.9 s), replayed
with no gap.}

float Property FirstSongDelay = 4.0 Auto
{Seconds after arriving (or loading) before the first song.}

int[] Property SongLineCount2 Auto

idle Property SingerEndMove Auto
{At a song's end, with the crowd's cheer (a wave).}

int[] Property CameoFirstIdle2 Auto

idle[] Property SingerCheerMoves Auto

float Property SingerStepSeconds = 3.0 Auto
{Seconds a step takes: no gesture starts before it ends, or would run into the next.}

actor[] Property FolkDancers Auto
{Astra's paired folk dance: each dancer's clip replaces FolkIdle's animation for that NPC
(Open Animation Replacer), so both are started together and restarted every FolkLength.}

referencealias Property PassportGreeter Auto
{The alias holding him for the force greet: forced in the plugin, filled here on saves where the
Passport quest was already running.}

idle[] Property CameoIdles2 Auto

globalvariable Property TalkDuckUntil Auto
{Set by the talk perk's fragment: the real time until which the music stays ducked.}

float Property ActivePoll = 2.0 Auto
{Most seconds between checks at the fair (volumes, leaving).}

int[] Property CameoSpotCount Auto

globalvariable Property ArcherHold Auto
{No longer used to switch the archers (it didn't restart their package); only ever set
back to 0 here, in case a save holds it at 1.}

worldspace Property FairWorld Auto
{Where the set plays. Outside it, everything this script started is stopped.}

float Property MusicMix = 0.8 Auto
{Retired: MusicMix2 now (saves that ran 2.0.1 keep this one's 0.8).}

objectreference[] Property SeatChairs Auto

float[] Property SingerStarts2 Auto
{Each line's start, in seconds from its song's start.}

globalvariable Property MusicVolume Auto

float[] Property SingerStepOffsets Auto
{The line's sideways offsets, in turn, one a step (Songs2.config.json singerSteps). None: they stand.}

string[] Property MoreDanceEvents Auto

topic[] Property SingerTopics2 Auto

globalvariable Property CrowdLayer Auto
{How many crowd layers are on: set SkyrimFairCrowdLayers to 0..n in the console.}

actor[] Property Dancers2 Auto
{The dance floor (persistent references): they dance through each song and cheer at its end.}

actor[] Property Orchestra Auto
{The rest of the orchestra (added after the first band, so a save picks them up).}

package Property PassportGreet Auto
{Claudius's wait at the entrance, the whole time (a sandbox, no sitting).}

idle[] Property CameoStops2 Auto
{The idle that ends each of CameoIdles2 (Hadvar's ledger has its own exit); None: BandStop.}

int Property MoreDancesCheck Auto
{A record in MoreDancesPlugin that shows it's loaded.}

float[] Property SingerHomeY Auto

actor Property PassportInspector Auto
{Claudius, whom RunUp nudges: his AI is only re-checked every so often, so a player arriving
found him still seated at his table under his rounds' sandbox (Barry, 2026-09-26).}

Quest Property Passport Auto
{The Fair Passport (SkyrimFairPassport), if built: told when each song starts and ends.}

objectreference[] Property FireworkAims Auto
{A marker above each site, for the shell to fly at.}

float[] Property ClapLengths Auto
{A song's "clap" sections: the dancers applaud, each clip replayed as it ends.}

globalvariable Property MusicEnabled Auto

sound[] Property Cheers Auto

objectreference Property StageSpeaker Auto
{The persistent marker on the stage the music and the cheer come from.}

globalvariable Property AmbienceEnabled Auto

float Property SingerStepEvery = 8.0 Auto
{Seconds between steps while they sing.}

int[] Property SectionDrums Auto
{Retired (the drums alone): a save keeps its old value; SectionPlay2 has every instrument now.}

float[] Property CameoMoveMax3 Auto
{Each cameo's round: his spot global (his spot packages each run on one value), how many
spots, and the seconds before he moves on. Moving on sets the global to another spot and
re-evaluates his package, so he walks there.}

idle[] Property OrchestraIdles Auto

float Property PauseAfterCheer = 2.0 Auto
{The breath between the cheer and the next song.}

float[] Property CameoMoveMin3 Auto

float[] Property CameoHolds3 Auto

idle[] Property SingerRestMoves Auto

idle Property DrumIdle Auto
{Retired: InstrumentIdles has every instrument now.}

float[] Property CheerIdleLengths Auto
{Each cheer idle's clip length: a song's "cheer" sections replay them as each ends.}

globalvariable Property CheerVolume Auto

float[] Property SingerMoveLengths Auto
{While they sing, the singers gesture: these idles, in turn, each clip replayed after its
length and a breath (SingerGap), the three staggered so they don't move as one.}

float[] Property SeatYaw Auto
{The chairs at the tables and the heading each should face (degrees). A save that met the fair's
bar stools keeps their old angles, so each is turned to its heading once (SeatLayoutVersion).}

idle[] Property DanceIdles Auto

spell[] Property FireworkNightShells Auto
{More at night (20:00-05:00), from the middle site.}

globalvariable Property AtFair Auto
{1 while the player is at the fair: the compatibility patches switch other mods' per-NPC
spells off while it's on. Saved with the game, so a load at the fair starts with it on.}

float[] Property SingerHomeZ Auto
{Each singer's mark, as an offset from the anchor.}

int[] Property CameoIdleCount2 Auto
{Each cameo's idles are CameoIdles2[CameoFirstIdle2[i] ...], CameoIdleCount2[i] of them, in turn.}

float[] Property SectionStarts2 Auto
{Every song's sections, song by song: each one's start in seconds from its song's start.}

idle Property FolkIdle Auto

float Property PassportGreetRadius = 800.0 Auto

float Property IdlePoll = 5.0 Auto
{Seconds between checks while the player is elsewhere.}

int[] Property SectionPlay2 Auto
{For each section, each instrument in InstrumentIdles in turn: 0 rest (held, still), 1 normal,
2 fast, 3 away (put away).}

float Property MusicMix2 = 0.6 Auto
{The stage music and the crowd's cheer, as a share of MusicVolume (0.6). A player found the band
drowned out the NPCs (Nexus, 2026-09-25); 0.8 was still loud (Barry).}

float[] Property MoreDanceLengths Auto
{Professional Dancer's dances: its animation events (Dance1...) and their clips' lengths. While
dancing, if its plugin is loaded, each dancer takes them in turn; otherwise the vanilla dances.}

float Property SingerFollow = 12.0 Auto
{KeepOffsetFromActor's radii: past catch-up they'd run; within follow they stand.}

idle[] Property SingerMoves Auto

int Property CompanionSlots = 6 Auto

float Property SpeechDuckLevel = 0.05 Auto
{The music's volume, as a share of its mix, while anyone speaks: a cameo's greeting, or any
dialogue or barter menu open (Utility.IsInMenuMode). 0.05, nearly silent.}

string[] Property StripPlugins Auto

globalvariable[] Property CameoSpot Auto

globalvariable Property FirstTrack Auto
{For testing: the song to start with on arrival or load (0 = the first). At -1 (the default)
the show still opens with the first song, The Wanderer's Fair. set SkyrimFairAudioFirstTrack
to 3 starts with Fiddle.}

objectreference[] Property ResetRefs Auto

formlist Property StripSpells Auto
{The NPC guard's list (SkyrimFairNpcGuard): filled here from StripPlugins/StripIds.}

int Property DanceEvery = 2 Auto
{Each dancer is given a dance every this many updates during a song (an update is 2 s at most).}

float Property FolkClipLength = 57.6 Auto
{The folk clip's length in seconds: the pair start it again together as it ends.}

float[] Property CameoEveryMin3 Auto

actor[] Property Singers Auto
{The three singers at the front of the deck (docs/BARDS.md). Their lips follow the song:
each sung line is a topic whose voice file (silent audio, a lip track) differs per
singer's voice type.}

int[] Property StripIds Auto

float Property PassportTalkRange = 400.0 Auto
{Within this of him, if his force greet hasn't started the talk, the script starts it, and the
player is held where they are until he's handed the passport over (Barry: "I can literally just
run past Claudius").}

sound[] Property Songs2 Auto

float Property PassportWaitAhead = 300.0 Auto
{How far in front of the entrance marker (along its heading, into the fair) he's put.}

globalvariable Property AmbienceVolume Auto

idle Property SingerCheerMove Auto
{Retired: the song-end move is SingerEndMove now.}

objectreference[] Property FireworkSites Auto
{Invisible markers the fireworks go up from, as each song ends.}

float Property SingerGap = 2.0 Auto
{Seconds each singer stands between moves.}

float Property FolkLength = 9.6 Auto
{Retired: a save keeps this property's old value, so the length is FolkClipLength now.}

int Property RetiredVisitorsVersion Auto

idle[] Property InstrumentIdles Auto
{The instruments with timelines (lute, drum, flute): a musician whose idle is one follows it.}

float[] Property DanceLengths Auto
{Each dance's clip length in seconds. A vanilla idle plays its clip once, so each dancer
is given the next dance the moment the last one ends.}

float[] Property SingerHomeX Auto

float Property FaceStageSteps = 3.0 Auto
{Clapping and cheering dancers turn to the stage in this many steps (0.06 s apart), not a snap.}

package Property PassportForceGreet Auto
{His force greet (on the Passport quest's Greeter alias): with the player within
PassportGreetRadius and no passport issued, he walks up and starts the stop line.}

float[] Property SongLengths2 Auto
{Seconds, measured from the files by the generator.}

perk Property FairPrices Auto
{The fair's prices (FairShops.cs): a hidden perk, buying at many times the price, only in the
fair's worldspace. Given to the player at the fair; it does nothing anywhere else.}

bool Property SteadyShow Auto
{Barry, 2026-09-25: everything plays through the whole song. Every instrument at its normal
loop, the singers singing, and their sing move replayed back to back; the songs' drums and
singers timelines are ignored (the crowd's still runs).}

actor[] Property Sitters2 Auto
{The seated visitors: sent back to their seats (their editor locations) once, to sit down again.}

Quest Property CompanionFinder Auto
{Optional aliases that find the player's companions anywhere (teammates or followers, alive,
not waiting). Followers don't come through the fair's gate by themselves: its load door has
no navmesh door links on either side. So on arriving and on leaving, the finder is restarted
and each companion it finds is moved to the player.}

objectreference[] Property RetiredVisitors Auto
{The visitors the voiced fairgoers stand in for (FairFairgoers.cs): switched off in the plugin,
and once per RetiredVisitorsVersion here, as a save may have them on.}

spell[] Property FireworkShells Auto
{The shells, one per site in turn (the fair's own: vanilla effects, no damage).}

float[] Property ResetTransforms Auto
{Pieces a save may hold in the wrong place (a swaying sign board): each put back to its position
and heading once, four numbers a piece (x, y, z, heading in degrees).}

int[] Property SongFirstSection2 Auto
{For each song, its first section, or -1 for a song without (drums and dancing throughout).}

soundcategory Property AmbienceCategory Auto
{The fair's own ambience category; the placed crowd markers play in it.}

float Property DuckDuringSong = 0.75 Auto
{The ambience's level while a song plays, as a share of its normal level.}

float Property CheerLead = 1.0 Auto
{Seconds before a song's end that its cheer starts, as the last note rings. The song
isn't stopped: it finishes on its own (the update timer can run late when Papyrus is
busy, so waiting for the full length left a gap).}

float[] Property SingerCheerLengths Auto
{A "cheer" stretch of the singers' timeline: they break into these (the Civil War cheer) at
once, replayed through the stretch, and keep singing their lines.}

idle[] Property ClapIdles Auto

float Property FireworkStagger = 0.6 Auto

float[] Property CheerLengths Auto

int[] Property SongSectionCount2 Auto

actor[] Property Band Auto
{The bards on the stage (persistent references).}

actor[] Property Keepers Auto
{The shopkeepers: sent back to their spots behind their counters once as well (one had wandered
off beside his stall in a save, 2026-09-25).}

int Property SeatLayoutVersion Auto
{Bumped whenever the seat layout changes, so every save re-seats once more.}

globalvariable Property FireworksOn Auto
{set SkyrimFairFireworks to 0 to stop them.}

float Property CameoDuckLevel = 0.2 Auto
{Retired: SpeechDuckLevel now (a save keeps this one's old value).}

float Property SingerCatchUp = 1000.0 Auto

float Property SpeechPoll = 1.0 Auto
{The longest the script waits between looks while the show runs, so the music dips within about
a second of a conversation starting.}

int[] Property SongFirstLine2 Auto
{For each song, its first line in SingerTopics2, or -1 for a song with no singing.}

objectreference Property PassportWaitMarker Auto
{The entrance marker he waits at: on arrival (or a load) at the fair, if he's wandered off (or a
save has him at his old table), he's put a few steps in front of it. His AI never walked him
there from his table (Barry, 2026-10-02).}

float Property ArcherHoldSeconds = 1.5 Auto

actor Property SingerAnchor Auto
{Hidden under the deck, facing north, its AI off. While the show runs the singers keep an
offset from it (KeepOffsetFromActor), so they step sideways across the deck facing the crowd.}

int[] Property SectionSing2 Auto
{For each section: 1 the singers sing (their lines are said), 2 they sing and cheer, 0 they
rest (lines skipped).}

float Property PassportWatchRange = 2000.0 Auto
{Within this of him, with no passport issued, the script looks every PassportWatchPoll seconds,
so a sprinting player can't pass him between two looks.}

Event OnInit()
    debug.Trace("SkyrimFairAudio: started, " + Songs2.Length + " Songs2", 0)
    FillStripSpells()
    RegisterForSingleUpdate(3.0)
EndEvent

Function Recover()
    debug.Trace("SkyrimFairAudio: game loaded, the set starts over", 0)
    songInstance = 0
    cheerInstance = 0
    tailInstance = 0
    bandUntil = 0.0
    lastReal = 0.0
    phase = 0
    ambienceLevel = -1.0
    bandOn = false
    bandPlaying = new bool[16]
    orchestraPlaying = new bool[32]
    appliedTier = -1
    folkNext = 0.0
    moreDancesChecked = false
    cameoNext = new float[8]
    cameoPlaying = new bool[8]
    cameoPlays = new int[8]
    cameoIdleNow = new int[8]
    cameoMoveNext = new float[8]
    if CameoDuckUntil
        CameoDuckUntil.SetValue(0.0)
    endif
    SingersStand()
    FillStripSpells()
    RegisterForSingleUpdate(1.0)
EndFunction

Function FillStripSpells()
    if !StripSpells
        return
    endif
    StripSpells.Revert()
    int i = 0
    while i < StripPlugins.Length && i < StripIds.Length
        spell S = (game.GetFormFromFile(StripIds[i], StripPlugins[i]) as spell)
        if S
            StripSpells.AddForm(S)
        endif
        i = i + 1
    endwhile
    debug.Trace("SkyrimFairAudio: NPC guard strips " + StripSpells.GetSize() + " spells", 0)
EndFunction

Event OnUpdate()
    bool here = game.GetPlayer().GetWorldSpace() == FairWorld
    if AtFair && !(AtFair.GetValue() >= 0.5 == here)
        if here
            AtFair.SetValue(1.0)
        else
            AtFair.SetValue(0.0)
        endif
    endif
    if !here
        ReleaseArchers()
        if !(phase == 0)
            StopAll()
            phase = 0
            BringCompanions()
        endif
        RegisterForSingleUpdate(IdlePoll)
        return
    endif
    float now = utility.GetCurrentGameTime()
    float show = ShowNow()
    if phase == 0
        track = 0
        if FirstTrack && FirstTrack.GetValue() >= 0.0 && (FirstTrack.GetValue() as int) < Songs2.Length
            track = (FirstTrack.GetValue() as int)
        endif
        Enter(1, FirstSongDelay, show)
        StopBand(true)
        QueueArchers()
        RunUpRelease()
        PlaceInspector()
        RetireVisitors()
        BringCompanions()
    endif
    ResetArchers()
    if FairPrices && !game.GetPlayer().HasPerk(FairPrices)
        game.GetPlayer().AddPerk(FairPrices)
    endif
    if FairTalk && !game.GetPlayer().HasPerk(FairTalk)
        game.GetPlayer().AddPerk(FairTalk)
    endif
    if seatLayoutDone < SeatLayoutVersion
        Reseat()
    endif
    ApplyCrowdLayers()
    RunUp()
    CameoIdles2(utility.GetCurrentGameTime())
    if MusicEnabled.GetValue() < 0.5 || Songs2.Length == 0
        if !(songInstance == 0) || !(cheerInstance == 0)
            StopAll()
        endif
        Enter(1, FirstSongDelay, show)
    elseif show >= phaseEnds
        Advance(show)
    endif
    if !(songInstance == 0)
        if CameoTalking() || utility.IsInMenuMode() || TalkDuckUntil && utility.GetCurrentRealTime() < TalkDuckUntil.GetValue()
            sound.SetInstanceVolume(songInstance, MusicVolume.GetValue() * MusicMix2 * SpeechDuckLevel)
        else
            sound.SetInstanceVolume(songInstance, MusicVolume.GetValue() * MusicMix2)
        endif
    endif
    SetAmbience(phase == 2)
    if phase == 2
        Sections(show)
        PlayBand()
        Dance()
        SingerSteps(now)
        SingerGestures(now)
        FolkDance(now)
        Sing(show)
    else
        if phase == 3
            Dance()
        endif
        if bandOn && show >= bandUntil
            StopBand(false)
        endif
    endif
    float left = Seconds(phaseEnds - show)
    if (phase == 2 || phase == 3) && danceWake > now && Seconds(danceWake - now) < left
        left = Seconds(danceWake - now)
    endif
    if phase == 2 && folkOn && folkNext > now && Seconds(folkNext - now) < left
        left = Seconds(folkNext - now)
    endif
    if phase == 2 && singerWake > now && Seconds(singerWake - now) < left
        left = Seconds(singerWake - now)
    endif
    if phase == 2 && !SteadyShow && SingerStepOffsets.Length > 0 && stepNext > now && Seconds(stepNext - now) < left
        left = Seconds(stepNext - now)
    endif
    if cameoWake > now && Seconds(cameoWake - now) < left
        left = Seconds(cameoWake - now)
    endif
    if left > 0.5 && CameoNear()
        left = 0.5
    endif
    if left > SpeechPoll && !(songInstance == 0)
        left = SpeechPoll
    endif
    if !(phase == 2) && bandOn && bandUntil > show && Seconds(bandUntil - show) < left
        left = Seconds(bandUntil - show)
    endif
    if phase == 2 && nextSection >= 0 && nextSection < endSection
        float toSection = SectionStarts2[nextSection] - Seconds(show - songStarted)
        if toSection < left
            left = toSection
        endif
    endif
    if phase == 2 && nextLine >= 0 && nextLine < endLine
        float toLine = SingerStarts2[nextLine] - Seconds(show - songStarted)
        if toLine < left
            left = toLine
        endif
    endif
    if left > ActivePoll
        left = ActivePoll
    elseif left < 0.1
        left = 0.1
    endif
    if runUpClose && left > PassportWatchPoll
        left = PassportWatchPoll
    endif
    RegisterForSingleUpdate(left)
EndEvent

int Function AuthoriaSkipHatedSong(int t)
    {Authoria 2026-10-22: the user's pick - never play "The Wanderer's Fair" song; the rotation moves on to the next one.}
    sound hated = game.GetFormFromFile(0x050002, "SkyrimFair.esp") as sound
    if hated && Songs2.Length > 1 && Songs2[t] == hated
        t = (t + 1) % Songs2.Length
    endif
    return t
EndFunction

Function Advance(float now)
    float lead
    if phase == 1 || phase == 4
        if phase == 4
            track = (track + 1) % Songs2.Length
        endif
        if track >= Songs2.Length
            track = 0
        endif
        track = AuthoriaSkipHatedSong(track)
        tailInstance = 0
        songInstance = Songs2[track].Play(StageSpeaker)
        debug.Trace("SkyrimFairAudio: song " + track + " playing, instance " + songInstance, 0)
        songsPlayed = songsPlayed + 1
        if Passport
            (Passport as skyrimfairpassport).songStarted()
        endif
        dancing = new bool[128]
        danceEnds = new float[128]
        dancePlays = new int[128]
        danceMode = new int[128]
        folkOn = false
        folkNext = 0.0
        songStarted = now
        nextLine = -1
        endLine = -1
        drumLevel = 1
        playLevel = new int[8]
        int pl = 0
        while pl < 8
            playLevel[pl] = 1
            pl = pl + 1
        endwhile
        SetTempo(1)
        singing = true
        singMode = 1
        singerNext = new float[16]
        singerPlays = new int[16]
        int si = 0
        while si < 16
            singerNext[si] = utility.GetCurrentGameTime() + (1.5 + si * 1.3) * TimeScale.GetValue() / 86400.0
            si = si + 1
        endwhile
        stepAt = 0
        stepOn = false
        stepDone = 0.0
        stepNext = utility.GetCurrentGameTime() + SingerFirstStep * TimeScale.GetValue() / 86400.0
        crowdMode = 0
        nextSection = -1
        endSection = -1
        if track < SongFirstSection2.Length && SongFirstSection2[track] >= 0
            nextSection = SongFirstSection2[track]
            endSection = nextSection + SongSectionCount2[track]
        endif
        if track < SongFirstLine2.Length && SongFirstLine2[track] >= 0
            nextLine = SongFirstLine2[track]
            endLine = nextLine + SongLineCount2[track]
        endif
        sound.SetInstanceVolume(songInstance, MusicVolume.GetValue() * MusicMix2)
        Enter(2, SongLengths2[track] - lead(), now)
    elseif phase == 2
        lead = lead()
        if Passport
            (Passport as skyrimfairpassport).SongEnded()
        endif
        tailInstance = songInstance
        songInstance = 0
        bandUntil = now + lead * TimeScale.GetValue() / 86400.0
        int cheer = SongCheers2[track]
        if cheer >= 0 && cheer < Cheers.Length
            cheerInstance = Cheers[cheer].Play(StageSpeaker)
            sound.SetInstanceVolume(cheerInstance, CheerVolume.GetValue() * MusicMix2)
            debug.Trace("SkyrimFairAudio: cheer " + cheer + " at " + Seconds(now - songStarted) + " s into song " + track + " (" + SongLengths2[track] + " s long, lead " + lead + ")", 0)
            Enter(3, CheerLengths[cheer], now)
            cheer()
            Fireworks()
        else
            Enter(4, lead + PauseAfterCheer, now)
        endif
    elseif phase == 3
        cheerInstance = 0
        Enter(4, PauseAfterCheer, now)
    endif
EndFunction

float Function lead()
    float lead = CheerLead
    if lead < 0.0
        lead = 0.0
    elseif lead > SongLengths2[track] / 2.0
        lead = SongLengths2[track] / 2.0
    endif
    return lead
EndFunction

float Function ShowNow()
    float realNow = utility.GetCurrentRealTime()
    float gameNow = utility.GetCurrentGameTime()
    float perSecond = TimeScale.GetValue() / 86400.0
    if lastReal > 0.0 && realNow >= lastReal
        float step = realNow - lastReal
        float cap = (gameNow - lastGame) / perSecond * 1.6 + 0.25
        if step > cap
            step = cap
        endif
        if step > 0.0
            showDays = showDays + step * perSecond
        endif
    endif
    lastReal = realNow
    lastGame = gameNow
    return showDays
EndFunction

Function Enter(int newPhase, float lengthSeconds, float now)
    phase = newPhase
    phaseEnds = now + lengthSeconds * TimeScale.GetValue() / 86400.0
EndFunction

float Function Seconds(float days)
    return days * 86400.0 / TimeScale.GetValue()
EndFunction

Function StopAll()
    nextLine = -1
    if !(songInstance == 0)
        sound.StopInstance(songInstance)
        songInstance = 0
    endif
    if !(cheerInstance == 0)
        sound.StopInstance(cheerInstance)
        cheerInstance = 0
    endif
    if !(tailInstance == 0)
        sound.StopInstance(tailInstance)
        tailInstance = 0
    endif
    bandUntil = 0.0
    SetTempo(1)
    int i = 0
    while i < Dancers2.Length && i < inMoreDance.Length
        if inMoreDance[i] && Dancers2[i] && Dancers2[i].Is3DLoaded()
            debug.SendAnimationEvent(Dancers2[i], "IdleForceDefaultState")
        endif
        inMoreDance[i] = false
        i = i + 1
    endwhile
    SetAmbience(false)
    StopBand(false)
    SingersStand()
EndFunction

Function PlayBand()
    if bandPlaying.Length < Band.Length
        bandPlaying = new bool[16]
    endif
    if orchestraPlaying.Length < Orchestra.Length
        orchestraPlaying = new bool[32]
    endif
    bandOn = true
    PlayAll(Band, BandIdles, bandPlaying)
    PlayAll(Orchestra, OrchestraIdles, orchestraPlaying)
EndFunction

Function PlayAll(actor[] players, idle[] idles, bool[] playing)
    int i = 0
    while i < players.Length && i < playing.Length && i < idles.Length
        if !playing[i] && players[i] && players[i].Is3DLoaded() && playing(idles[i])
            playing[i] = players[i].PlayIdle(idles[i])
        endif
        i = i + 1
    endwhile
EndFunction

Function StopBand(bool force)
    if bandPlaying.Length < Band.Length
        bandPlaying = new bool[16]
    endif
    if orchestraPlaying.Length < Orchestra.Length
        orchestraPlaying = new bool[32]
    endif
    StopAllOf(Band, bandPlaying, force)
    StopAllOf(Orchestra, orchestraPlaying, force)
    bandOn = false
EndFunction

Function StopAllOf(actor[] players, bool[] playing, bool force)
    int i = 0
    while i < players.Length && i < playing.Length
        if (force || playing[i]) && players[i] && players[i].Is3DLoaded()
            players[i].PlayIdle(BandStop)
        endif
        playing[i] = false
        i = i + 1
    endwhile
EndFunction

Function ApplyCrowdLayers()
    if !CrowdLayer
        return
    endif
    int want = (CrowdLayer.GetValue() as int)
    if want == appliedTier
        return
    endif
    int i = 0
    while i < CrowdLayers.Length
        if CrowdLayers[i]
            if i < want
                CrowdLayers[i].Enable(false)
            else
                CrowdLayers[i].Disable(false)
            endif
        endif
        i = i + 1
    endwhile
    appliedTier = want
    debug.Trace("SkyrimFairAudio: crowd layers on: " + want, 0)
EndFunction

Function SingerGestures(float now)
    singerWake = 0.0
    if Singers.Length == 0 || singerNext.Length < Singers.Length
        return
    endif
    idle[] moves = SingerMoves
    float[] lengths = SingerMoveLengths
    if SteadyShow
    elseif !singing
        moves = SingerRestMoves
        lengths = SingerRestLengths
    elseif singMode == 2 && SingerCheerMoves.Length > 0
        moves = SingerCheerMoves
        lengths = SingerCheerLengths
    endif
    if moves.Length == 0
        return
    endif
    float perSecond = TimeScale.GetValue() / 86400.0
    int i = 0
    while i < Singers.Length
        if now >= singerNext[i] && Singers[i] && Singers[i].Is3DLoaded()
            int which = (i * 2 + singerPlays[i]) % moves.Length
            float clip = 3.0
            if which < lengths.Length
                clip = lengths[which]
            endif
            float gap = SingerGap + i * 0.4
            if SteadyShow
                gap = 0.0
                if SteadySingerLoop > 0.0
                    clip = SteadySingerLoop
                endif
            endif
            if now < stepDone
                singerNext[i] = stepDone
            elseif !SteadyShow && singing && SingerStepOffsets.Length > 0 && stepOn && now + clip * perSecond > stepNext
                singerNext[i] = stepNext + SingerStepSeconds * perSecond
            elseif Singers[i].PlayIdle(moves[which])
                singerPlays[i] = singerPlays[i] + 1
                singerNext[i] = now + (clip + gap) * perSecond
            else
                singerNext[i] = now + perSecond
            endif
        endif
        if singerWake == 0.0 || singerNext[i] < singerWake
            singerWake = singerNext[i]
        endif
        i = i + 1
    endwhile
EndFunction

Function Reseat()
    if reseating
        return
    endif
    reseating = true
    seatLayoutDone = SeatLayoutVersion
    int i = 0
    while i < Sitters2.Length
        if Sitters2[i] && !Sitters2[i].IsDead()
            Sitters2[i].Disable(false)
        endif
        i = i + 1
    endwhile
    i = 0
    while i < SeatChairs.Length && i < SeatYaw.Length
        if SeatChairs[i] && AngleOff(SeatChairs[i].GetAngleZ(), SeatYaw[i]) > 1.0
            SeatChairs[i].SetAngle(0.0, 0.0, SeatYaw[i])
        endif
        i = i + 1
    endwhile
    i = 0
    while i < Sitters2.Length
        if Sitters2[i] && !Sitters2[i].IsDead()
            Sitters2[i].MoveToMyEditorLocation()
            Sitters2[i].Enable(false)
            Sitters2[i].EvaluatePackage()
        endif
        i = i + 1
    endwhile
    i = 0
    while i < ResetRefs.Length && i * 4 + 3 < ResetTransforms.Length
        if ResetRefs[i]
            ResetRefs[i].SetPosition(ResetTransforms[i * 4], ResetTransforms[i * 4 + 1], ResetTransforms[i * 4 + 2])
            ResetRefs[i].SetAngle(0.0, 0.0, ResetTransforms[i * 4 + 3])
        endif
        i = i + 1
    endwhile
    i = 0
    while i < Keepers.Length
        if Keepers[i] && !Keepers[i].IsDead()
            Keepers[i].MoveToMyEditorLocation()
            Keepers[i].EvaluatePackage()
        endif
        i = i + 1
    endwhile
    reseating = false
    debug.Trace("SkyrimFairAudio: re-seated " + SeatChairs.Length + " chairs, " + Sitters2.Length + " visitors and " + Keepers.Length + " keepers (layout " + SeatLayoutVersion + ")", 0)
EndFunction

Function RunUp()
    if !PassportGreet || !PassportInspector || !Passport || !(Passport.GetStage() == 0)
        runUpSeated = 0
        runUpClose = false
        RunUpRelease()
        if Passport
            RunUpLog("off, passport stage " + Passport.GetStage(), "")
        endif
        if PassportGreeter && PassportGreeter.GetReference()
            PassportGreeter.Clear()
            if PassportInspector
                PassportInspector.EvaluatePackage()
            endif
        endif
        return
    endif
    actor a = PassportInspector
    if PassportGreeter && !PassportGreeter.GetReference()
        PassportGreeter.ForceRefTo(a)
    endif
    package now = a.GetCurrentPackage()
    actor player = game.GetPlayer()
    float apart = a.GetDistance(player)
    bool near = apart < PassportGreetRadius
    string atGate = ""
    if PassportWaitMarker
        atGate = ", " + (a.GetDistance(PassportWaitMarker) as int) + " from the entrance"
    endif
    runUpClose = apart < PassportWatchRange
    if runUpHeld && !a.IsInDialogueWithPlayer() && (utility.GetCurrentRealTime() - runUpTalkAt > 3.0 || utility.GetCurrentRealTime() < runUpTalkAt)
        RunUpRelease()
    endif
    RunUpLog("package " + now + ", near " + near + ", alias " + (PassportGreeter && PassportGreeter.GetReference()) + ", sit " + a.GetSitState() + ", 3D " + a.Is3DLoaded() + ", talking " + a.IsInDialogueWithPlayer(), ", " + (apart as int) + " away" + atGate)
    if a.IsDead() || a.IsDisabled() || a.IsInDialogueWithPlayer()
        return
    endif
    float realNow = utility.GetCurrentRealTime()
    if apart < PassportTalkRange && a.Is3DLoaded() && !player.IsInCombat() && !utility.IsInMenuMode() && (realNow - runUpTalkAt > 20.0 || realNow < runUpTalkAt)
        runUpTalkAt = realNow
        debug.Trace("SkyrimFairAudio: run-up talk started by the script, " + (apart as int) + " away", 0)
        game.DisablePlayerControls(true, true, false, false, true, false, false, false, 0)
        runUpHeld = true
        a.SetAngle(0.0, 0.0, a.GetAngleZ() + a.GetHeadingAngle(player))
        a.SetLookAt(player, false)
        a.Activate(player, false)
        return
    endif
    if !(now == PassportGreet) && !(now == PassportForceGreet)
        runUpSeated = 0
        a.EvaluatePackage()
        return
    endif
    if PassportForceGreet && !(near == (now == PassportForceGreet))
        a.EvaluatePackage()
    endif
    if a.GetSitState() >= 2 && a.Is3DLoaded()
        runUpSeated = runUpSeated + 1
        if runUpSeated >= 2
            debug.SendAnimationEvent(a, "IdleForceDefaultState")
            a.EvaluatePackage()
            runUpSeated = 0
        endif
    else
        runUpSeated = 0
    endif
EndFunction

Function RetireVisitors()
    if RetiredVisitorsVersion <= 0 || retiredDone >= RetiredVisitorsVersion || RetiredVisitors.Length == 0
        return
    endif
    retiredDone = RetiredVisitorsVersion
    int off = 0
    int i = 0
    while i < RetiredVisitors.Length
        objectreference r = RetiredVisitors[i]
        if r && !r.IsDisabled()
            r.DisableNoWait(false)
            off = off + 1
        endif
        i = i + 1
    endwhile
    debug.Trace("SkyrimFairAudio: retired visitors switched off: " + off + " of " + RetiredVisitors.Length + " (version " + RetiredVisitorsVersion + ")", 0)
EndFunction

Function PlaceInspector()
    if !PassportWaitMarker || !PassportInspector
        return
    endif
    actor a = PassportInspector
    if a.IsDead() || a.IsDisabled() || a.IsInDialogueWithPlayer() || a.GetDistance(PassportWaitMarker) < PassportWaitAhead + 200.0
        return
    endif
    if a.GetSitState() >= 2
        debug.SendAnimationEvent(a, "IdleForceDefaultState")
    endif
    float heading = PassportWaitMarker.GetAngleZ()
    a.MoveTo(PassportWaitMarker, PassportWaitAhead * math.Sin(heading), PassportWaitAhead * math.Cos(heading), 0.0, true)
    a.SetAngle(0.0, 0.0, heading + 180.0)
    a.EvaluatePackage()
    debug.Trace("SkyrimFairAudio: run-up: Claudius put at the entrance", 0)
EndFunction

Function RunUpRelease()
    if runUpHeld
        game.EnablePlayerControls(true, true, false, false, true, false, false, true, 0)
        runUpHeld = false
        if PassportInspector
            PassportInspector.ClearLookAt()
        endif
    endif
EndFunction

Function RunUpLog(string what, string extra)
    if !(what == runUpLogged)
        runUpLogged = what
        debug.Trace("SkyrimFairAudio: run-up " + what + extra, 0)
    endif
EndFunction

float Function AngleOff(float a, float b)
    float d = a - b
    while d > 180.0
        d = d - 360.0
    endwhile
    while d < -180.0
        d = d + 360.0
    endwhile
    if d < 0.0
        return -d
    endif
    return d
EndFunction

Function BringCompanions()
    if !CompanionFinder
        return
    endif
    CompanionFinder.Stop()
    if !CompanionFinder.Start()
        return
    endif
    actor player = game.GetPlayer()
    int brought = 0
    int i = 0
    while i < CompanionSlots
        referencealias slot = (CompanionFinder.GetAlias(i) as referencealias)
        actor mate = None
        if slot
            mate = slot.GetActorRef()
        endif
        if mate && !(mate == player) && AuthoriaFairTravelAllowed(mate) && (!(mate.GetWorldSpace() == player.GetWorldSpace()) || mate.GetDistance(player) > 1500.0)
            mate.MoveTo(player, 70.0 * (brought % 3 - 1), -90.0 - 40.0 * (brought / 3), 0.0, true)
            brought = brought + 1
        endif
        i = i + 1
    endwhile
    CompanionFinder.Stop()
    if brought > 0
        debug.Trace("SkyrimFairAudio: brought " + brought + " companions to the player", 0)
    endif
EndFunction

bool Function CameoTalking()
    if CameoDuckUntil && utility.GetCurrentRealTime() < CameoDuckUntil.GetValue()
        return true
    endif
    int i = 0
    while i < Cameos.Length
        if Cameos[i] && Cameos[i].Is3DLoaded() && Cameos[i].IsInDialogueWithPlayer()
            return true
        endif
        i = i + 1
    endwhile
    return false
EndFunction

bool Function CameoNear()
    actor player = game.GetPlayer()
    int i = 0
    while i < Cameos.Length
        if Cameos[i] && Cameos[i].Is3DLoaded() && Cameos[i].GetDistance(player) < 600.0
            return true
        endif
        i = i + 1
    endwhile
    return false
EndFunction

Function CameoIdles2(float now)
    cameoWake = 0.0
    if Cameos.Length == 0
        return
    endif
    if cameoNext.Length < 8
        cameoNext = new float[8]
        cameoPlaying = new bool[8]
        cameoPlays = new int[8]
    endif
    if cameoIdleNow.Length < 8
        cameoIdleNow = new int[8]
    endif
    if cameoMoveNext.Length < 8
        cameoMoveNext = new float[8]
    endif
    if cameoExiting.Length < 8
        cameoExiting = new bool[8]
    endif
    float perSecond = TimeScale.GetValue() / 86400.0
    int i = 0
    while i < Cameos.Length && i < 8
        actor a = Cameos[i]
        bool greeting = PassportForceGreet && a && a.GetCurrentPackage() == PassportForceGreet
        if greeting && cameoPlaying[i]
            cameoNext[i] = now
        endif
        if cameoNext[i] == 0.0
            cameoNext[i] = now + utility.RandomFloat(CameoEveryMin3[i], CameoEveryMax3[i]) * perSecond
        elseif now >= cameoNext[i] && a
            if cameoExiting[i]
                if a.Is3DLoaded()
                    debug.SendAnimationEvent(a, "IdleForceDefaultState")
                    a.EvaluatePackage()
                endif
                cameoExiting[i] = false
                cameoNext[i] = now + utility.RandomFloat(CameoEveryMin3[i], CameoEveryMax3[i]) * perSecond
            elseif cameoPlaying[i]
                if a.Is3DLoaded()
                    idle Stop = BandStop
                    int playing = cameoIdleNow[i]
                    if playing < CameoStops2.Length && CameoStops2[playing]
                        Stop = CameoStops2[playing]
                    endif
                    a.PlayIdle(Stop)
                    a.EvaluatePackage()
                endif
                cameoPlaying[i] = false
                cameoExiting[i] = true
                cameoNext[i] = now + 3.0 * perSecond
            elseif CameoIdleCount2[i] > 0 && !greeting && a.Is3DLoaded() && !a.IsInCombat() && a.GetSitState() == 0 && !a.IsInDialogueWithPlayer()
                int k = CameoFirstIdle2[i] + cameoPlays[i] % CameoIdleCount2[i]
                if a.PlayIdle(CameoIdles2[k])
                    cameoIdleNow[i] = k
                    cameoPlays[i] = cameoPlays[i] + 1
                    cameoPlaying[i] = true
                    cameoNext[i] = now + CameoHolds3[k] * perSecond
                else
                    cameoNext[i] = now + 5.0 * perSecond
                endif
            else
                cameoNext[i] = now + 10.0 * perSecond
            endif
        endif
        if cameoWake == 0.0 || cameoNext[i] < cameoWake
            cameoWake = cameoNext[i]
        endif
        if a && i < CameoSpotCount.Length && CameoSpotCount[i] > 1 && i < CameoSpot.Length && CameoSpot[i]
            if cameoMoveNext[i] == 0.0
                cameoMoveNext[i] = now + utility.RandomFloat(CameoMoveMin3[i], CameoMoveMax3[i]) * perSecond
            elseif now >= cameoMoveNext[i] && !cameoPlaying[i] && !cameoExiting[i] && !greeting
                int count = CameoSpotCount[i]
                int spot = ((CameoSpot[i].GetValue() as int) + 1 + utility.RandomInt(0, count - 2)) % count
                CameoSpot[i].SetValue(spot)
                if a.Is3DLoaded()
                    a.EvaluatePackage()
                endif
                cameoMoveNext[i] = now + utility.RandomFloat(CameoMoveMin3[i], CameoMoveMax3[i]) * perSecond
            endif
            if cameoMoveNext[i] < cameoWake
                cameoWake = cameoMoveNext[i]
            endif
        endif
        i = i + 1
    endwhile
EndFunction

Function SingerSteps(float now)
    if SingerStepOffsets.Length == 0 || !SingerAnchor || SingerHomeX.Length < Singers.Length
        return
    endif
    float perSecond = TimeScale.GetValue() / 86400.0
    if SteadyShow
        if !stepOn || !(stepApplied == 0.0)
            SingerOffset(0.0)
            HoldGestures(now + SingerStepSeconds * perSecond)
        endif
        return
    endif
    if !stepOn
        stepAt = 0
        SingerOffset(SingerStepOffsets[0])
    endif
    if !singing
        if !(stepApplied == 0.0)
            SingerOffset(0.0)
            HoldGestures(now + SingerStepSeconds * perSecond)
        endif
        stepNext = now + SingerStepEvery * perSecond
        return
    endif
    if now >= stepNext
        stepAt = (stepAt + 1) % SingerStepOffsets.Length
        SingerOffset(SingerStepOffsets[stepAt])
        HoldGestures(now + SingerStepSeconds * perSecond)
        stepNext = now + SingerStepEvery * perSecond
    endif
EndFunction

Function SingerOffset(float dx)
    if !SingerAnchor || SingerHomeX.Length < Singers.Length
        return
    endif
    if SingerAnchor.Is3DLoaded()
        SingerAnchor.EnableAI(false)
        SingerAnchor.SetAlpha(0.0, false)
    endif
    int i = 0
    while i < Singers.Length
        if Singers[i] && Singers[i].Is3DLoaded()
            Singers[i].KeepOffsetFromActor(SingerAnchor, SingerHomeX[i] + dx, SingerHomeY[i], SingerHomeZ[i], 0.0, 0.0, SingerFacing[i], SingerCatchUp, SingerFollow)
        endif
        i = i + 1
    endwhile
    if !(dx == stepApplied) || !stepOn
        debug.Trace("SkyrimFairAudio: singers step to " + dx, 0)
    endif
    stepApplied = dx
    stepOn = true
EndFunction

Function HoldGestures(float until)
    stepDone = until
    int i = 0
    while i < singerNext.Length
        if singerNext[i] < until
            singerNext[i] = until
        endif
        i = i + 1
    endwhile
EndFunction

Function SingersStand()
    int i = 0
    while i < Singers.Length
        if Singers[i]
            Singers[i].ClearKeepOffsetFromActor()
        endif
        i = i + 1
    endwhile
    stepOn = false
    stepApplied = 0.0
    stepDone = 0.0
EndFunction

Function Sections(float now)
    if nextSection < 0
        return
    endif
    if playLevel.Length < 8
        playLevel = new int[8]
        int pl = 0
        while pl < 8
            playLevel[pl] = 1
            pl = pl + 1
        endwhile
    endif
    float into = Seconds(now - songStarted)
    int count = InstrumentIdles.Length
    int applied = -1
    int crowd = crowdMode
    while nextSection < endSection && nextSection < SectionStarts2.Length && SectionStarts2[nextSection] <= into + 0.05
        applied = nextSection
        crowd = SectionCrowd2[nextSection]
        nextSection = nextSection + 1
    endwhile
    if applied >= 0
        int k = 0
        while k < count && k < 8
            int level = SectionPlay2[applied * count + k]
            if SteadyShow
                level = 1
            endif
            if !(level == playLevel[k])
                debug.Trace("SkyrimFairAudio: instrument " + k + " level " + level + " at " + into + " s", 0)
            endif
            if !(level == 3 == (playLevel[k] == 3))
                if level == 3
                    Rest(Band, BandIdles, bandPlaying, InstrumentIdles[k])
                    Rest(Orchestra, OrchestraIdles, orchestraPlaying, InstrumentIdles[k])
                endif
            endif
            if !(level == playLevel[k]) && k < InstrumentTempo.Length && InstrumentTempo[k]
                InstrumentTempo[k].SetValue(level)
            endif
            playLevel[k] = level
            k = k + 1
        endwhile
        int mode = 1
        if applied < SectionSing2.Length && !SteadyShow
            mode = SectionSing2[applied]
        endif
        if !(mode == singMode)
            debug.Trace("SkyrimFairAudio: singers " + mode + " at " + into + " s", 0)
            int si = 0
            while si < singerNext.Length
                singerNext[si] = utility.GetCurrentGameTime()
                si = si + 1
            endwhile
        endif
        singMode = mode
        singing = mode > 0
    endif
    if !(crowd == crowdMode)
        debug.Trace("SkyrimFairAudio: crowd " + crowd + " at " + into + " s", 0)
        crowdMode = crowd
        CapDances(utility.GetCurrentGameTime())
    endif
EndFunction

Function SetTempo(int level)
    int k = 0
    while k < InstrumentTempo.Length
        if InstrumentTempo[k] && !(InstrumentTempo[k].GetValue() == level)
            InstrumentTempo[k].SetValue(level)
        endif
        k = k + 1
    endwhile
EndFunction

Function CapDances(float now)
    float perSecond = TimeScale.GetValue() / 86400.0
    int i = 0
    while i < Dancers2.Length && i < danceEnds.Length
        float cap = now + i % 8 * 0.5 * perSecond
        if danceEnds[i] > cap
            danceEnds[i] = cap
        endif
        i = i + 1
    endwhile
EndFunction

Function Fireworks()
    if !FireworksOn || FireworksOn.GetValue() < 0.5 || FireworkShells.Length == 0
        return
    endif
    int k = 0
    while k < FireworkSites.Length && k < FireworkAims.Length
        spell shell = FireworkShells[k % FireworkShells.Length]
        if shell && FireworkSites[k] && FireworkAims[k]
            shell.Cast(FireworkSites[k], FireworkAims[k])
        endif
        k = k + 1
        if k < FireworkSites.Length
            utility.Wait(FireworkStagger)
        endif
    endwhile
    float t = utility.GetCurrentGameTime()
    float hour = (t - math.Floor(t)) * 24.0
    int middle = FireworkSites.Length / 2
    if (hour >= 20.0 || hour < 5.0) && middle < FireworkAims.Length
        int n = 0
        while n < FireworkNightShells.Length
            utility.Wait(FireworkStagger)
            if FireworkNightShells[n]
                FireworkNightShells[n].Cast(FireworkSites[middle], FireworkAims[middle])
            endif
            n = n + 1
        endwhile
    endif
    debug.Trace("SkyrimFairAudio: fireworks after song " + track, 0)
EndFunction

Function CheckMoreDances()
    if moreDancesChecked
        return
    endif
    moreDancesChecked = true
    moreDancesFound = MoreDanceEvents.Length > 0 && !(game.GetFormFromFile(MoreDancesCheck, MoreDancesPlugin) == None)
    debug.Trace("SkyrimFairAudio: " + MoreDancesPlugin + " loaded: " + moreDancesFound, 0)
EndFunction

bool Function playing(idle instrument)
    int k = 0
    while k < InstrumentIdles.Length && k < playLevel.Length
        if InstrumentIdles[k] == instrument
            return !(playLevel[k] == 3)
        endif
        k = k + 1
    endwhile
    return true
EndFunction

Function FaceStage(bool[] which)
    if !StageSpeaker
        return
    endif
    float[] Start = new float[128]
    float[] turn = new float[128]
    int i = 0
    while i < Dancers2.Length && i < 128
        if which[i] && Dancers2[i] && Dancers2[i].Is3DLoaded()
            Start[i] = Dancers2[i].GetAngleZ()
            turn[i] = Dancers2[i].GetHeadingAngle(StageSpeaker)
        endif
        i = i + 1
    endwhile
    int steps = (FaceStageSteps as int)
    if steps < 1
        steps = 1
    endif
    int k = 1
    while k <= steps
        i = 0
        while i < Dancers2.Length && i < 128
            if (turn[i] > 10.0 || turn[i] < -10.0) && Dancers2[i] && Dancers2[i].Is3DLoaded()
                Dancers2[i].SetAngle(0.0, 0.0, Start[i] + turn[i] * k / steps)
            endif
            i = i + 1
        endwhile
        if k < steps
            utility.Wait(0.06)
        endif
        k = k + 1
    endwhile
EndFunction

Function Rest(actor[] players, idle[] idles, bool[] playing, idle instrument)
    int i = 0
    while i < players.Length && i < playing.Length && i < idles.Length
        if idles[i] == instrument && playing[i] && players[i] && players[i].Is3DLoaded()
            players[i].PlayIdle(BandStop)
            playing[i] = false
        endif
        i = i + 1
    endwhile
EndFunction

Function Dance()
    idle[] idles = DanceIdles
    float[] lengths = DanceLengths
    if crowdMode == 1 && ClapIdles.Length > 0
        idles = ClapIdles
        lengths = ClapLengths
    elseif crowdMode == 2 && CheerIdles.Length > 0
        idles = CheerIdles
        lengths = CheerIdleLengths
    endif
    if idles.Length == 0
        return
    endif
    if dancing.Length < Dancers2.Length
        dancing = new bool[128]
        danceEnds = new float[128]
        dancePlays = new int[128]
    endif
    if danceMode.Length < Dancers2.Length
        danceMode = new int[128]
    endif
    if inMoreDance.Length < Dancers2.Length
        inMoreDance = new bool[128]
    endif
    CheckMoreDances()
    float now = utility.GetCurrentGameTime()
    float perSecond = TimeScale.GetValue() / 86400.0
    danceWake = 0.0
    bool[] turning = new bool[128]
    bool anyTurn = false
    int[] todo = new int[128]
    idle[] moves = new idle[128]
    float[] clips = new float[128]
    string[] events = new string[128]
    bool settle = false
    int i = 0
    while i < Dancers2.Length && i < dancing.Length
        if (!dancing[i] || now >= danceEnds[i]) && Dancers2[i] && Dancers2[i].Is3DLoaded()
            int which = (i + dancePlays[i]) % idles.Length
            moves[i] = idles[which]
            clips[i] = 6.0
            if which < lengths.Length
                clips[i] = lengths[which]
            endif
            todo[i] = 2
            if crowdMode == 0 && moreDancesFound
                int d = (i * 2 + dancePlays[i]) % MoreDanceEvents.Length
                events[i] = MoreDanceEvents[d]
                clips[i] = MoreDanceLengths[d]
                todo[i] = 1
            endif
            if todo[i] == 1 || inMoreDance[i]
                debug.SendAnimationEvent(Dancers2[i], "IdleForceDefaultState")
                settle = true
            endif
        endif
        i = i + 1
    endwhile
    if settle
        utility.Wait(0.1)
        now = utility.GetCurrentGameTime()
    endif
    i = 0
    while i < Dancers2.Length && i < dancing.Length
        bool started = false
        if todo[i] == 1
            debug.SendAnimationEvent(Dancers2[i], events[i])
            inMoreDance[i] = true
            started = true
        elseif todo[i] == 2
            if Dancers2[i].PlayIdle(moves[i])
                inMoreDance[i] = false
                started = true
            endif
        endif
        if started
            if crowdMode > 0 && !(danceMode[i] == crowdMode)
                turning[i] = true
                anyTurn = true
            endif
            danceMode[i] = crowdMode
            dancing[i] = true
            dancePlays[i] = dancePlays[i] + 1
            danceEnds[i] = now + clips[i] * perSecond
        endif
        if dancing[i] && (danceWake == 0.0 || danceEnds[i] < danceWake)
            danceWake = danceEnds[i]
        endif
        i = i + 1
    endwhile
    if anyTurn
        FaceStage(turning)
    endif
EndFunction

Function Sing(float now)
    if nextLine < 0 || Singers.Length == 0
        return
    endif
    float into = Seconds(now - songStarted)
    while nextLine < endLine && nextLine < SingerStarts2.Length && SingerStarts2[nextLine] <= into + 0.05
        int i = 0
        while i < Singers.Length && singing
            if Singers[i] && Singers[i].Is3DLoaded()
                Singers[i].Say(SingerTopics2[nextLine], None, false)
            endif
            i = i + 1
        endwhile
        nextLine = nextLine + 1
    endwhile
EndFunction

Function FolkDance(float now)
    if !FolkIdle || FolkDancers.Length == 0 || folkOn && now < folkNext
        return
    endif
    int i = 0
    while i < FolkDancers.Length
        if !FolkDancers[i] || !FolkDancers[i].Is3DLoaded()
            return
        endif
        i = i + 1
    endwhile
    i = 0
    while i < FolkDancers.Length
        FolkDancers[i].PlayIdle(FolkIdle)
        i = i + 1
    endwhile
    folkOn = true
    folkNext = now + FolkClipLength * TimeScale.GetValue() / 86400.0
EndFunction

Function cheer()
    if stepOn && !(stepApplied == 0.0)
        SingerOffset(0.0)
    endif
    int S = 0
    while SingerEndMove && S < Singers.Length
        if Singers[S] && Singers[S].Is3DLoaded()
            Singers[S].PlayIdle(SingerEndMove)
        endif
        S = S + 1
    endwhile
    if CheerIdles.Length > 0
        crowdMode = 2
        CapDances(utility.GetCurrentGameTime())
    endif
    nextLine = -1
    int i = 0
    while i < FolkDancers.Length
        if FolkDancers[i] && FolkDancers[i].Is3DLoaded()
            FolkDancers[i].PlayIdle(BandStop)
        endif
        i = i + 1
    endwhile
    folkOn = false
EndFunction

Function QueueArchers()
    if archerPending.Length < Archers.Length
        archerPending = new bool[32]
    endif
    int i = 0
    while i < Archers.Length && i < archerPending.Length
        archerPending[i] = true
        i = i + 1
    endwhile
EndFunction

Function ResetArchers()
    if ArcherHold && !(ArcherHold.GetValue() == 0.0)
        ArcherHold.SetValue(0.0)
    endif
    int i = 0
    while i < Archers.Length && i < archerPending.Length
        if archerPending[i] && Archers[i] && Archers[i].Is3DLoaded()
            objectreference stand = Archers[i].GetLinkedRef()
            if stand
                Archers[i].MoveTo(stand, 0.0, 0.0, 0.0, true)
            endif
            Archers[i].EvaluatePackage()
            archerPending[i] = false
            debug.Trace("SkyrimFairAudio: archer " + i + " on their stand, running " + Archers[i].GetCurrentPackage(), 0)
        endif
        i = i + 1
    endwhile
EndFunction

Function SetAmbience(bool duck)
    float level = 0.0
    if AmbienceEnabled.GetValue() >= 0.5
        level = AmbienceVolume.GetValue()
        if duck
            level = level * DuckDuringSong
        endif
    endif
    if !(level == ambienceLevel)
        AmbienceCategory.SetVolume(level)
        ambienceLevel = level
    endif
EndFunction

Function ReleaseArchers()
EndFunction


; Gore's Vigilant quest adds its story actors to CurrentFollowerFaction before
; recruitment. Its recruitment controller explicitly sets IsPlayerTeammate.
; Both fair entry and exit call BringCompanions, so this guard covers both.
bool Function AuthoriaFairTravelAllowed(actor mate)
    if mate.IsPlayerTeammate()
        return true
    endif
    if mate == (Game.GetFormFromFile(0x0316B1, "Gore - Vigilant.esp") as actor) || mate == (Game.GetFormFromFile(0x0316B2, "Gore - Vigilant.esp") as actor) || mate == (Game.GetFormFromFile(0x0316B3, "Gore - Vigilant.esp") as actor)
        Debug.Trace("AuthoriaFairCompanions: skipped unrecruited Vigilant Gore " + mate)
        return false
    endif
    return true
EndFunction
; Explicit recovery ONLY for the fresh test save affected before recruitment.
; Console: cqf SkyrimFairAudioQuest AuthoriaRestoreGores
; Never called automatically. No factions, quests, inventory, or enable state edited.
Function AuthoriaRestoreGores()
    AuthoriaRestoreOneGore(Game.GetFormFromFile(0x0316B1, "Gore - Vigilant.esp") as actor)
    AuthoriaRestoreOneGore(Game.GetFormFromFile(0x0316B2, "Gore - Vigilant.esp") as actor)
    AuthoriaRestoreOneGore(Game.GetFormFromFile(0x0316B3, "Gore - Vigilant.esp") as actor)
EndFunction

Function AuthoriaRestoreOneGore(actor mate)
    if mate && !mate.IsPlayerTeammate() && !mate.IsDead()
        mate.MoveToMyEditorLocation()
        Debug.Trace("AuthoriaFairCompanions: returned unrecruited Gore to editor location " + mate)
    else
        Debug.Trace("AuthoriaFairCompanions: recovery skipped missing, recruited, or dead Gore " + mate)
    endif
EndFunction
