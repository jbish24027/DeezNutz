Authoria - No Ammo Weight

Adds Enable Ammo Weight and Enable Septim Weight toggles to the Requiem MCM. Both options default to enabled, preserving Requiem behavior until disabled.

When ammo weight is disabled, the override removes Requiem's hidden ammo-weight dummy weapons, hides the quiver display item, and skips future ammo weight bookkeeping. Re-enabling rescans the player's current ammunition and rebuilds the quiver weight.

When Septim weight is disabled, the override sets Septims to zero weight, hides the Coin Purse display item, sets its weight to zero, and skips future gold-weight updates. Re-enabling restores Requiem's Septim weight and recalculates from the player's current Septim count.

No plugin records are included. The scripts use MCM Helper global settings plus ModEvents, so the existing Requiem VMAD properties are sufficient.
