-- census-render.lua — render the census (census/summary.tsv, census/hits.tsv) and the hand-read
-- verdicts (census/verdicts.tsv, census/issues.tsv) into the Markdown tables of LibKa0s
-- docs/api/CONSUMERS.md, and the per-document "no consumer" lines.
--
-- Pure Lua 5.1. Run from this folder (plan-data/):
--
--   lua census-render.lua table   > census/consumers-table.md   # every export, one row each
--   lua census-render.lua zero    > census/zero-table.md        # the zero-consumer set
--   lua census-render.lua doclines                              # Major|section|line, for the docs
--
-- census/issues.tsv maps a host-duplicate or suspect-shape verdict to the issue filed for it:
-- `major<TAB>member<TAB>ref` (ref like `KickCD#40`). Absent, the verdict cell says "issue pending".

local MODE = arg[1] or "table"

local function readTSV(path)
  local rows, header = {}, nil
  local f = io.open(path, "rb")
  if not f then return rows end
  for line in f:lines() do
    line = line:gsub("\r$", "")
    local cells = {}
    for c in (line .. "\t"):gmatch("([^\t]*)\t") do cells[#cells + 1] = c end
    if not header then header = cells
    else
      local row = {}
      for i, h in ipairs(header) do row[h] = cells[i] or "" end
      rows[#rows + 1] = row
    end
  end
  f:close()
  return rows
end

local function short(major) return (major:gsub("^LibKa0s%-", ""):gsub("%-1%.0$", "")) end

local summary = readTSV("census/summary.tsv")
local hits = readTSV("census/hits.tsv")
local verdicts = {}
for _, v in ipairs(readTSV("census/verdicts.tsv")) do
  verdicts[v.major .. "|" .. v.kind .. "|" .. v.member] = v
end
local issues = {}
for _, r in ipairs(readTSV("census/issues.tsv")) do issues[r.major .. "|" .. r.member] = r.ref end

-- First production call per (major, kind, member, addon).
local firstCall = {}
for _, h in ipairs(hits) do
  if h.class == "call" then
    local k = h.major .. "|" .. h.kind .. "|" .. h.member
    firstCall[k] = firstCall[k] or {}
    if not firstCall[k][h.addon] then firstCall[k][h.addon] = h.location end
  end
end

local function exportName(kind, member)
  if kind == "lib" then return "`lib." .. member .. "`" end
  if kind == "instance" then return "`" .. member .. "` (instance)" end
  return "`" .. member .. "` (descriptor)"
end

local function hostsOf(s)
  local out = {}
  for h in (s.callHosts or ""):gmatch("[^,]+") do out[#out + 1] = h end
  return out
end

local function consumersCell(s, key)
  local hs = hostsOf(s)
  if #hs == 0 then return "none" end
  if #hs <= 3 then
    local parts = {}
    for _, h in ipairs(hs) do
      local loc = firstCall[key] and firstCall[key][h]
      parts[#parts + 1] = loc and ("%s `%s`"):format(h, loc) or h
    end
    return table.concat(parts, "; ")
  end
  if #hs == 11 then return "all 11" end
  return ("%d: %s"):format(#hs, table.concat(hs, ", "))
end

local function classCell(s)
  local parts = { ("call %s"):format(s.call) }
  if tonumber(s.namecall) > 0 then parts[#parts + 1] = "name-only " .. s.namecall end
  if tonumber(s.duplicate) > 0 then parts[#parts + 1] = "def " .. s.duplicate end
  if tonumber(s.stub) > 0 then parts[#parts + 1] = "stub " .. s.stub end
  if tonumber(s.test) > 0 then parts[#parts + 1] = "test " .. s.test end
  return table.concat(parts, " · ")
end

local VERDICT_WORD = {
  ["documented"] = "zero — kept, documented",
  ["host-duplicate"] = "zero — host duplicate",
  ["deliberate-host-copy"] = "zero — deliberate host copy",
  ["suspect-shape"] = "zero — suspect shape",
}

local function verdictCell(s, key)
  local n = #hostsOf(s)
  local v = verdicts[key]
  if n == 0 then
    if not v then return "zero — UNREAD" end
    local word = VERDICT_WORD[v.verdict] or v.verdict
    if v.verdict == "host-duplicate" or v.verdict == "suspect-shape" then
      local ref = issues[short(s.major) .. "|" .. s.member]
      word = word .. " → " .. (ref or "issue pending")
    end
    return word
  end
  if n <= 2 then return "thin (" .. n .. ")" end
  return "consumed (" .. n .. ")"
end

local function esc(s) return (s:gsub("|", "\\|")) end

if MODE == "table" or MODE == "zero" then
  print(MODE == "zero" and "| Major | Export | Evidence | Hits by class | Verdict |"
    or "| Major | Export | Consumers (first production call per host) | Hits by class | Verdict |")
  print("|---|---|---|---|---|")
  for _, s in ipairs(summary) do
    local key = short(s.major) .. "|" .. s.kind .. "|" .. s.member
    local fkey = s.major .. "|" .. s.kind .. "|" .. s.member
    if MODE == "table" or #hostsOf(s) == 0 then
      local cells = { short(s.major), exportName(s.kind, s.member), consumersCell(s, fkey),
        classCell(s), verdictCell(s, key) }
      if MODE == "zero" then
        local v = verdicts[key]
        cells[3] = v and esc(v.evidence) or "?"
      end
      print("| " .. table.concat(cells, " | ") .. " |")
    end
  end
elseif MODE == "doclines" then
  for _, s in ipairs(summary) do
    if #hostsOf(s) == 0 then
      local key = short(s.major) .. "|" .. s.kind .. "|" .. s.member
      local v = verdicts[key]
      local tail = ""
      if v and (v.verdict == "host-duplicate" or v.verdict == "suspect-shape") then
        tail = " (" .. (issues[short(s.major) .. "|" .. s.member] or "issue pending") .. ")"
      end
      local name = s.kind == "lib" and ("lib." .. s.member) or s.member
      print(("%s\t%s\t- `%s`: no consumer as of v1.66.0, kept because %s.%s"):format(
        short(s.major), s.kind, name, v and v.kept_because or "?", tail))
    end
  end
end
