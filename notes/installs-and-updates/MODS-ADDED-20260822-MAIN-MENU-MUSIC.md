# Main menu music - final state 2026-08-22

Playing: **Skyrim Lofi - Main Menu Replacer** (Nexus 38968 v1, file 153535, song by Mikel, 3:17).
Mod folder: mods\Skyrim Lofi - Main Menu Replacer, one file, Music\special\mus_maintheme.xwm (CRC 21285DB2, matches the archive).
Encoded 48 kbps / blockAlign 1008, byte-identical in format to the vanilla track. Archive staged in downloads\ with a hand-written .meta.
Enabled in all 4 profiles, in the Audio - Music block above Peaceful Nerevar Rising.

Required partner mod: **Authoria - Main Menu Video - No Audio Track** (see below). Without it nothing here is audible.

## The three things that decide this track

### 1. The path is hardcoded in the exe, and it is .xwm ONLY

SkyrimSE.exe contains exactly one main-theme string:

    \Data\Music\Special\MUS_MainTheme.xwm

There is no .wav variant and no MUSC/MUST record involved, so no plugin or patch can ever re-route it.
**A mus_maintheme.wav is completely inert.** Two were hidden in round 1 on the false assumption that a .wav
outranks an .xwm; that assumption was wrong, and hiding them changed nothing either way. They stay hidden
(harmless, and they are old menu songs the user replaced):
  - mods\Authoria - UI Positioning\Music\Special\mus_maintheme.wav.mohidden
  - mods\Peaceful Nerevar Rising\music\special\mus_maintheme.wav.mohidden

### 2. Main Menu Video silently suppresses the music

Its source bypasses the music trigger outright:

    if (Manager::GetSingleton()->IsPlayingVideoAudio()) { return true; }

and the mod page states "Main menu music is disabled if the video has an audio track".
MainCompWithSong_3.mp4 carries an AAC track, so no music file of any kind could be heard.
bPlayAudio = false is NOT a dependable off switch.

Fix: mod "Authoria - Main Menu Video - No Audio Track" holds the same video with the audio stream removed
(ffmpeg -an -c:v copy, video bitstream untouched). It overrides the original by filename at higher priority,
so the plugin still counts exactly 1 video. Confirmed working: po3_MainMenuVideo.log now reports 4355 frames
(the silent copy) instead of 4356 (the original). bPlayAudio is left false; with no audio track it is moot.

### 3. Everything else that owns this filename, and why it loses

  - mods\Main Menu Music - Touch the Sky - DISABLED. Wrong song (an orchestral Jeremy Soule homage, not lofi).
    Kept on disk; re-enable its line in modlist.txt to get it back.
  - mods\Phoenix Compendium\music\special\mus_maintheme.xwm - 2:14, loose, lower priority.
  - mods\Unofficial High Definition Audio Project - Music\UHDAP - MusicHQ.bsa - holds the vanilla track at
    192 kbps. A BSA always loses to a loose file. Found only by parsing the name tables of all 567 BSAs;
    a plain file search over mods\ misses archives entirely.

## Encoding rules for any future swap

Legal xWMA for this game, confirmed against three working files:
  - vanilla          48 kbps  blockAlign 1008
  - lofi (installed) 48 kbps  blockAlign 1008
  - UHDAP            192 kbps blockAlign 8192
Bethesda's own tool is at mods\Creation Kit Platform Extended for Skyrim\Root\Tools\LipGen\LipGenerator\xWMAEncode.exe
(ffmpeg.exe sits beside it). Native bitrates at 48000 Hz stereo: 48000, 64000, 96000, 160000, 192000.
Encoding a wav: xWMAEncode -b 192000 in.wav out.xwm

## Side note

Unslaad.esm's track zzzCrbMUSDovahkiinTrack points at Music\special\mus_maintheme.wav. Since a .wav at that
path is inert, that cue is unaffected by any of this.

## Revert

- Video's own song back: delete mod "Authoria - Main Menu Video - No Audio Track", set bPlayAudio = true.
- Touch the Sky back instead: flip its modlist line from - to + and disable the lofi mod.
- Modlist backups: _backups\2026-08-22 - main menu lofi swap\ , ...\2026-08-21 - main menu music fix round2\ ,
  ...\2026-08-21 - main menu music touch the sky\ (that last one also holds the original video INI).

## Test

Not tested in game. The lofi track is 3:17; vanilla is 3:56; Phoenix's is 2:14; Touch the Sky is 5:04.
