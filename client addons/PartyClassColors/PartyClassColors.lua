local frame = CreateFrame("Frame", "PartyClassColorsFrame")

local function UpdatePartyHealthBarColor(index)
    local unit = "party" .. index
    local healthBar = _G["PartyMemberFrame" .. index .. "HealthBar"]
    if not healthBar then
        return
    end

    if not UnitExists(unit) then
        healthBar:SetStatusBarColor(0, 1, 0)
        return
    end

    local _, class = UnitClass(unit)
    local color = class and RAID_CLASS_COLORS[class]
    if color then
        healthBar:SetStatusBarColor(color.r, color.g, color.b)
    end
end

local function UpdateTargetHealthBarColor()
    if not UnitExists("target") or not UnitIsPlayer("target") or UnitIsUnit("target", "player") then
        return
    end

    local _, class = UnitClass("target")
    local color = class and RAID_CLASS_COLORS[class]
    if color then
        TargetFrameHealthBar:SetStatusBarColor(color.r, color.g, color.b)
    end
end

local function UpdateAllPartyHealthBarColors()
    for i = 1, 4 do
        UpdatePartyHealthBarColor(i)
    end

    UpdateTargetHealthBarColor()
end

frame:SetScript("OnEvent", UpdateAllPartyHealthBarColors)
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PARTY_MEMBERS_CHANGED")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("UNIT_NAME_UPDATE")
frame:RegisterEvent("UNIT_MODEL_CHANGED")

hooksecurefunc("UnitFrameHealthBar_Update", function(statusbar, unit)
    if unit == "target" then
        UpdateTargetHealthBarColor()
    elseif unit == "party1" then
        UpdatePartyHealthBarColor(1)
    elseif unit == "party2" then
        UpdatePartyHealthBarColor(2)
    elseif unit == "party3" then
        UpdatePartyHealthBarColor(3)
    elseif unit == "party4" then
        UpdatePartyHealthBarColor(4)
    end
end)

hooksecurefunc("HealthBar_OnValueChanged", function(statusbar)
    if statusbar == TargetFrameHealthBar then
        UpdateTargetHealthBarColor()
    elseif statusbar == PartyMemberFrame1HealthBar then
        UpdatePartyHealthBarColor(1)
    elseif statusbar == PartyMemberFrame2HealthBar then
        UpdatePartyHealthBarColor(2)
    elseif statusbar == PartyMemberFrame3HealthBar then
        UpdatePartyHealthBarColor(3)
    elseif statusbar == PartyMemberFrame4HealthBar then
        UpdatePartyHealthBarColor(4)
    end
end)
