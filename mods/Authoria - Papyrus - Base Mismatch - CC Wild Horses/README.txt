Creation Club Wild Horses - Papyrus Script Binding Fix

Plugin: Creation Club Wild Horses - Papyrus Script Binding Fix.esp

Removes an ObjectReference script from a quest alias; Papyrus cannot bind that base type to an alias, and the HostlerRef alias has no resolved reference in this record.

This reversible patch only changes VMAD script attachment records to stop Papyrus base-type mismatch binding errors. It does not edit installed mod files or ship Papyrus stubs.
