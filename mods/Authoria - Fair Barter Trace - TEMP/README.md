# Fair barter trace — prepared, NOT installed

Compiled successfully on 20 October 2026 against installed SKSE/vanilla imports. This temporary diagnostic overrides only SkyrimFairStallCounter.pex. Preserves its four properties and original player/keeper/dead/3D checks; adds trace output and a one-shot menu observation after 0.5 seconds. No background polling, new quests, vendor edits or inventory resets.

Install as a temporary separate mod after The Wanderer's Fair in MO2 file priority, only with MO2/game closed. No ESP or generator reruns. Preserve the fixed order and Outputs block. Confirm its script wins before testing. Not installed by this diagnostic pass.

Test: fully restart Skyrim, load the affected save, activate any fair Browse counter once, and leave an opened shop menu open at least two seconds. Then quit and inspect Papyrus.0.log for `AuthoriaFairTrade:`. Existing logging was enabled in the latest available session; verify before interpreting missing output. A screenshot of the prompt is useful but remembering the stall name is unnecessary: the trace records its reference.

Interpretation:
- No activated trace: investigate script activation/loading or severe delay; absence alone is not proof which.
- Lookup None: runtime keeper resolution failed.
- Dead or unloaded keeper: original guard blocks trade; investigate why.
- Calling/returned but menu false: request reached native barter; inspect actor's runtime vendor eligibility/faction and menu conditions. A delayed menu or closing it too quickly can also produce false.
- Menu true: it opened at the sampling moment; observe any later closure separately.

Remove the temporary override after collecting evidence and restart the game. Original script remains untouched. This is diagnostic instrumentation, not a claimed fix.
