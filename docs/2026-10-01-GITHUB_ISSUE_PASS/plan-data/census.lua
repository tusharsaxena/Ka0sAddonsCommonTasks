-- census.lua — the LibKa0s zero-consumer export census (GI-LK-13, LibKa0s#9).
--
-- Pure Lua 5.1. Run it FROM THE LibKa0s REPO ROOT, because it loads the library through LibKa0s's
-- own mock exactly as tools/gen-api-members.lua does:
--
--   cd ../LibKa0s
--   /home/tushar/.claude/wow-addon/bin/ka0s-bounded \
--     lua ../Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS/plan-data/census.lua \
--         .. ../Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS/plan-data/census
--
--   arg[1]  the GIT root holding every sibling repo (default "..")
--   arg[2]  the output folder, which must exist (default ".")
--
-- WHAT IT ENUMERATES, per major in tests/majors.lua:
--   lib         every public member of the live library table (Kit.publicMembers, the rule
--               docs/api/<Major>/members-*.json is generated with), i.e. `lib.X` exports
--   instance    every public member a major's own files define on the INSTANCE that lib:New hands
--               back, found statically: `function R.X(` / `function R:X(` / `R.X =` where R is the
--               major's instance local (Sl, D, O, P, S, B, LC, Lb)
--   descriptor  every field the major's files read off a descriptor as `d.<field>`
--
-- WHAT IT SEARCHES: every git-tracked .lua file of every addon in WowAddonStandards'
-- standards/ADDONS.md "In-scope addons" table, excluding libs/ and tests/_kit/.
--
-- HOW EACH HIT IS CLASSIFIED (mechanically; the verdicts in LibKa0s docs/api/CONSUMERS.md were
-- then read by hand for every export whose verdict depended on the class):
--   stub        inside a degradation block: `if not <libVar> then ... end` or the `else` arm of
--               `if <libVar> then`, where <libVar> was assigned from LibStub(...) in that file
--   duplicate   a definition of the same name in host code (`function ...X(`, `X = function`),
--               unless the same line forwards to `.X(` / `:X(` on another table (a call)
--   call        a member access `.X` / `:X` in code whose receiver resolves to the member's major
--               (see "receivers" below)
--   namecall    a member access whose receiver does not resolve (`self:Stop()`, a parameter,
--               another table's member of the same name): listed, never counted as a consumer
--   comment     only in a comment
--   string      only inside a string literal
--   bare        any other textual mention (a local of the same name, an alias, ...)
-- A hit in tests/ is prefixed `test:`; tests are evidence but never a consumer.
-- A DESCRIPTOR FIELD is not classified textually: it counts as a call only where it is a top-level
-- key of the descriptor literal handed to `<receiver>:New(` / `CopyWindow(` (see "descriptor
-- literals" below).
--
-- OUTPUT
--   hits.tsv     major, kind, member, addon, file:line, class, the trimmed line
--   summary.tsv  major, kind, member, then counts: call / namecall / duplicate / stub / other /
--                test, the addons with a call, and the addons with a namecall
-- hits.tsv is filtered as the comment above its writer says (string literals never; widely
-- consumed members capped to five hits per addon per class); summary.tsv counts every hit.
-- census-render.lua turns these, plus the hand-read census/verdicts.tsv and census/issues.tsv,
-- into the tables of LibKa0s docs/api/CONSUMERS.md.

-- The kit's resource guard (tests/_kit/framework.lua) re-launches this script with a marker
-- argument, `--kit-guarded`, so positional arguments are read with it filtered out.
local ARGS = {}
for _, a in ipairs(arg or {}) do
  if a ~= "--kit-guarded" then ARGS[#ARGS + 1] = a end
end
local GIT = ARGS[1] or ".."
local OUT = ARGS[2] or "."

-- ── the members ─────────────────────────────────────────────────────────────────────────────

local MAJORS = dofile("tests/majors.lua")
local Kit = dofile("tests/_kit/framework.lua")
local Loader = dofile("tests/_kit/loader.lua")
local mocks = dofile("tests/wow_mock.lua")()
Loader.loadAll(Loader.xmlFiles("LibKa0s/LibKa0s.xml"), nil, mocks)

local INSTANCE = {
  ["LibKa0s-Bus-1.0"] = "B", ["LibKa0s-DebugLog-1.0"] = "D", ["LibKa0s-Lifecycle-1.0"] = "LC",
  ["LibKa0s-Launcher-1.0"] = "Lb", ["LibKa0s-Schema-1.0"] = "S", ["LibKa0s-Slash-1.0"] = "Sl",
  ["LibKa0s-Options-1.0"] = "O", ["LibKa0s-Perf-1.0"] = "P",
}

local function readLines(path)
  local f = io.open(path, "rb")
  if not f then return nil end
  local lines = {}
  for line in f:lines() do lines[#lines + 1] = (line:gsub("\r$", "")) end
  f:close()
  return lines
end

local function escape(s) return (s:gsub("[%^%$%(%)%%%.%[%]%*%+%-%?]", "%%%0")) end

local members = {}   -- { major=, kind=, name= }
local seen = {}
local function addMember(major, kind, name)
  local key = major .. "\0" .. kind .. "\0" .. name
  if seen[key] then return end
  seen[key] = true
  members[#members + 1] = { major = major, kind = kind, name = name }
end

for _, m in ipairs(MAJORS) do
  local lib = mocks.LibStub(m.major, true)
  for _, mem in ipairs(Kit.publicMembers(lib)) do addMember(m.major, "lib", mem.name) end
  local R = INSTANCE[m.major]
  local inst, desc = {}, {}
  for _, file in ipairs(m.files) do
    for _, line in ipairs(readLines("LibKa0s/" .. file .. ".lua") or {}) do
      if R then
        local r = escape(R)
        local n = line:match("^%s*function%s+" .. r .. "[.:]([%a][%w_]*)%s*%(")
          or line:match("^%s*" .. r .. "%.([%a][%w_]*)%s*=[^=]")
        if n then inst[n] = true end
      end
      local codePart = line:match("^(.-)%-%-") or line
      for f in codePart:gmatch("%f[%w_]d%.([%a_][%w_]*)") do desc[f] = true end
    end
  end
  local function sortedKeys(t)
    local out = {}
    for k in pairs(t) do out[#out + 1] = k end
    table.sort(out)
    return out
  end
  for _, n in ipairs(sortedKeys(inst)) do addMember(m.major, "instance", n) end
  for _, n in ipairs(sortedKeys(desc)) do addMember(m.major, "descriptor", n) end
end

-- ── the addons and their files ──────────────────────────────────────────────────────────────

local function addons()
  local out, inTable = {}, false
  for _, line in ipairs(assert(readLines(GIT .. "/WowAddonStandards/standards/ADDONS.md"),
      "cannot read ADDONS.md under " .. GIT)) do
    if line:match("^## In%-scope addons") then inTable = true
    elseif line:match("^## ") then inTable = false
    elseif inTable then
      local folder = line:match("^|[^|]+|%s*%[`%.%./%.%./([%w_]+)/`%]")
      if folder then out[#out + 1] = folder end
    end
  end
  return out
end

local function trackedLua(repo)
  local p = assert(io.popen("git -C '" .. repo .. "' ls-files '*.lua'"))
  local out = {}
  for path in p:lines() do
    if not path:match("^libs/") and not path:match("^tests/_kit/") then out[#out + 1] = path end
  end
  p:close()
  table.sort(out)
  return out
end

-- Per file: the code part of each line (comments removed), and which lines sit in a stub block.
local function analyse(lines)
  local code, inLong = {}, false
  for i, line in ipairs(lines) do
    local c = line
    if inLong then
      local e = c:find("]]", 1, true)
      if e then c = c:sub(e + 2); inLong = false else c = "" end
    end
    local s = c:find("--", 1, true)
    if s then
      if c:sub(s, s + 3) == "--[[" and not c:find("]]", s + 4, true) then inLong = true end
      c = c:sub(1, s - 1)
    end
    code[i] = c
  end
  local libVars = {}
  for _, line in ipairs(lines) do
    local v = line:match("^%s*local%s+([%w_]+)%s*=.-LibStub")
    if v then libVars[v] = true end
  end
  local stub = {}
  local function closeAt(from, indent, word)
    for j = from, #lines do
      if lines[j]:match("^" .. indent .. word .. "%f[^%w_]") then return j end
    end
  end
  for i, line in ipairs(lines) do
    local indent, v = line:match("^(%s*)if%s+not%s+([%w_]+)%s+then%s*$")
    if v and libVars[v] then
      local e = closeAt(i + 1, indent, "end") or i
      for j = i, e do stub[j] = true end
    end
    indent, v = line:match("^(%s*)if%s+([%w_]+)%s+then%s*$")
    if v and libVars[v] then
      local e = closeAt(i + 1, indent, "end")
      if e then
        for j = i + 1, e do
          if lines[j]:match("^" .. indent .. "else%s*$") then
            for k = j, e do stub[k] = true end
            break
          end
        end
      end
    end
  end
  return code, stub
end

local function inString(code, pos)
  local q
  local i = 1
  while i < pos do
    local ch = code:sub(i, i)
    if q then
      if ch == "\\" then i = i + 1 elseif ch == q then q = nil end
    elseif ch == '"' or ch == "'" then q = ch end
    i = i + 1
  end
  return q ~= nil
end

local function classify(kind, name, code, isStub, line)
  local pat = "%f[%w_]" .. escape(name) .. "%f[^%w_]"
  if not line:find(pat) then return nil end
  if isStub then return "stub" end
  local n = escape(name)
  -- A descriptor field PASSED as a function (`onClear = function(...)`) is a pass, not a host
  -- definition, so the key shapes are tested before the definition shapes for descriptors.
  if kind == "descriptor" and not code:find("^%s*local%s") and (code:find("[{,;]%s*" .. n .. "%s*=[^=]")
      or code:find("^%s*" .. n .. "%s*=[^=]") or code:find("[%w_%]]%." .. n .. "%s*=[^=]")) then
    return "call"
  end
  -- A host definition of the same name is a duplicate, unless the same line forwards to a member
  -- of that name on another table (`function DL.ShowCopy() D:ShowCopy() end`): that is a one-line
  -- forwarder onto the library instance, which is a call.
  for _, def in ipairs({ "function%s+[%w_.:]*[.:]" .. n .. "%s*%b()", "function%s+" .. n .. "%s*%b()",
      "%f[%w_]" .. n .. "%s*=%s*function%s*%b()" }) do
    local _, e = code:find(def)
    if e then
      if code:sub(e + 1):find("[.:]" .. n .. "%s*%(") then return "call" end
      return "duplicate"
    end
  end
  local pos = code:find(pat)
  if not pos then return "comment" end
  if inString(code, pos) then return "string" end
  if kind == "descriptor" then
    if code:find("^%s*local%s+[%w_,%s]*%f[%w_]" .. n .. "%f[^%w_]") then return "bare" end
    if code:find("[{,;]%s*" .. n .. "%s*=[^=]") or code:find("^%s*" .. n .. "%s*=[^=]")
        or code:find("[%w_%]]%." .. n .. "%s*=[^=]") then
      return "call"
    end
    return "bare"
  end
  if code:find("[.:]" .. n .. "%f[^%w_]") then return "call" end
  return "bare"
end

-- ── receivers: which expressions in an addon hold which major ──────────────────────────────
--
-- A member access `X.Name` is credited to a major only when `X` is known to hold that major's
-- library table or one of its instances. Learned per addon from three assignment shapes, iterated
-- to a fixpoint because an alias can be declared in a file that loads before its source:
--   lib       `<lhs> = ... LibStub(... "LibKa0s-<M>-1.0" ...)`
--   instance  `<lhs> = <receiver of M>:New(` (or `.New(`)
--   instance  also `<lhs> = <x> and <receiver of M>:New(`
--   alias     `<lhs> = <receiver>`, `<lhs> = <receiver> or ...`, `<lhs> = <x> and <receiver>`, and
--             each pair of `local a, b = x, y`
-- A `local` lhs is scoped to its file; a dotted lhs (`NS.Perf`) to the whole addon. An access whose
-- receiver resolves to the member's major is a `call`; one whose receiver does not (`self:Stop()`,
-- a parameter, another table's member of the same name) is a `namecall`, which is listed for a
-- reader and never counted as a consumer.

local function learnReceivers(files)
  local global, perFile = {}, {}
  local function resolve(path, expr)
    return (perFile[path] and perFile[path][expr]) or global[expr]
  end
  local function add(path, isLocal, lhs, majors)
    local t
    if isLocal or not lhs:find(".", 1, true) then
      perFile[path] = perFile[path] or {}
      t = perFile[path]
    else
      t = global
    end
    t[lhs] = t[lhs] or {}
    local grew = false
    for m in pairs(majors) do
      if not t[lhs][m] then t[lhs][m] = true; grew = true end
    end
    return grew
  end
  local changed = true
  local rounds = 0
  while changed and rounds < 6 do
    changed, rounds = false, rounds + 1
    for _, f in ipairs(files) do
      if not f.isTest then
        for _, c in ipairs(f.code) do
          local pairsOf = {}
          local isLocal, lhs, rhs = true, c:match("^%s*local%s+([%a_][%w_]*)%s*=%s*(.-)%s*$")
          if not lhs then
            isLocal = false
            lhs, rhs = c:match("^%s*([%a_][%w_%.]*)%s*=%s*(.-)%s*$")
          end
          if lhs then
            pairsOf[1] = { lhs, rhs }
          else
            -- `local a, b, c = x, y, z`, each side a plain list of the same length.
            local l, r = c:match("^%s*local%s+([%a_][%w_]*%s*,[%w_%s,]*)=%s*([%w_%.%s,]+)$")
            if l then
              local ls, rs = {}, {}
              for x in l:gmatch("[%a_][%w_]*") do ls[#ls + 1] = x end
              for x in r:gmatch("[^,]+") do rs[#rs + 1] = (x:gsub("^%s+", ""):gsub("%s+$", "")) end
              if #ls == #rs then
                for i = 1, #ls do pairsOf[#pairsOf + 1] = { ls[i], rs[i] } end
              end
              isLocal = true
            end
          end
          for _, pr in ipairs(pairsOf) do
            local lv, rv = pr[1], pr[2]
            if rv and rv ~= "" then
              local majors
              local M = rv:match('LibStub.-"(LibKa0s%-[%w]+%-1%.0)"')
              if M then
                majors = { [M] = true }
              else
                local recv = rv:match("^([%a_][%w_%.]*)[:.]New%s*%(")
                  or rv:match("^[%a_][%w_%.]*%s+and%s+([%a_][%w_%.]*)[:.]New%s*%(")
                  or rv:match("^([%a_][%w_%.]*)$")
                  or rv:match("^([%a_][%w_%.]*)%s+or%f[^%w_]")
                  or rv:match("^[%a_][%w_%.]*%s+and%s+([%a_][%w_%.]*)$")
                majors = recv and resolve(f.path, recv)
              end
              if majors and add(f.path, isLocal, lv, majors) then changed = true end
            end
          end
        end
      end
    end
  end
  return resolve
end

-- ── descriptor literals ─────────────────────────────────────────────────────────────────────
--
-- A descriptor field counts only where it is passed: a top-level key of the table literal handed
-- to `<receiver of M>:New(` (or `.New(`, or Widgets' `.CopyWindow(`). When the argument is a name
-- rather than a literal (`lib:New(descriptor)`), the table that name is assigned in the same file
-- is read instead, plus any `descriptor.key = ...` assignment to it in that file. A grep for a bare
-- key finds locals; this reads the descriptor.

--- Top-level keys of the table whose `{` is at (li, col) in f.code, as { key, line } records.
local function tableKeys(f, li, col)
  local out, depth, quote = {}, 0, nil
  local expectKey = false
  for i = li, #f.code do
    local c = f.code[i]
    local j = (i == li) and col or 1
    while j <= #c do
      local ch = c:sub(j, j)
      if quote then
        if ch == "\\" then j = j + 1 elseif ch == quote then quote = nil end
      elseif ch == '"' or ch == "'" then
        quote = ch
      elseif ch == "{" or ch == "(" or ch == "[" then
        depth = depth + 1
        if depth == 1 then expectKey = true end
      elseif ch == "}" or ch == ")" or ch == "]" then
        depth = depth - 1
        if depth == 0 then return out end
      elseif ch == "," or ch == ";" then
        if depth == 1 then expectKey = true end
      elseif depth == 1 and expectKey and ch:match("[%a_]") then
        local key = c:match("^([%a_][%w_]*)%s*=[^=]", j) or c:match("^([%a_][%w_]*)%s*=$", j)
        if key then out[#out + 1] = { key, i } end
        expectKey = false
      elseif depth == 1 and not ch:match("%s") then
        expectKey = false
      end
      j = j + 1
    end
    quote = nil
  end
  return out
end

local function descriptorPasses(files, resolve)
  local passes = {}   -- { major, key, path, line }
  for _, f in ipairs(files) do
    if not f.isTest then
      for li, c in ipairs(f.code) do
        for recv, fn, rest in c:gmatch("([%a_][%w_%.]*)[:.](%a+)%s*(%(?%s*[%w_{]*)") do
          if fn == "New" or fn == "CopyWindow" then
            -- CopyWindow is Widgets' alone, and hosts lease it as a bare function
            -- (`NS.CopyWindow = lib.CopyWindow`), so its receiver is not resolved.
            local majors = (fn == "CopyWindow") and { ["LibKa0s-Widgets-1.0"] = true }
              or resolve(f.path, recv)
            if majors then
              local keys = {}
              local brace = rest:find("{", 1, true)
              if brace then
                local s0 = c:find(recv .. (c:find(recv .. ":" .. fn, 1, true) and ":" or ".") .. fn, 1, true)
                local col = s0 and c:find("{", s0, true)
                if col then keys = tableKeys(f, li, col) end
              else
                local name = rest:match("^%(%s*([%a_][%w_]*)")
                if name then
                  local nm = escape(name)
                  for lj, cj in ipairs(f.code) do
                    local col = cj:match("^%s*local%s+" .. nm .. "%s*=%s*()%{")
                      or cj:match("^%s*" .. nm .. "%s*=%s*()%{")
                    if col then
                      for _, k in ipairs(tableKeys(f, lj, col)) do keys[#keys + 1] = k end
                    end
                    local k2 = cj:match("^%s*" .. nm .. "%.([%a_][%w_]*)%s*=[^=]")
                    if k2 then keys[#keys + 1] = { k2, lj } end
                  end
                end
              end
              for M in pairs(majors) do
                if fn == "New" or M == "LibKa0s-Widgets-1.0" then
                  for _, k in ipairs(keys) do
                    passes[#passes + 1] = { M, k[1], f.path, k[2], f.lines[k[2]] }
                  end
                end
              end
            end
          end
        end
      end
    end
  end
  return passes
end

-- ── the scan ────────────────────────────────────────────────────────────────────────────────

local hitsF = assert(io.open(OUT .. "/hits.tsv", "wb"))
hitsF:write("major\tkind\tmember\taddon\tlocation\tclass\tline\n")
local summary = {}
for i = 1, #members do
  summary[i] = { call = 0, namecall = 0, duplicate = 0, stub = 0, other = 0, test = 0,
    hosts = {}, nameHosts = {}, hits = {} }
end

local memberIndex = {}
for i, mem in ipairs(members) do memberIndex[mem.major .. "\0" .. mem.kind .. "\0" .. mem.name] = i end

local function qualified(resolve, path, mem, code)
  local n = escape(mem.name)
  for recv in code:gmatch("([%a_][%w_%.]*)[.:]" .. n .. "%f[^%w_]") do
    local majors = resolve(path, recv)
    if majors and majors[mem.major] then return true end
  end
  return false
end

local nFiles = 0
for _, addon in ipairs(addons()) do
  local repo = GIT .. "/" .. addon
  local files = {}
  for _, path in ipairs(trackedLua(repo)) do
    local lines = readLines(repo .. "/" .. path)
    if lines then
      local code, stub = analyse(lines)
      files[#files + 1] = { path = path, lines = lines, code = code, stub = stub,
        isTest = path:match("^tests/") ~= nil, blob = table.concat(lines, "\n") }
    end
  end
  local resolve = learnReceivers(files)
  for _, pass in ipairs(descriptorPasses(files, resolve)) do
    local mi = memberIndex[pass[1] .. "\0descriptor\0" .. pass[2]]
    if mi then
      local s = summary[mi]
      s.call = s.call + 1
      s.hosts[addon] = true
      s.hits[#s.hits + 1] = { addon, pass[3] .. ":" .. pass[4], "call", "call",
        (pass[5]:gsub("^%s+", ""):gsub("\t", " "):sub(1, 160)) }
    end
  end
  for _, f in ipairs(files) do
    nFiles = nFiles + 1
    for mi, mem in ipairs(members) do
      if mem.kind ~= "descriptor" and f.blob:find("%f[%w_]" .. escape(mem.name) .. "%f[^%w_]") then
        local s = summary[mi]
        for li, line in ipairs(f.lines) do
          local cls = classify(mem.kind, mem.name, f.code[li], f.stub[li], line)
          if cls == "call" and mem.kind ~= "descriptor"
              and not qualified(resolve, f.path, mem, f.code[li]) then
            cls = "namecall"
          end
          if cls then
            if f.isTest then
              s.test = s.test + 1
            elseif s[cls] then
              s[cls] = s[cls] + 1
              if cls == "call" then s.hosts[addon] = true end
              if cls == "namecall" then s.nameHosts[addon] = true end
            else
              s.other = s.other + 1
            end
            local label = (f.isTest and "test:" or "") .. cls
            local list = s.hits
            list[#list + 1] = { addon, f.path .. ":" .. li, label, cls,
              (line:gsub("^%s+", ""):gsub("\t", " "):sub(1, 160)) }
          end
        end
      end
    end
  end
end
-- What hits.tsv keeps. A member with production calls in FEWER THAN THREE addons (the thin and
-- zero-consumer set this census exists for) keeps every hit except string literals, which are
-- dropped everywhere: PrettyChat's GlobalStrings.lua alone carries thousands of English words that
-- collide with member names. A member three or more hosts call cannot have its verdict changed by
-- one hit, so it keeps its production call, duplicate and stub hits only, at most five per addon
-- per class, as evidence; summary.tsv still counts every hit. Descriptor fields never list bare or
-- comment hits (a grep for a bare key finds locals, docs/adoption-prompt.md's own warning).
for mi, mem in ipairs(members) do
  local s = summary[mi]
  local nHosts = 0
  for _ in pairs(s.hosts) do nHosts = nHosts + 1 end
  local perAddon = {}
  for _, h in ipairs(s.hits) do
    local cls, label = h[4], h[3]
    local strong = cls == "call" or cls == "duplicate" or cls == "stub" or cls == "namecall"
    local keep
    if nHosts < 3 then
      keep = strong or (cls ~= "string" and mem.kind ~= "descriptor")
    elseif strong and label == cls then
      local k = h[1] .. "\0" .. cls
      perAddon[k] = (perAddon[k] or 0) + 1
      keep = perAddon[k] <= 5
    end
    if keep then
      hitsF:write(table.concat({ mem.major, mem.kind, mem.name, h[1], h[2], h[3], h[5] }, "\t"), "\n")
    end
  end
end
hitsF:close()

local function keys(t)
  local out = {}
  for k in pairs(t) do out[#out + 1] = k end
  table.sort(out)
  return table.concat(out, ",")
end
local sumF = assert(io.open(OUT .. "/summary.tsv", "wb"))
sumF:write("major\tkind\tmember\tcall\tnamecall\tduplicate\tstub\tother\ttest\tcallHosts\tnamecallHosts\n")
for mi, mem in ipairs(members) do
  local s = summary[mi]
  sumF:write(table.concat({ mem.major, mem.kind, mem.name, s.call, s.namecall, s.duplicate, s.stub,
    s.other, s.test, keys(s.hosts), keys(s.nameHosts) }, "\t"), "\n")
end
sumF:close()
print(("census: %d members across %d majors, %d files searched"):format(#members, #MAJORS, nFiles))
