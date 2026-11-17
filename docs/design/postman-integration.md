# Postman integration plan

**Status:** Planned; not implemented.

## Purpose and scope

Use Postman to explore the HTTP API, demonstrate the fishing workflow, and run
an end-to-end smoke test. This complements Python tests; it does not replace
deterministic tests of domain rules, time boundaries, or random selections.

The [fishing requirements](fishing-requirements.md) remain the source of truth
for behavior. No application, collection, environment export, or CI job exists
yet. This plan does not select endpoint paths or add API requirements.

## OpenAPI and collection maintenance

Once the FastAPI application exists, import its local OpenAPI schema into
Postman. With FastAPI's default configuration and a local server on port 8000:

- `http://localhost:8000/openapi.json` provides the schema.
- `http://localhost:8000/docs` provides interactive Swagger UI.

These are planned defaults, not currently available services. Add the actual
startup command to the root README with the application scaffold.

Use the generated OpenAPI schema as the source of truth for implemented API
shapes, and the Postman collection for workflow sequencing and assertions.
An import is a snapshot, not continuous synchronization. When contracts change,
review the schema changes, regenerate or update affected requests, preserve
workflow scripts, and review the collection diff in the same change.

## Planned repository artifacts

Add these files when the first endpoints can be exercised:

```text
postman/
  README.md
  bobby-jenkins.postman_collection.json
  local.postman_environment.json
```

- The README will document import, startup prerequisites, interactive execution,
  the exact command-line runner command, and supported tool versions.
- The collection will contain requests, assertions, and workflow scripts.
- The local environment will contain only non-secret defaults, initially
  `baseUrl = http://localhost:8000`. Requests will use `{{baseUrl}}`.

Use a collection export format compatible with Newman and verify compatibility
with the selected Postman and Newman versions before adopting them. Pin the
runner version when CI is introduced.

Keep credentials, tokens, real user data, and sensitive locations out of
committed exports and reports. If authentication is added, inject secrets
locally or through CI secret storage. Review exports before committing them.
Repository-based execution must not require uploading project data to a shared
Postman cloud workspace.

## Fishing workflow smoke test

The collection should create its own attempt and capture returned identifiers
as collection variables rather than requiring manual copying. Reset run-specific
variables at the start so stale identifiers cannot make a later run pass.

| Step | Planned assertion | Requirements |
| --- | --- | --- |
| Set up and cast | A fresh setup permits a cast and the attempt enters waiting. | FR-02, FR-03, AC-01 |
| Observe uncaught status | An addressable not-yet-caught barracuda returns `404`. | FR-08, AC-06 |
| Wait for a bite | Bounded polling observes a barracuda on the line before pulling. | FR-04, FR-05 |
| Pull until caught | Stop at catch completion; fail if four valid pulls do not complete the catch under the default configuration. | FR-05, FR-06 |
| Query caught status twice | Each response is `200` with the exact JSON body `{"status": "screaming"}`. | FR-07, AC-05 |
| Cast again without setup | The cast is rejected using the eventual documented error contract. | FR-03, AC-07 |
| Set up again and cast | A fresh setup permits another attempt. | FR-02, FR-03, AC-07 |
| Query a nonexistent barracuda | The response is `404`, using a fixture or identifier known not to exist. | FR-08, AC-06 |

Resource identifiers, observing attempt state, and invalid-action responses
depend on future endpoint contracts. In particular, do not assume a barracuda
identifier is available immediately after casting. Resolve those contracts before
implementing these requests; do not invent routes or response fields in scripts.

### Timing and randomness

The smoke test exercises real default timing: a randomly selected 5–10 second
wait and a fixed, randomly selected 1–4 pull threshold per bite.

Poll at a documented interval with a finite overall deadline, request timeouts,
and an iteration bound. Choose and document the deadline with allowance for the
10-second maximum bite wait plus request/scheduling overhead. Unexpected
responses or an exhausted bound must fail the run, not silently skip assertions.
Do not pull after catch completion or retry mutating requests blindly.

This smoke test demonstrates a real workflow; it cannot prove all random outcomes
or exact timing boundaries. Python tests should control the clock and random
source to cover AC-03 and AC-04, including both bounds and threshold stability,
without real sleeps. No production-only bypass or force-catch endpoint is needed.

## Planned CI execution

After the complete workflow exists, add a job that:

1. Starts an isolated test instance using the documented application command.
2. Waits for readiness with a bounded check.
3. Runs the repository collection and environment with a pinned Newman version.
4. Fails on request, assertion, timeout, or workflow-bound failures and publishes
   a non-secret test report.
5. Stops the application and disposes of test state even if the run fails.

Use a disposable local instance, not production or a shared mutable environment.
Define test-state isolation and cleanup when persistence is selected. Keep this
real-time smoke job separate from the fast deterministic Python suite.

## Alternatives and rationale

- **Swagger UI alone:** useful for individual requests, but does not capture
  repeatable multi-request workflows and assertions.
- **Postman alone:** convenient for demonstrations, but real delays and randomness
  make exhaustive domain checks slow and unreliable.
- **Shared cloud workspace as the only source:** adds account and synchronization
  dependencies. Prefer reviewable repository exports; cloud collaboration is
  optional and requires a separate decision about what may be shared.

## Rollout and completion criteria

1. **Now:** document the plan without placeholder exports or speculative endpoints.
2. **First endpoints:** import OpenAPI, add the collection and safe environment,
   and document exact import/run commands and supported versions.
3. **Complete fishing flow:** add scripted identifiers, bounded polling, and the
   assertions above; demonstrate a clean run and a deliberately failing assertion.
4. **CI:** automate the same collection against an isolated instance, retain
   reports, and verify failure propagation and cleanup.

Before implementation, resolve endpoint/state-observation contracts, runner
versions and export compatibility, polling limits, readiness checks, and test
data lifecycle. Authentication and cloud sharing remain separate decisions.

## References

- [FastAPI metadata and documentation URLs](https://fastapi.tiangolo.com/tutorial/metadata/)
- [Import an API into Postman](https://learning.postman.com/docs/design-apis/specifications/import-a-specification/)
- [Newman command-line runner](https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/)
