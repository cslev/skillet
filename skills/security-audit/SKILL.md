---
name: security-audit
description: >
  Run a structured security audit of a web application or API. Fourteen concrete
  vulnerability patterns, each with a detection command, a reproduction step, the false
  alarms that look identical, and what a regression test must assert. Triggers on
  /security-audit, "security audit", "security review", "audit this codebase", "pen-test",
  "harden this app", or a specific class such as authentication bypass, replay attacks,
  CSRF, secrets in logs, race conditions, timing attacks, or denial of service. Use this
  INSTEAD of an open-ended "find vulnerabilities" pass — it runs defined phases, proves
  each finding with a reproduction, and verifies the tests that protect it. Do NOT use for
  writing security documentation or policies; that is ordinary writing.
argument-hint: "What should I audit — a path, a repo, or a specific class (e.g. 'csrf')?"
---

# Web Application Security Audit

An open-ended instruction to "find vulnerabilities" produces plausible findings, most of
them wrong and none demonstrated. Work these phases in order instead. Each check is narrow
enough to run without judgement and specific enough that a negative result means something.

Examples are Python/FastAPI because that is where these were catalogued; every pattern has a
direct equivalent in Express, Flask, Rails and Django. Items marked **Observed** are real
mistakes found in production code, including several made by the auditor while auditing.

Add these exclusions to every command, or results are unreadable:

```
--exclude-dir=node_modules --exclude-dir=.venv --exclude-dir=__pycache__
--exclude-dir=dist --exclude-dir=build --exclude-dir=.git
```

---

## Phase 0 — Map the surface before looking for bugs

Do not start grepping for bugs. Roughly half the findings fall out of the map.

```bash
grep -rnE '@(app|router)\.(get|post|put|patch|delete)\(' --include='*.py' .   # routes
grep -rnE "getenv|environ\[|process\.env" --include='*.py' --include='*.js' . # config
grep -rn "async def" --include='*.py' .                                       # async handlers
```

Answer five questions **in writing**:

| Question | What it exposes |
|---|---|
| What authenticates a request, and can the client influence it? | Header-spoofing auth bypass (1.1) |
| Does any credential travel in a request **body** rather than a header? | Replay, transport and logging exposure (1.4) |
| What is *ambient* authority — cookies, source IP, network position? | CSRF where `SameSite` does not apply (1.11) |
| Which endpoints change state or move money? | Serialisation (1.6) and CSRF (1.11) |
| What is written to logs, and who can influence its contents? | 1.2, 1.10, 1.13 |

For each route, record **whether the auth guard runs before any data lookup**. A guard after
the lookup is an enumeration oracle: `404` versus `401` reveals which identifiers exist.

---

## Phase 1 — The pattern checks

### 1.1 Client-supplied headers trusted for identity

```bash
grep -rnE "X-Forwarded-For|X-Real-IP|X-Forwarded-Proto|HTTP_X_FORWARDED" --include='*.py' .
```

For each hit: **is the direct peer verified as a known proxy first?** If not, attacker-
controlled input is being used as identity.

**Proof.** `curl -H 'X-Forwarded-For: <an allowlisted ip>' http://host/`

**False alarm.** Used only for display or logging. Worth fixing (log forgery), not a bypass.

**Fix.** Honour forwarded headers only from a configured trusted-proxy list, and take the
**rightmost** hop that is not itself a trusted proxy — proxies *append*, so the leftmost
value is the one the client chose.

**Check the framework layer too.** Many servers rewrite the client address from
`X-Forwarded-For` before your code runs (Uvicorn's `ProxyHeadersMiddleware` does this by
default for loopback peers). An application check is meaningless if the framework already
overwrote the value it inspects.

### 1.2 Secrets reaching logs

```bash
# Direct: a secret-named variable at a log call site
grep -rnE "(password|secret|token|api_key|passphrase|private_key)" --include='*.py' . \
  | grep -iE "logger\.|logging\.|print\(|console\."

# Indirect — THE ONE THAT GETS MISSED: a whole structure dumped
grep -rnE "(logger|logging|console)\.[a-z]+\(.*(json\.dumps|JSON\.stringify|repr|vars|__dict__|payload|body|config)" \
  --include='*.py' --include='*.js' .
```

> **Observed.** The first grep returned clean while `logger.info(f"payload: {json.dumps(data)}")`
> was writing an API key to disk — the secret was *inside a dict*, not named at the call
> site. Always run the second grep.

**Proof.** Capture log output during a request; assert the literal secret is absent. **Set
the capture level to DEBUG first** — at the default `WARNING` nothing is captured and the
absence assertion passes for the wrong reason.

**Check the notification path.** If ERROR-level logs are forwarded to chat/email/push, every
leaked secret is also transmitted off-host.

### 1.3 Secrets partially rendered in a UI

```bash
grep -rnE "\[:[0-9]+\].*\[-[0-9]+:\]|substring\([0-9]|slice\([0-9]" templates/ src/ views/
```

**Proof.** Render the page, then compute the longest substring of the real secret appearing
anywhere in the output. More than ~4 characters is too much.

**Subtlety.** Use a fixed-width mask: `abc...xyz` leaks the length, `••••••••1234` does not.

### 1.4 A bearer credential inside the request body

Common for webhooks. Implies **three** findings — check all:

| Consequence | Check | Fix |
|---|---|---|
| Replayable forever | Is the request required to be recent *and* unique? | Freshness window + idempotency key |
| Credential crosses the wire in cleartext | Is TLS enforced on that endpoint? | Refuse non-TLS delivery |
| Credential lands in logs | See 1.2 | Redact |

**Proof of replay.** Capture one valid request; send the exact bytes again.

**Sizing trap.** An idempotency entry must outlive the freshness of what it protects. If the
window accepts timestamps ±W, a request dated `+W` in the future is accepted now and stays
fresh until `W` past its own timestamp — up to **2W** after acceptance. A TTL of `W` leaves
it replayable in the gap. Size the cache at `2W`.

**Signing is stronger but often unavailable.** If the source is a third-party service sending
static bodies, HMAC is impossible — and adds little anyway, since that service would hold
the signing secret exactly as it holds the bearer key.

### 1.5 Timestamp handling that mixes naive and aware datetimes

```bash
# Precise: calls producing a NAIVE value. Two steps beat a fragile lookahead.
grep -rn "fromtimestamp(" --include='*.py' . | grep -v "tz="

# Broad: needs reading, not counting — most hits are harmless display formatting
grep -rn "datetime.now()\|utcnow()" --include='*.py' .
```

`fromtimestamp(x)` without `tz=` returns **naive local** time; `fromisoformat("...Z")`
returns **aware UTC**. Code using both produces values that cannot be subtracted
(`TypeError`) or that differ by the host's UTC offset. Only those feeding a comparison
matter.

**Proof.** Parse one instant in every accepted representation and assert equality. Then run
the suite under several `TZ` values (`UTC`, `Asia/Singapore`, `America/New_York`,
`Pacific/Kiritimati`) and assert identical verdicts.

**Second-order bug.** Even with correct arithmetic, a value keeping the *sender's* offset is
formatted wrongly if the code labels it UTC — `18:31:44+08:00` printed as `"18:31:44 UTC"`.
Normalise on parse.

### 1.6 Read-then-act on shared state without serialisation

```bash
grep -rn "asyncio.Lock\|Semaphore\|threading.Lock\|Mutex" --include='*.py' .   # often zero
```

Then read handlers for `await get_X()` … `await act_on(X)` with nothing between.

**Proof.** Fire concurrent requests at a fake backend recording call overlap. Assert the
**outcome**, not the call count: two "spend 50%" requests against 1000 must spend 750, not
1000. Track `max_concurrent_calls` in the fake; it must never exceed 1.

**Fix.** Lock keyed by the resource, not globally, so unrelated resources stay parallel.
Hold it across the whole read-then-act sequence, bound the wait, fail with `503`, and ensure
error paths release it.

### 1.7 Blocking I/O reachable from an async handler

A synchronous network or disk call inside a coroutine freezes the **entire** event loop —
every request, health check and background task — for its duration.

**Detection must be transitive.** The naive version misses the common case:

```bash
# WRONG — only finds blocking calls in files that themselves define async handlers
grep -rln "async def" --include='*.py' . | xargs grep -nE "requests\.(get|post)|time\.sleep"

# RIGHT — find blocking calls ANYWHERE, then trace whether async code can reach them
grep -rnE "requests\.(get|post|put)|urllib\.request|time\.sleep\(|subprocess\.run|\.execute\(" \
  --include='*.py' . 
# then, for each file containing one:
grep -rn "import <that_module>\|from <that_module>" --include='*.py' .
```

> **Observed.** The wrong grep returned two harmless hits in the request handler and **missed
> the real bug entirely**: a synchronous `requests.post` sat in a logging helper containing
> no `async def` at all, reached from every async handler through an ordinary `logger.error()`
> call. One unauthenticated request froze the whole application for 1.5 seconds. Utility
> modules — logging, metrics, notifications, feature flags — are the highest-risk place for
> this precisely because nothing in them looks asynchronous.

**Proof, and how to get it wrong.** Run a heartbeat coroutine appending a timestamp every
50 ms, trigger the call, measure the largest gap.

> **Observed, twice:**
> 1. Timing a request *after* an `await` that was itself blocked — the stall finishes before
>    the clock starts and the measurement reads zero.
> 2. Clearing the tick list immediately before the call — with no "before" tick the gap is
>    invisible. **Seed the list with a timestamp taken before the call.**
>
> Both reported "no bug" for a bug that was present.

**Fix.** Move it to a worker thread with a **bounded** queue; drop on overflow rather than
blocking, or backpressure reintroduces the stall. Flush on shutdown, or a daemon thread
discards the tail.

### 1.8 Session cookie flags

```bash
grep -rn "SessionMiddleware\|set_cookie\|session_cookie\|cookie-session" --include='*.py' --include='*.js' .
```

Check `secure`, `httponly`, `samesite`, and the **actual** `max_age` — read the framework's
default rather than assuming absence. Reporting "no max_age" when the framework defaults to
14 days is a wrong description of a real finding.

**Proof.** Log in and read the raw `Set-Cookie` header. Do not infer from source.

**Deployment trap.** Setting `Secure` on an app that cannot serve TLS makes login
*impossible* — the browser silently discards the cookie and the user sees an unexplained
redirect loop. Detect that case server-side and return an explicit error.

### 1.9 Non-constant-time secret comparison

```bash
grep -rnE "(api_key|token|secret|password|signature|hmac)\s*[!=]=" --include='*.py' .
```

**Fix.** A constant-time comparison, on **bytes**.

> **Observed.** A codebase already used `secrets.compare_digest` on its login form — with
> `str` arguments, which raise `TypeError` on non-ASCII input. Any password containing an
> accent made login impossible (correct password → unhandled 500), and any client could
> trigger a 500 on the unauthenticated login endpoint with a non-ASCII username. **Auditing
> a correct-looking control found a worse bug than the one sought.** Check how a control is
> *called*, not just that it is present.

### 1.10 The logging path as an attack surface

Logging is invoked from every code path, including every unauthenticated one, which makes it
the highest-leverage place in the codebase for an attacker. Audit it as a surface in its own
right, asking what **one log line actually costs**:

| What a log call does | Attack it enables |
|---|---|
| Synchronous push to a notification service | **Event-loop freeze per request** (1.7) — a full denial of service from one unauthenticated request |
| Disk write with no size cap | Disk exhaustion |
| Disk write with size-capped rotation | **History eviction** — see below |
| Writes attacker-supplied text | Log injection; they choose what fills the file |
| Sends a notification per event | **Alert fatigue** — real alerts buried and stop being read |

```bash
grep -rn "FileHandler\|RotatingFileHandler\|TimedRotating\|winston\|pino" --include='*.py' --include='*.js' .
# and check what the logger does BESIDES writing to a file:
grep -rnE "def (debug|info|warning|error|critical)" --include='*.py' . -A5 | grep -iE "requests|post|notify|webhook|smtp|slack"
```

**Eviction is the counter-intuitive one.** Adding rotation to fix unbounded growth creates a
*new* vulnerability: rotation caps size by **discarding old entries**, so anyone who can
trigger log writes can now flush your history — including the record of their own activity.
Quantify it: `retained_bytes / (bytes_per_request × requests_per_second)`. At 144 bytes and
100 req/s, a 63 MB retention is gone in 73 minutes. **The real fix is upstream — stop
writing a line per hostile request (1.13) — not merely capping the file.**

**Multi-writer trap.** If several loggers write one file they must share **one handler
object**. Independent rotating handlers each track size separately and rename the file out
from under each other, losing writes. Test with three loggers writing interleaved across
several rollovers and assert every writer's last line survives.

### 1.11 CSRF where authority is ambient and not a cookie

`SameSite=lax` protects cookie-authenticated POSTs. It does **nothing** for authority the
browser attaches by other means — source IP, network position, mTLS — because there is no
cookie for it to govern. Any page loaded in a browser at a trusted address can fire the
request.

**Proof.** Send a POST carrying an `Origin:` header from another site; see if it succeeds.

**Fix.** Require a custom header on state-changing requests. This is **not** security by
obscurity and the header name may be public: a cross-origin page cannot set *any* custom
header without a CORS preflight, and an app answering no preflight makes the browser refuse
to send the real request. The rule enforced is "only same-origin JavaScript can set custom
headers"; knowing the name does not confer same-origin status.

**Guard the guard.** Assert in a test that no `Access-Control-Allow-Origin` is returned. A
permissive CORS middleware added later for an unrelated integration disables the entire
protection with nothing in the CSRF code changing.

**State the limits.** Does not stop a non-browser attacker already inside the trusted
network, and does not survive XSS.

### 1.12 Insecure or predictable defaults

Audit the shipped `*.example` / `*.sample` config, not only the code:

- A default credential (`admin` / `changeme`)?
- An identifier or path meant to be random, shipped as a constant?
- **Placeholder secrets** (`your_api_key_here`) — published in the repository, so not secret
  at all. A live config still containing one is **critical**, not a nag. Detect at runtime.
- Any security control disabled by default?

**Design guidance.** A control with an "off" switch gets switched off by the first person who
hits a rejection. Prefer a *tunable* to a *disable*: a window that can be widened but not
removed, a floor rather than a zero.

### 1.13 Unbounded work triggered by unauthenticated requests

For every pre-authentication path, ask what an attacker gets per request — then multiply by
the rate they can achieve. Costs and consequences are tabulated in 1.10.

**Check what is logged *before* authentication.** A "request received" line carrying
attacker-supplied fields hands them a pen for your log file and doubles the volume of any
flood.

**Fix, in priority order:**

1. **Coalesce.** Report the first occurrence of each distinct problem immediately, count
   repeats, emit one periodic summary. Preserves every genuine signal and kills the flood.
2. **Throttle** per source address.
3. Move pre-auth logging to after authentication.

> **Throttling design trap.** A limiter an attacker can aim at the *victim* is worse than no
> limiter. Count per **source**, never per target account — otherwise flooding account X
> becomes a way to lock out account X. Clear the counter on success, exempt loopback and
> configured trusted addresses, keep windows short and self-healing. State the residual
> trade-off plainly: a blocked source's *valid* requests also wait out the window, and
> checking the credential first to avoid that would remove the protection entirely.

### 1.14 Resource exhaustion without an attacker

Not every denial of service is hostile. Check the limits a *legitimate* heavy user hits:

- Queue or lock timeouts — if requests serialise on a shared resource, does
  `(concurrent requests) × (time per request)` exceed the timeout at realistic load?
- Unbounded in-memory collections keyed by user-supplied values.
- Retry loops with no ceiling.

**Proof.** Compute the crossover point and state it in the configuration file, so the
operator knows when to raise the limit instead of discovering it as dropped requests.

---

## Phase 2 — Prove every finding before reporting it

A finding without a reproduction is a guess.

1. Write the smallest script demonstrating the bug against the **real** code path — the
   actual app object, real routes, real middleware. Several patterns appear only through the
   full stack.
2. Run it. If it does not reproduce, discard the finding.
3. Keep the script; it becomes the regression test.

**Treat a surprising negative as suspiciously as a surprising positive.** Two probes in one
audit reported "no bug" for a bug that was present (1.7).

---

## Phase 3 — Fix with the operator's failure mode in mind

Every behaviour-changing fix needs the *legitimate user's* failure path designed, not only
the attacker's:

- **What breaks for a correct user?** Enumerate before shipping. Auth hardening that
  silently stops a working integration is worse than the vulnerability.
- **Does the error name the cause?** When one change has three possible misconfigurations,
  the log must say which. "Rejected: not HTTPS" is useless; "arrived from 1.2.3.4, which is
  not in the trusted-proxy list" is actionable.
- **Is failure loud or silent?** Silent rejection of valid traffic is the worst outcome of a
  security fix.
- **Would a stale cached client hit this?** After a JS change, a browser holding the old
  bundle produces exactly the "attack" signature. Say so in the message.

---

## Phase 4 — Mutation-test the regression tests

**A passing test proves nothing.** Revert the fix and confirm the test fails.

```python
source = path.read_text()
try:
    path.write_text(source.replace(FIXED, ORIGINAL, 1))
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", target], ...)
finally:
    path.write_text(source)          # restore by CONTENT, never `git checkout`
assert result.returncode != 0, "the test does not catch the regression"
```

Three failure modes this catches, all **observed**:

**A vacuous assertion.** A test asserted `guard.ttl == window * 2`, but the fixture
*constructed* the guard with `window * 2` — it checked the fixture's arithmetic, not the
application's, and reverting the fix did not fail it. **Rule: a fixture must never recompute
a value the test asserts. Read it from the application.**

**A vacuous absence check.** `assert secret not in captured_logs` passes trivially when
nothing was captured. **Rule: assert the capture is non-empty before asserting absence.**

**An ineffective mutation.** Defensive code often has two layers — a fast path and a locked
re-check. Removing one leaves the other, behaviour is unchanged, and you wrongly conclude the
test is weak. **Rule: before trusting a "MISSED", prove the mutation changed behaviour.**

> **Restore by content, not `git checkout`.** A mutation script using `git checkout --`
> silently reverts *uncommitted* work in the same file. This destroyed a real fix mid-audit.

---

## Phase 5 — Audit what the fixes themselves introduced

Every fix creates new considerations:

| Fix | Introduced |
|---|---|
| Log rotation | An attacker can now *evict* history (1.10) |
| `Secure` cookie | Login impossible over HTTP, appearing as a redirect loop (1.8) |
| Trusted-proxy gate | Proxied deployments break until configured |
| Freshness window | Now depends on host clock accuracy — needs NTP guidance |
| Background notification queue | Items lost at shutdown without a flush |
| Per-resource lock | A queue that can time out, i.e. a dropped request (1.14) |
| Throttle | A blocked source's valid requests are also refused |

Also audit the **test suite** for state leaks after introducing module-level singletons: a
shared limiter or cache accumulates across tests and changes results by run order. Run under
several shuffle seeds to catch it.

---

## Deliverable checklist

An audit is finished when, for each finding:

- [ ] A reproduction against the real code path, with measured impact
- [ ] A fix whose operator-facing failure mode is designed and documented
- [ ] A regression test that **provably fails** when the fix is reverted
- [ ] Second-order effects of the fix examined (Phase 5)
- [ ] Breaking changes listed explicitly for the release notes
- [ ] Residual risk stated honestly, including what the fix does *not* cover
