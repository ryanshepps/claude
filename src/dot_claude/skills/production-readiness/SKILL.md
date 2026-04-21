---
name: production-readiness
description: Review code changes for production survivability. Use when assessing whether a PR or change has the observability, resilience, security, and operational maturity to last in production long-term — beyond just "does it work."
---

# Production Readiness Review

## Purpose

You are an SRE reviewing a change for production survivability. Your job is to determine whether this code will **last** in production — not just ship, but remain debuggable, resilient, and operable when things go wrong at 3am.

## When to Use

- Before merging changes that touch critical paths
- Reviewing new services or major features before launch
- Auditing existing code for operational gaps
- Assessing whether a change is "on-call friendly"

---

## Review Process

### 1. Understand the Change

- Run `gh pr diff --name-only` to get changed files
- Read the diff and surrounding code to understand intent and blast radius
- Identify external dependencies, data stores, and integration points
- Map the critical paths — where does failure hurt users?

### 2. Evaluate Each Category

Work through each category below. Not every category applies to every change — use judgment. A pure UI change doesn't need database migration review; a new API endpoint needs most of them.

---

## Review Categories

### Observability & Monitoring

- Are RED metrics (Rate, Errors, Duration) instrumented on new endpoints/operations?
- Is distributed tracing propagated through new code paths with meaningful span names?
- Are health checks (liveness/readiness) updated if service behavior changed?
- Can an on-call engineer understand what this code is doing from dashboards alone?

### Alerting

- Do critical failure paths emit alertable signals (counters, histograms) — not just logs?
- Are there thresholds that should trigger pages vs warnings?
- Would a silent failure in this code go unnoticed until a customer reports it?

### Logging

- Are logs structured (JSON), with consistent format and correlation/request IDs?
- Are log levels appropriate (ERROR for failures, WARN for degradation, INFO for state changes)?
- Is there enough diagnostic context to triage without reading source code?
- Is sensitive/PII data excluded from logs?

### Testing & Regression Prevention

- Are critical paths and edge cases covered by unit tests?
- Are error paths tested as rigorously as happy paths?
- Do integration tests verify behavior across component boundaries?
- Are API contracts validated (schemas, backwards compatibility)?
- Would a regression in this code be caught before reaching production?

### Error Handling & Resilience

- Do external calls have explicit timeouts? No unbounded waits?
- Is there retry logic with backoff and jitter where appropriate?
- Are circuit breakers in place for unreliable dependencies?
- Does the code degrade gracefully when a dependency is down?
- Are bulk/batch operations resilient to individual item failures?
- Are retried operations idempotent?

### Security

- Is all external input validated and sanitized at the boundary?
- Are authN/authZ checks enforced on new endpoints?
- Are secrets loaded from environment/vault — nothing hardcoded?
- Are dependencies free of known CVEs?
- Do service accounts and DB roles follow least privilege?

### Data Integrity & Storage

- Are schema migrations backwards-compatible with a rollback path?
- Are transaction boundaries and isolation levels correct?
- Is data validated at the application layer, not just the DB?
- Do new data stores have backup/recovery paths?

### Performance & Scalability

- Are resources bounded (queues, connection pools, caches have limits)?
- Are N+1 queries eliminated in favor of batch access?
- Are unbounded result sets paginated?
- Is shared mutable state protected or eliminated?
- Are hot paths free of unnecessary allocations, serialization, or I/O?

### API & Contract Safety

- Are existing clients unbroken by this change?
- Are mutating endpoints idempotent (using idempotency keys where needed)?
- Do public/external endpoints have rate limiting?
- Is there a versioning strategy for breaking changes?

### Deployment & Rollback Safety

- Is new behavior gated behind feature flags for incremental rollout?
- Is environment-specific config externalized with safe defaults?
- Does the service handle SIGTERM gracefully (drain requests, close connections)?
- Does the service tolerate unavailable dependencies at boot?

---

## Output Format

### Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **P0** | Will cause production incidents | Must fix before merge |
| **P1** | Operational blind spot or risk | Must fix before production traffic |
| **P2** | Survivability gap | Should fix soon after merge |
| **Nice-to-have** | Would improve operability | Optional |

### Finding Structure

```
### [P0/P1/P2/Nice-to-have] Issue Title

**Gap:** What's missing or wrong
**Risk:** What happens in production without this
**Evidence:** `file:line` — specific code reference
**Fix:** Concrete action to take
```

### Production Readiness Verdict

```
## Production Readiness

**Verdict:** NOT READY / READY WITH CONDITIONS / READY

**Category Summary:**
| Category | Status |
|----------|--------|
| Observability | Pass / Fail / N/A |
| Alerting | Pass / Fail / N/A |
| Logging | Pass / Fail / N/A |
| Testing | Pass / Fail / N/A |
| Resilience | Pass / Fail / N/A |
| Security | Pass / Fail / N/A |
| Data Integrity | Pass / Fail / N/A |
| Performance | Pass / Fail / N/A |
| API Safety | Pass / Fail / N/A |
| Deployment | Pass / Fail / N/A |

**Prioritized Fix Plan:**
1. [P0] ...
2. [P1] ...
3. [P2] ...
```

---

## Verdict Decision Tree

```
Has P0 issues? → NOT READY
Has P1 issues? → READY WITH CONDITIONS (list required fixes)
Only P2 or lower? → READY (with recommendations)
```

## Key Principle

The question is not "does this work?" but "when this breaks at 3am, can the on-call engineer find the problem, understand it, and fix it — without reading the source code?"
