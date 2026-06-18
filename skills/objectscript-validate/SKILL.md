---
name: objectscript-validate
description: >-
  Reference of hard-won InterSystems ObjectScript / IRIS gotchas: compilation
  traps, interactive-session limitations, and FHIR/interop API quirks. Consult
  this before writing or compiling ObjectScript classes, before running code in
  an interactive `iris session`, or when a compile/runtime error looks
  misleading. A long-lived, append-only knowledge base; future versions may add
  an automated validator (cf. the iris-dtl-validate skill).
---

# ObjectScript gotchas

A running list of ObjectScript / IRIS pitfalls we have actually hit, with the
symptom, the cause, and the fix. **Read the relevant entries before writing or
compiling ObjectScript**, especially when an error message does not obviously
point at its cause.

When you hit a new gotcha, **add an entry here** in the same format. Keep entries
concrete: real symptom text, root cause, minimal fix. Prefer appending over
rewriting so the history stays useful.

## How to use

- Before authoring a `.cls`: skim "Compilation" and "Classes & methods".
- Before running code via `iris session ... <<EOF`: read "Interactive session".
- When a compile error mentions methods you didn't write (e.g. `methodimpl`,
  auto-generated methods), suspect a cascade — check "Compilation" first.

---

## Compilation

### `try`/`catch` requires `return` (not `quit`) to return a value, and `[ ProcedureBlock = 1 ]`
- **Symptom:** misleading cascade of errors on *unrelated* and auto-generated
  methods: `#1043 QUIT argument not allowed`, `#1026 Invalid command : 'catch'`,
  and method headers showing `methodimpl {` in the generated `.int`. The error
  list does not point at the real line.
- **Cause:** inside a `try { }` (or any nested `{ }` such as an `if` block),
  `quit <value>` exits the *block*, not the method, so returning a value there is
  illegal. The compiler's error recovery then mis-parses following methods.
- **Fix:** in any method that uses `try`/`catch`, mark it `[ ProcedureBlock = 1 ]`
  and use `return <value>` to return from the method (use `quit` only bare, to
  leave a loop/block). Example:
  ```objectscript
  Method Foo() As %Status [ ProcedureBlock = 1 ]
  {
      set sc = $$$OK
      try {
          if bad { return ..MakeError(...) }   // return, NOT quit
      }
      catch ex { set sc = ex.AsStatus() }
      return sc
  }
  ```

### A dynamic-object literal `{ }` cannot contain `""`-escaped quotes
- **Symptom:** `#1021: Expected right bracket` on a line building a `{...}`/`[...]`
  literal whose string value itself contains doubled quotes, e.g.
  `do arr.%Push({"div":"<div xmlns=""http://..."">x</div>"})`.
- **Cause:** the `{}`/`[]` dynamic-literal parser is *not* the ObjectScript string
  parser; inside a literal it does not accept `""` as an escaped quote, so the
  embedded quote prematurely closes the value and brace matching breaks.
- **Fix:** build the troublesome string as an ordinary ObjectScript literal
  (where `""` *is* a valid escaped quote) and assign it via `%Set`/property,
  rather than inlining it in the `{}` literal:
  ```objectscript
  set div = "<div xmlns=""http://www.w3.org/1999/xhtml"">x</div>"
  set o = {}  do o.%Set("text", {"status":"generated"})  set o.text.div = div
  ```

### `$$$` macros need their include
- **Symptom:** undefined-macro / syntax errors on `$$$OK`, `$$$ERROR`,
  `$$$ISERR`, `$$$GeneralError`, etc. at compile time.
- **Cause:** the status macros are defined in `%occStatus`.
- **Fix:** put `Include %occStatus` at the top of the `.cls` (before the `Class`
  line). For other macro families, include the matching `.inc`.

### Compiling a class from a mounted source tree
- Single file: `do $system.OBJ.Load("/opt/app/src/iris/cls/Pkg/MyClass.cls","ck")`.
- Whole tree (recurse): `set sc=$system.OBJ.LoadDir("/opt/app/src/iris/cls","ck",.err,1)`.
- `"ck"` = compile + keep source. Check success with `$system.Status.IsError(sc)`
  (see interactive-session note about `$$$` below).
- Deployed HS library classes have their source stripped: you can read method
  signatures/params via `%Dictionary.*` but `Implementation` is empty.

---

## Interactive session (`iris session ... <<EOF`)

### `$$$` macros do not work interactively
- **Symptom:** `<SYNTAX>` error on a line using `$$$ISERR(sc)` / `$$$OK` etc. run
  through `iris session`.
- **Cause:** `$$$` macros are a *compile-time* preprocessor feature; the
  interactive shell / XECUTE has no compile context.
- **Fix:** use the runtime API instead — `$system.Status.IsError(sc)`,
  `$system.Status.GetErrorText(sc)`, `$system.Status.OK()`. Reserve `$$$` macros
  for code inside `.cls`/`.mac` routines.

### No multi-line brace blocks
- **Symptom:** `<SYNTAX>` when an `if { }` / `for { }` / `while { }` / `try { }`
  body spans multiple physical lines in a heredoc.
- **Cause:** the interactive parser handles one line at a time.
- **Fix:** keep each brace block body on a single line, e.g.
  `if x { do a  do b  write c,! }`. Use multiple spaces to separate commands.

### Escape `$` in unquoted heredocs
- **Symptom:** shell expands `$data`, `$job`, `$system`, `$lb`, etc. to empty
  before IRIS sees them.
- **Cause:** an unquoted heredoc (`<<EOF`) is subject to shell expansion.
- **Fix:** escape ObjectScript `$` as `\$` (e.g. `\$system.OBJ.Load(...)`,
  `\$data(^x)`), or use a quoted heredoc (`<<'EOF'`) when no shell interpolation
  is needed in the body.

---

## Classes & methods

### Reading shape of deployed/locked classes
- Methods/signatures: query `%Dictionary.MethodDefinition` /
  `%Dictionary.CompiledMethod` (cols `Name`, `FormalSpec`, `ReturnType`,
  `ClassMethod`). Properties: `%Dictionary.PropertyDefinition` /
  `%Dictionary.CompiledProperty`. Superclass: `%Dictionary.ClassDefinition.Super`.
- The single override point on `HS.FHIRServer.Interop.Service` is
  `OnProcessInput(pRequest As HS.FHIRServer.Interop.Request, Output pResponse As HS.FHIRServer.Interop.Response) As %Status`.

---

## Productions (interop runtime)

### A recompiled host keeps running the *previous* code until the production restarts
- **Symptom:** after fixing and recompiling a business host (`.cls`) and re-running
  the installer (`UpdateProduction`), a queued message still fails with the old
  error; the event log shows `Host Class X has been recompiled; continuing to run
  using code from previous version`, sometimes a `<SYNTAX>` at a line that no
  longer exists.
- **Cause:** `Ens.Director.UpdateProduction(timeout)` reloads config but does not
  necessarily recycle a busy/pooled host job; the running job keeps its already-
  loaded routine until it idles or the production is bounced.
- **Fix:** for code (not just config) changes, restart the production:
  `do ##class(Ens.Director).StopProduction(30,1)` then
  `do ##class(Ens.Director).StartProduction(name)`. Re-run the flow after the
  bounce so the message executes against the new code.

## FHIR / interoperability (IRIS for Health)

### In-namespace resource create/read (no HTTP)
- `set svc = ##class(HS.FHIRServer.Service).EnsureInstance(endpointPath)` then
  `do svc.DispatchRequest(apiReq, .apiResp)` with an
  `HS.FHIRServer.API.Data.Request` (`RequestMethod`, `RequestPath`, `BaseURL`,
  `Json`).
- **`EnsureInstance` wants the endpoint *path* (`/fhir/R4`), not a full URL.**
  `pRequest.Request.BaseURL` is fully-qualified
  (`http://host:52773/fhir/R4`) — strip scheme/host first, or you get
  `Object open failed because 'ServiceIdIdx' key value of '<url>' was not found`.
- On create, `apiResp.Status="201"`, new id in `apiResp.Id`, path in
  `apiResp.Location`; `apiResp.Json` is **empty** on create (no `Prefer:
  return=representation`).

### Reading the request payload in a production
- The interop request payload is **not** reliably in the persisted QuickStream
  after the fact (observed `Size=0`); `Request.Json` is transient.
- At runtime inside `OnProcessInput`, read `pRequest.QuickStreamId`
  (`##class(HS.SDA3.QuickStream).%OpenId(id)`, `Rewind()`, `%FromJSON()`) first,
  and fall back to `pRequest.Request.Json`.

### Building an interop response
- Construct `HS.FHIRServer.Interop.Response`; set `.Response` (an
  `HS.FHIRServer.API.Data.Response` with `.Json` + `.Status`); **set
  `.ContentType`** ("application/fhir+json") explicitly; and write the body JSON
  to a new `HS.SDA3.QuickStream` whose id goes on `.QuickStreamId` — the REST
  renderer reads the body from the QuickStream, not from `.Response.Json`.

### Unregistered `$`-operations reach the production
- A custom `$`-operation that is not registered with an `OperationHandler` is
  **not** rejected at the REST layer. It arrives at the interop service as a
  normal request with `RequestPath = "$ambient-intake"` (literal `$`, no leading
  slash). The `OperationNotSupported` 400 is generated *downstream* in
  `HS.FHIRServer.Interop.Operation`. This is what lets you intercept and handle
  the operation by branching on `Request.RequestPath` in a service subclass,
  with no `OperationHandler` subclass.

### FHIR R4 status vs docStatus on `DocumentReference`
- `DocumentReference.status` (required) is the *reference* status:
  `current | superseded | entered-in-error` — there is **no `preliminary`**.
- The document draft→final lifecycle lives on the optional `DocumentReference.docStatus`:
  `preliminary | final | amended | entered-in-error`.
- `Composition.status` *does* use `preliminary | final | amended | entered-in-error`.
- A `Composition.date` must be a FHIR `dateTime` (ISO 8601, e.g.
  `2026-06-05T09:03:21Z`); the ODBC space-separated form
  (`$zdatetime(...,3)` → `2026-06-05 09:03:21`) fails validation. Fix:
  `$translate($zdatetime($ztimestamp,3,1,0)," ","T")_"Z"`.

## Productions — retry, timeouts, message re-delivery

### Business Operation retry is opt-in; returning an error fails fast by default
- **Symptom/assumption to avoid:** expecting a Business Operation to auto-retry a
  transient external-call failure just because its mapped method returned an error
  `%Status`. It does **not**.
- **Cause:** per "Defining Business Operations", retry only happens if the host
  sets `..Retry = 1` (then it waits `..RetryInterval` and retries until
  `..FailureTimeout` elapses). With `..Retry` left at its default, a returned error
  propagates immediately — the message fails fast.
- **Consequence (useful):** if you implement your own classified retry/backoff
  inside a helper (e.g. around the HTTP call), the interop layer will **not**
  double-retry; a `%Status` you return to the BP is genuinely terminal, so a
  `FailJob`-style handler runs exactly once. Don't also set `..Retry=1` unless you
  want both layers retrying.

### `%Net.HttpRequest.Post` blocks up to `..Timeout` on a connect failure
- **Symptom:** a BO that calls a bad/unreachable host appears hung; the job sits
  in-progress for a long time before any retry/backoff logging appears.
- **Cause:** an unresolvable host or refused connection does **not** fail
  instantly — `Post()` waits up to `..Timeout` seconds before returning
  `ERROR #6059: Unable to open TCP/IP socket to server <host>:<port>`. A generous
  `..Timeout` (e.g. 300s for large uploads) therefore makes *transient-failure
  detection* correspondingly slow, multiplied by each retry attempt.
- **Fix/implication:** make the timeout configurable and keep it modest, or use a
  separate shorter connect timeout, so transient failures are detected quickly.
  When forcing a transient failure in a test, set a small `..Timeout` (e.g. 3s) and
  point at an unresolvable host (`something.invalid`) — DNS failure returns #6059
  in ~`..Timeout` seconds; `127.0.0.1:443` with nothing listening unexpectedly
  *blocked* (not refused) in this build, so prefer the `.invalid` host.

### Stopping/restarting a production re-delivers in-flight messages
- **Symptom:** after `StopProduction` + `StartProduction` to clear a stuck job, the
  same message runs again on restart (you see a second pipeline run for the old
  correlation id).
- **Cause:** a message that was in-progress when the production stopped is
  re-delivered when it restarts (at-least-once). Expect duplicate runs of an
  injected failure when you bounce to unstick it; identify runs by correlation id.

### `Ens.Util.Log.LogWarning/LogInfo/LogError` work from a plain helper class
- A non-host helper (`Extends %RegisteredObject`) called *within* a running host
  job can write to the Event Log via
  `##class(Ens.Util.Log).LogWarning(pSourceClass, pSourceMethod, pText)` (and
  `LogInfo`/`LogError`). This is the way to log from a shared helper that has no
  `$$$LOGINFO` macro context (those macros need an Ens/Ensemble include and a host
  context). Wrap the call in a `try/catch` so a logging hiccup never disturbs the
  real work.

### `Composition.identifier` is 0..1 (a single Identifier), not an array
- **Symptom:** creating a `Composition` fails with HTTP 400
  `<HSFHIRErr>UnexpectedArray ... Property 'identifier' of Type 'Composition'
  cannot be an Array` (`expression: ["Composition.identifier"]`).
- **Cause:** unlike most resources where `identifier` is `0..*`,
  `Composition.identifier` is `0..1` — a single `Identifier`, not a list. The same
  applies to a few other resources (e.g. `Encounter.identifier` is `0..*`, but
  check each type). `DocumentReference.identifier` *is* `0..*` (an array).
- **Fix:** set `Composition.identifier` to a single object
  (`{"system":...,"value":...}`), not a one-element array. When writing a generic
  "stamp identifier" helper, parameterise the array-vs-single shape per resource type.

### IRIS FHIR server supports PUT update-as-create (client-assigned id)
- A `PUT /Type/<id>` to a logical id that does not yet exist **creates** the
  resource with that id (update-as-create), rather than 400/405. This is the clean,
  idempotent way to load conformance resources (`StructureDefinition`, `ValueSet`,
  `CodeSystem`) under stable, known ids so code can read them back by id later —
  re-running the load just overwrites in place (and bumps the version).

### `HSFHIR_X0001_R.Rsrc.ResourceId` is stored upper-cased
- **Symptom:** a script enumerates resource ids from the repository table
  (`SELECT DISTINCT ResourceId FROM HSFHIR_X0001_R.Rsrc WHERE ResourceType=...`)
  and then `DELETE`s / reads each via the FHIR API, but resources with
  *client-assigned string ids* (e.g. `StructureDefinition/DemoConsultNote`,
  `CodeSystem/ikem-ambient-activity`) are never affected — the DELETE returns a
  cheerful 204 yet the resource survives.
- **Cause:** `Rsrc.ResourceId` is normalised to **upper case** in the table, so
  the enumerated id (`DEMOCONSULTNOTE`, `IKEM-AMBIENT-ACTIVITY`) does not match the
  resource's real logical id. A FHIR DELETE on the wrong-case path hits a
  non-existent resource and no-ops (DELETE is idempotent → 204/200). Numeric
  server-assigned ids (`Binary/79`, `Composition/81`) are case-neutral, so they
  appear to work — masking the bug until a string-id resource is involved.
- **Fix:** for client-assigned (string) ids, enumerate via a FHIR **search**
  (`GET /Type?_elements=id`), whose `entry[].resource.id` is the true-case logical
  id; use the table only for numeric server-assigned ids (handy when you want ids
  without loading large bodies, e.g. audio `Binary`s).

### FHIR search with `_elements=id` on `Binary` returns HTTP 500
- **Symptom:** `GET /Binary?_elements=id` (in-namespace dispatch or REST) returns
  an `OperationOutcome` with status 500; the same query works for `Composition`,
  `DocumentReference`, `StructureDefinition`, etc.
- **Cause:** `Binary` is special (raw data, no normal element model); the
  `_elements` projection is not supported for it on this build.
- **Fix:** don't use `_elements` for `Binary`. To list Binary ids cheaply without
  pulling the (large) bodies, read them from `HSFHIR_X0001_R.Rsrc`
  (`WHERE ResourceType='Binary'`) — Binary ids are numeric, so the upper-casing
  caveat above does not bite.

## Classes & methods (continued)

### Abstract provider classes: `[ Abstract ]` body, and `%IsA` is an instance method
- An abstract base with `Class X Extends %RegisteredObject [ Abstract ]` and a
  method declared `Method M(...) As %String [ Abstract ] { }` (empty body)
  compiles fine and forces subclasses to implement `M`. Useful for a provider
  seam (one abstract capability, config-selected concrete subclasses).
- To verify a *configured class name* is the expected kind before using it,
  `%IsA` is an **instance** method, not a class method: instantiate first
  (`set obj = $classmethod(className,"%New")`) then check
  `if 'obj.%IsA("Pkg.BaseClass") { ... }`. There is no
  `$classmethod(className,"%IsA",super)` class-level form.
