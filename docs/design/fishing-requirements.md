# Fishing workflow requirements

**Status:** Agreed requirements; not implemented.

This document records the fishing story and the follow-up decisions agreed with
the project owner. It is the source of truth for the initial workflow's behavior.
Endpoint paths, persistence, and implementation mechanisms are not selected here.

## User story

A fisher heads to a lake containing barracudas, sets up a pole with tackle and
bait, and casts. After a random wait, a barracuda takes the bait. The fisher pulls
the line until the barracuda is caught. Asking a caught barracuda for its status
always returns the exact value `"screaming"`.

## Functional requirements

| ID | Requirement |
| --- | --- |
| FR-01 | The fishing activity shall take place at a lake containing barracudas. Lake selection and travel mechanics are not specified. |
| FR-02 | The fisher shall set up the pole with tackle and bait before each cast. Initially, there shall be one supported tackle type and one supported bait type. |
| FR-03 | Casting shall require a completed, fresh setup. A cast uses that setup; another cast requires setup again. Casting without a fresh setup shall be rejected. |
| FR-04 | On each cast, the system shall randomly select a waiting duration using the default bounds below. Before it elapses, the attempt shall remain waiting. When it elapses, a barracuda shall bite. |
| FR-05 | A bite shall put a barracuda on the line, not immediately catch it. At the bite, the system shall initialize progress to zero and randomly select a required pull count using the default bounds below. That threshold shall remain fixed for that catch. |
| FR-06 | Each valid pull after the bite shall add one progress point. When progress reaches or exceeds the selected threshold, the barracuda shall become caught. |
| FR-07 | A successful status query for a caught barracuda shall return HTTP `200` with the JSON body `{"status": "screaming"}`. The exact value shall remain unchanged across repeated queries. |
| FR-08 | A status query for a nonexistent or not-yet-caught barracuda shall return HTTP `404`. The error body is not yet specified. |

## Default mechanics

| Parameter | Agreed default |
| --- | --- |
| Minimum bite wait | 5 seconds |
| Maximum bite wait | 10 seconds |
| Minimum required pulls | 1 |
| Maximum required pulls | 4 |
| Progress per valid pull | 1 |

The wait is selected once per cast within the 5–10 second bounds. Whether time is
sampled in whole seconds or at finer precision, and the probability distribution,
remain unspecified.

The required pull count is an integer selected once per bite from 1 through 4,
inclusive. It is not rerolled on each pull. The probability distribution and how
these defaults can be configured remain unspecified.

## Workflow

[PlantUML state diagram](diagrams/fishing-workflow.puml)

| Current state | Event / condition | Result |
| --- | --- | --- |
| Setup required | Equip the pole with tackle and bait | Ready to cast |
| Ready to cast | Cast | Waiting for bite; select the wait duration |
| Waiting for bite | Selected duration elapses | Barracuda on the line; set progress to zero and select the catch threshold |
| Barracuda on the line | Pull; new progress is below threshold | Remain on the line with increased progress |
| Barracuda on the line | Pull; new progress reaches threshold | Barracuda caught |
| Barracuda caught | Query status | Return `200` and `{"status": "screaming"}`; remain caught |
| Barracuda caught | Begin another fishing attempt | Setup required for the next cast |

Requiring setup again does not, by itself, require finite inventory, bait
consumption, or tackle loss. Beginning another attempt does not define how long a
previously caught barracuda remains addressable; retention remains open.

## Acceptance scenarios

These are specifications for future tests, not claims of implemented behavior.

### AC-01: Cast a prepared pole (FR-02, FR-03)

Given a fisher at a lake with a pole equipped with the supported tackle and bait,
when they cast, then the attempt enters the waiting state.

### AC-02: Reject an incomplete or used setup (FR-02, FR-03)

Given setup is incomplete, or a previous cast has used it and setup has not been
repeated, when the fisher attempts to cast, then the cast is rejected.
The rejection's HTTP status and body remain to be defined.

### AC-03: Wait for the selected bite time (FR-04)

Given a test-controlled random wait of 7 seconds selected at casting,
when less than 7 seconds have elapsed, then the attempt remains waiting.
When 7 seconds have elapsed, then a barracuda is on the line, but is not yet caught.
Boundary tests shall also exercise selected waits of 5 and 10 seconds.

### AC-04: Keep the selected catch threshold fixed (FR-05, FR-06)

Given a bite with a test-controlled threshold of 3 pulls and zero progress,
when the fisher pulls twice, then progress is 2 and the barracuda is not caught.
When they pull a third time, then the barracuda is caught.
The threshold is selected only at the bite, not again during those pulls.
Boundary tests shall also verify catches requiring 1 and 4 pulls.

### AC-05: Return the exact caught status repeatedly (FR-07)

Given a caught barracuda, when its status is queried repeatedly, then each
successful response is HTTP `200` with `{"status": "screaming"}`.

### AC-06: Hide uncaught and nonexistent barracudas (FR-08)

Given either a nonexistent barracuda or one not yet caught, when its status is
queried, then the response is HTTP `404`. This includes a barracuda on the line
whose catch threshold has not been reached.

### AC-07: Require setup for the next cast (FR-02, FR-03)

Given a completed catch, when the fisher attempts another cast without setting
up again, then it is rejected. After a fresh setup, another cast is permitted and
a new wait duration is selected.

Tests should control time and random selections so they are deterministic and
do not sleep for real bite delays. The mechanism for doing so is an implementation
decision, not an additional game rule.

## Remaining decisions and scope boundaries

- Endpoint paths, resource identifiers, and response contracts other than the
  specified status query.
- Rejection behavior for pulls before a bite or after a catch, repeated setup,
  and casts while an attempt is active.
- Whether multiple attempts may be active, and how concurrent or retried requests
  are handled.
- Cancellation, abandonment, escape, and timeout behavior; none is required yet.
- Random sampling distribution, time precision, and configuration interface.
- Persistence, caught-barracuda retention, identity, and access rules.
- Lake selection, inventory, additional equipment types, and location features
  are not part of the agreed initial mechanics.
