The original script calls UnregisterForUpdate from unload/finish cleanup events. those events can run after the active magic effect object is already unbound, producing repeated "no native object bound" Papyrus errors.

This override keeps the NPC Hallowed Flare AI behavior intact while:
- replacing cleanup-time UnregisterForUpdate calls with a local active/inactive flag
- restoring the missing combat-start RegisterForSingleUpdate call
- guarding missing combat targets and optional animation/sound properties
