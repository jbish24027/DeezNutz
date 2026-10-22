ScriptName RMS_InventoryScript extends Quest
{Authoria Requiem patch 2026-09-06 for Rovan's Market Stall 1.4.1.
 Only the Speech bonus differs from the shipped script, in BOTH places 1.4.1 computes a price
 (CalculateRetailPrice() for the ledger/follower sales and SellOneItem() for a customer sale): it scales
 the stall the way Speech scales Requiem's own merchants (fBarterMax 4 at Speech 0 -> fBarterMin 3 at
 Speech 100 = +33% relative), instead of the shipped flat +75% of item value at Speech 100. The 1.4.0
 additions (enchantment power value, tempering bonus, the tiered reputation multiplier, the hold
 multiplier, the tender's Speech) are kept as shipped. Everything else is the shipped 1.4.1 logic,
 decompiled and recompiled unchanged.}

int[] SellableQuantities
Form[] SellableItems
int[] SellableValues

globalvariable Property rms_StallReputation Auto

location Property HaafingarHoldLocation Auto

objectreference Property MerchandiseRef Auto

location Property WinterholdHoldLocation Auto

location Property HjaalmarchHoldLocation Auto

location Property FalkreathHoldLocation Auto

location Property EastmarchHoldLocation Auto

location Property PaleHoldLocation Auto

location Property RiftHoldLocation Auto

keyword Property LocTypeHold Auto

location Property ReachHoldLocation Auto

location Property WhiterunHoldLocation Auto

container Property MerchandiseContainer Auto

globalvariable Property PriceMultiplier Auto

Event OnInit()
    InitializeInventory()
EndEvent

Function InitializeInventory()
    SellableItems = new Form[1]
    SellableItems[0] = None
    SellableQuantities = new int[1]
    SellableQuantities[0] = 0
    SellableValues = new int[1]
    SellableValues[0] = 0
EndFunction

Function SetMerchandiseReference(objectreference NewReference)
    MerchandiseRef = NewReference
EndFunction

float Function GetRegionalMultiplier()
    location cur = None
    if !(MerchandiseRef == None)
        cur = MerchandiseRef.GetCurrentLocation()
    endif
    if cur == None
        actor p = game.GetPlayer()
        if !(p == None)
            cur = p.GetCurrentLocation()
        endif
    endif
    if cur == None
        return 1.0
    endif
    if !(HaafingarHoldLocation == None) && cur.IsSameLocation(HaafingarHoldLocation, LocTypeHold)
        return 1.15
    endif
    if !(ReachHoldLocation == None) && cur.IsSameLocation(ReachHoldLocation, LocTypeHold)
        return 1.15
    endif
    if !(WhiterunHoldLocation == None) && cur.IsSameLocation(WhiterunHoldLocation, LocTypeHold)
        return 1.0
    endif
    if !(RiftHoldLocation == None) && cur.IsSameLocation(RiftHoldLocation, LocTypeHold)
        return 1.0
    endif
    if !(EastmarchHoldLocation == None) && cur.IsSameLocation(EastmarchHoldLocation, LocTypeHold)
        return 0.95
    endif
    if !(FalkreathHoldLocation == None) && cur.IsSameLocation(FalkreathHoldLocation, LocTypeHold)
        return 0.95
    endif
    if !(PaleHoldLocation == None) && cur.IsSameLocation(PaleHoldLocation, LocTypeHold)
        return 0.85
    endif
    if !(HjaalmarchHoldLocation == None) && cur.IsSameLocation(HjaalmarchHoldLocation, LocTypeHold)
        return 0.85
    endif
    if !(WinterholdHoldLocation == None) && cur.IsSameLocation(WinterholdHoldLocation, LocTypeHold)
        return 0.85
    endif
    return 1.0
EndFunction

float Function GetReputationMultiplier()
    if !(rms_StallReputation == None)
        float rep = rms_StallReputation.GetValue()
        if rep >= 100.0
            return 1.2
        elseif rep >= 75.0
            return 1.15
        elseif rep >= 50.0
            return 1.1
        elseif rep >= 25.0
            return 1.05
        endif
    endif
    return 1.0
EndFunction

int Function GetEnchantmentPowerValue(Enchantment akEnch)
    if akEnch == None
        return 0
    endif
    int numEffects = akEnch.GetNumEffects()
    if numEffects <= 0
        return 0
    endif
    float totalCalculatedCost = 0.0
    int i = 0
    while i < numEffects
        magiceffect mgef = akEnch.GetNthEffectMagicEffect(i)
        if !(mgef == None)
            float baseCost = mgef.GetBaseCost()
            if baseCost <= 0.0
                baseCost = 10.0
            endif
            float mag = akEnch.GetNthEffectMagnitude(i)
            int dur = akEnch.GetNthEffectDuration(i)
            if mag <= 0.0
                mag = 1.0
            endif
            float effectCost = baseCost * math.Pow(mag, 1.25) * 1.5
            if dur > 1
                effectCost = effectCost + dur * (baseCost * 0.75)
            endif
            totalCalculatedCost = totalCalculatedCost + effectCost
        endif
        i = i + 1
    endwhile
    return (totalCalculatedCost as int)
EndFunction

; Authoria: the decompiler drops parameter defaults; the shipped 1.4.1 caller inside this script
; (ScanInventory) passes no tender (baked None), so the default is restored to compile the same bytecode.
int Function CalculateRetailPrice(form ItemForm, actor TenderActor = None)
    if ItemForm == None
        return 0
    endif
    int baseVal = ItemForm.GetGoldValue()
    if baseVal <= 0
        baseVal = 1
    endif
    weapon wpn = (ItemForm as weapon)
    if !(wpn == None)
        Enchantment ench = wpn.GetEnchantment()
        if !(ench == None)
            baseVal = baseVal + GetEnchantmentPowerValue(ench)
        endif
    endif
    armor arm = (ItemForm as armor)
    if !(arm == None)
        Enchantment mangled_ench_0 = arm.GetEnchantment()
        if !(mangled_ench_0 == None)
            baseVal = baseVal + GetEnchantmentPowerValue(mangled_ench_0)
        endif
    endif
    float baseMult = 1.75
    if !(PriceMultiplier == None) && PriceMultiplier.GetValue() > 0.0
        baseMult = PriceMultiplier.GetValue()
    endif
    actor activeVendor = TenderActor
    if activeVendor == None
        activeVendor = game.GetPlayer()
    endif
    float speechBonus = 0.0
    if !(activeVendor == None)
        float speech = activeVendor.GetActorValue("Speechcraft")
        if speech > 100.0
            speech = 100.0
        endif
        if speech > 0.0
            ; Requiem patch. Shipped: speech / 100.0 * 0.75 (a flat +75% of value at Speech 100, whatever the
            ; multiplier). Requiem's merchants go from value/4 at Speech 0 to value/3 at Speech 100, a +33%
            ; relative gain over the skill: the bonus is a third of the base multiplier at Speech 100, linear.
            speechBonus = baseMult * (speech / 100.0) * 0.3333
        endif
    endif
    float regMult = GetRegionalMultiplier()
    float repMult = GetReputationMultiplier()
    float totalMultiplier = (baseMult + speechBonus) * regMult * repMult
    int finalPrice = ((baseVal * totalMultiplier) as int)
    if finalPrice < 1
        finalPrice = 1
    endif
    return finalPrice
EndFunction

Function ScanInventory()
    if MerchandiseRef == None
        InitializeInventory()
        return
    endif
    int totalDistinct = MerchandiseRef.GetNumItems()
    if totalDistinct <= 0
        InitializeInventory()
        return
    endif
    int validCount = 0
    int i = 0
    while i < totalDistinct
        form item = MerchandiseRef.GetNthForm(i)
        if !(item == None) && item.GetGoldValue() > 0 && !(item.GetFormID() == 15)
            if MerchandiseRef.GetItemCount(item) > 0
                validCount = validCount + 1
            endif
        endif
        i = i + 1
    endwhile
    if validCount == 0
        InitializeInventory()
        return
    endif
    SellableItems = utility.CreateFormArray(validCount)
    SellableQuantities = utility.CreateIntArray(validCount, 0)
    SellableValues = utility.CreateIntArray(validCount, 0)
    int insertIdx = 0
    i = 0
    while i < totalDistinct && insertIdx < validCount
        form mangled_item_1 = MerchandiseRef.GetNthForm(i)
        if !(mangled_item_1 == None) && mangled_item_1.GetGoldValue() > 0 && !(mangled_item_1.GetFormID() == 15)
            int qty = MerchandiseRef.GetItemCount(mangled_item_1)
            if qty > 0
                SellableItems[insertIdx] = mangled_item_1
                SellableQuantities[insertIdx] = qty
                SellableValues[insertIdx] = CalculateRetailPrice(mangled_item_1)
                insertIdx = insertIdx + 1
            endif
        endif
        i = i + 1
    endwhile
EndFunction

int Function GetSellableItemCount()
    if !SellableItems || SellableItems.Length <= 0
        return 0
    endif
    int count = 0
    int i = 0
    while i < SellableItems.Length
        if !(SellableItems[i] == None) && SellableQuantities[i] > 0
            count = count + 1
        endif
        i = i + 1
    endwhile
    return count
EndFunction

int Function GetTotalItemUnits()
    if MerchandiseRef == None
        return 0
    endif
    ScanInventory()
    if !SellableItems || SellableItems.Length <= 0
        return 0
    endif
    int total = 0
    int i = 0
    while i < SellableItems.Length
        if !(SellableItems[i] == None)
            total = total + MerchandiseRef.GetItemCount(SellableItems[i])
        endif
        i = i + 1
    endwhile
    return total
EndFunction

form Function GetRandomSellableItem()
    if MerchandiseRef == None
        return None
    endif
    ScanInventory()
    int validCount = GetSellableItemCount()
    if validCount <= 0
        return None
    endif
    int targetIdx = utility.RandomInt(1, validCount)
    int cur = 0
    int i = 0
    while i < SellableItems.Length
        if !(SellableItems[i] == None) && SellableQuantities[i] > 0
            cur = cur + 1
            if cur == targetIdx
                return SellableItems[i]
            endif
        endif
        i = i + 1
    endwhile
    return None
EndFunction

int Function SellOneItem(form ItemForm, actor TenderActor)
    if ItemForm == None || MerchandiseRef == None
        return 0
    endif
    if MerchandiseRef.GetItemCount(ItemForm) <= 0
        return 0
    endif
    objectreference itemInstance = MerchandiseRef.DropObject(ItemForm, 1)
    int baseVal = ItemForm.GetGoldValue()
    if baseVal <= 0
        baseVal = 1
    endif
    if !(itemInstance == None)
        Enchantment playerEnch = itemInstance.GetEnchantment()
        if !(playerEnch == None)
            baseVal = baseVal + GetEnchantmentPowerValue(playerEnch)
        else
            weapon w = (ItemForm as weapon)
            if !(w == None) && !(w.GetEnchantment() == None)
                baseVal = baseVal + GetEnchantmentPowerValue(w.GetEnchantment())
            endif
            armor a = (ItemForm as armor)
            if !(a == None) && !(a.GetEnchantment() == None)
                baseVal = baseVal + GetEnchantmentPowerValue(a.GetEnchantment())
            endif
        endif
        float healthPercent = itemInstance.GetItemHealthPercent()
        if healthPercent > 1.0
            float healthDelta = healthPercent - 1.0
            float smithingBonus = healthDelta * 250.0 + healthDelta * baseVal * 0.5
            baseVal = baseVal + (smithingBonus as int)
        endif
        itemInstance.DisableNoWait(false)
        itemInstance.Delete()
    else
        MerchandiseRef.RemoveItem(ItemForm, 1, true)
    endif
    float baseMult = 1.75
    if !(PriceMultiplier == None) && PriceMultiplier.GetValue() > 0.0
        baseMult = PriceMultiplier.GetValue()
    endif
    actor activeVendor = TenderActor
    if activeVendor == None
        activeVendor = game.GetPlayer()
    endif
    float speechBonus = 0.0
    if !(activeVendor == None)
        float speech = activeVendor.GetActorValue("Speechcraft")
        if speech > 100.0
            speech = 100.0
        endif
        if speech > 0.0
            ; Requiem patch. Shipped: speech / 100.0 * 0.75 (a flat +75% of value at Speech 100, whatever the
            ; multiplier). Requiem's merchants go from value/4 at Speech 0 to value/3 at Speech 100, a +33%
            ; relative gain over the skill: the bonus is a third of the base multiplier at Speech 100, linear.
            speechBonus = baseMult * (speech / 100.0) * 0.3333
        endif
    endif
    float regMult = GetRegionalMultiplier()
    float repMult = GetReputationMultiplier()
    float totalMultiplier = (baseMult + speechBonus) * regMult * repMult
    int finalPrice = ((baseVal * totalMultiplier) as int)
    if finalPrice < 1
        finalPrice = 1
    endif
    return finalPrice
EndFunction

