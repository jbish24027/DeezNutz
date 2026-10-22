compatibility and optimization patch for the combination of Animated Ships and Dynamic Boats at Docks - Animated Ships Patch.

Animated Ships schedules distant ships by enabling and disabling ship references and their linked passenger references. Dynamic Boats at Docks - Animated Ships Patch changes some of those placed ship references so their enabled state is controlled by an enable parent. That is valid ESP-side data, but vanilla Papyrus cannot directly enable or disable an object that has an enable state parent.

Without this script override, the Animated Ships scheduler can print Papyrus log errors like:

  cannot enable an object with an enable state parent
  Cannot call IsPlayerNearShipRef() on a None object


- Skip direct enable/disable calls on references that have an enable parent.
- Replace the unsafe EnableLinkChain path with a guarded linked-reference loop.
- Check ship script casts before calling ship functions.
- Avoid FormList.ToArray() allocations in schedule list processing.
- Add defensive null checks around ship refs, markers, player refs, managers, sounds, and trigger-linked refs.

