local frame = CreateFrame("Frame", "AgroMeterFrame")

local text = TargetFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
text:SetPoint("BOTTOM", TargetFramePortrait, "TOP", 0, 4)
text:SetDrawLayer("OVERLAY", 7)
text:SetTextColor(1, 0.82, 0)
text:Hide()
local agroIcon = "|TInterface\\Icons\\Ability_Warrior_Challange:18:18:0:0|t"

local function UpdateThreatText()
    if GetNumPartyMembers() == 0 and GetNumRaidMembers() == 0 then
        text:Hide()
        return
    end

    if not UnitExists("target") or not UnitCanAttack("player", "target") then
        text:Hide()
        return
    end

    local isTanking, _, scaledPercent = UnitDetailedThreatSituation("player", "target")
    if not isTanking and not scaledPercent then
        text:Hide()
        return
    end

    if isTanking then
        text:SetText(agroIcon .. " 100%")
    else
        text:SetFormattedText("%s %.0f%%", agroIcon, scaledPercent)
    end

    text:Show()
end

frame:SetScript("OnEvent", UpdateThreatText)
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_TARGET_CHANGED")
frame:RegisterEvent("PARTY_MEMBERS_CHANGED")
frame:RegisterEvent("RAID_ROSTER_UPDATE")
frame:RegisterEvent("UNIT_THREAT_LIST_UPDATE")
frame:RegisterEvent("UNIT_THREAT_SITUATION_UPDATE")
