# Fishing API contract

**Status:** Planning skeleton; not implemented. Endpoint paths and HTTP details
below are proposed. Gameplay decisions explicitly described as agreed are
recorded in the [fishing requirements](fishing-requirements.md).

## Agreed direction

- A fisher owns their attempts and catches. Only the owner can access them.
- Each fisher can have at most one active attempt, including setup and ready states.
- Clients see current pull progress, never the required pull threshold.
- At the hidden threshold, roll once: 40% caught, 60% escaped. Do not roll per pull.
- Either outcome ends the attempt. The next attempt requires fresh setup.
- Successful catches enter the owner's catch archive automatically.
- Releasing a catch preserves its history but makes its live status unavailable.
- Mutating actions use idempotency keys to prevent duplicate effects on retries.

## Proposed endpoints

Base path: `/api/v1`. Resolve ownership from the authenticated caller, not a
client-supplied fisher ID. The authentication mechanism remains open.

| Method | Path | Purpose | Success |
| --- | --- | --- | --- |
| POST | `/attempts` | Create an attempt in `setup_required` | 201 |
| PUT | `/attempts/{id}/setup` | Equip the single supported tackle and bait types | 200 |
| POST | `/attempts/{id}/cast` | Consume fresh setup and begin waiting | 200 |
| GET | `/attempts/{id}` | Read state and current progress | 200 |
| POST | `/attempts/{id}/pulls` | Apply one pull and resolve the outcome at the threshold | 200 |
| GET | `/barracudas` | List catch history, including released catches | 200 |
| GET | `/barracudas/{id}/status` | Read an owned, retained catch's live status | 200 |
| POST | `/barracudas/{id}/release` | Release a catch without deleting history | 200 |

Create a new attempt for each cycle rather than resetting an old one. Enforce
the one-active-attempt rule even when requests arrive concurrently.

## Proposed representations

Attempt responses share this shape:

```json
{
  "id": "attempt_123",
  "state": "on_line",
  "tackle_type": "standard",
  "bait_type": "standard",
  "pull_progress": 2,
  "barracuda_id": "barracuda_456"
}
```

States: `setup_required`, `ready`, `waiting`, `on_line`, `caught`, `escaped`.
The last two are terminal. Equipment fields are null before setup;
`barracuda_id` is null before a bite. `standard` is a placeholder for the
supported equipment names, not an additional equipment requirement.

Setup accepts `{"tackle_type": "standard", "bait_type": "standard"}`.
Other action requests have no body. Create returns the new attempt; setup, cast,
and pull return the updated attempt. Never expose the selected threshold or
future catch outcome.

For an owned caught barracuda that has not been released, the status response
is exactly `{"status": "screaming"}`. Nonexistent, uncaught, released, and
other-owned barracudas return 404. Historical catch records distinguish retained
from released catches; their schema and list pagination remain open.

## Proposed action and error rules

- Return 404 for unknown or other-owned resources.
- Return 409 when creating an attempt while another is active.
- Return 409 for casting without fresh setup, casting an already-cast attempt,
  changing setup after casting, or pulling outside `on_line`.
- Repeating setup before casting is allowed and leaves the attempt ready.
- Return 422 for invalid inputs, using FastAPI's validation response.
- Start with polling the attempt to observe a bite. Time passage, not the number
  of polls, determines when a bite occurs. Pulls must also account for elapsed time.

Proposed domain error body:

```json
{
  "detail": {
    "code": "attempt_not_on_line",
    "message": "Pulling requires a barracuda on the line."
  }
}
```

## Idempotency and concurrency

Require `Idempotency-Key` for attempt creation, casting, pulling, and release.
Setup is an idempotent PUT.

- Scope keys to the authenticated fisher.
- The same key and request replay the original result without another effect.
- Reusing a key for a different method, target, or body returns 409.
- Each intentional new pull requires a new key.
- Concurrent duplicate requests must not apply the action twice.
- Serialize competing actions so progress and the terminal outcome are committed
  consistently. Resolve the catch outcome only once, including during retries.

Key retention, in-flight duplicate responses, replayable error categories, and
repeated release with a new key need contracts before implementation.

## Acceptance checklist

- Concurrent creation cannot produce two active attempts for one fisher.
- Another fisher cannot read or mutate an attempt or catch.
- Replayed pulls do not increment progress or reroll outcomes.
- Neither polls nor action responses reveal the hidden threshold.
- Controlled randomness exercises both catch and escape at the threshold.
- Both terminal outcomes permit a new attempt requiring fresh setup.
- A catch appears in history; release preserves that record and hides live status.

Retain the timing, setup, and fixed-threshold checks in the fishing requirements.
Use controlled time and randomness rather than sleeping or probabilistic tests.

## Still to decide

- Authentication, persistence, record retention, and archive pagination/schema.
- Idempotency retention and the remaining retry/error details above.
- Wait-time precision and distribution; pull-threshold distribution.
- Cancellation or recovery for an abandoned active attempt.

No database, identity provider, background worker, or deployment platform is
selected by this skeleton.
