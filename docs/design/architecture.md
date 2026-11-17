# Bobby Jenkins architecture

**Status:** Proposed; not implemented.

This document follows the 12-section [arc42 architecture template](https://arc42.org/overview).
arc42 was created by Peter Hruschka and Gernot Starke and is available under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The structure is adapted here with project-specific content; this attribution
does not select a software license for Bobby Jenkins.

## 1. Introduction and Goals

### 1.1 Requirements overview

Bobby Jenkins provides the Python/FastAPI backend for Barracuda Fishing.
The first goal is to define the API's responsibilities before introducing
application code or infrastructure.

The first user workflow is agreed: set up a pole, cast, wait for a random bite,
pull until caught, and query the barracuda's exact `"screaming"` status.
The [fishing requirements](fishing-requirements.md) record the default timing,
pull thresholds, HTTP status behavior, and acceptance scenarios.
These requirements are not implemented. Catch logs, trip planning, and location
features are not committed requirements.

### 1.2 Quality goals

These are proposed priorities, pending agreement with project stakeholders.
Section 10 describes how they should be validated.

| Goal | Motivation |
| --- | --- |
| Simplicity | Keep development and operation manageable while requirements emerge. |
| Testability | Verify each agreed workflow through its API boundary. |
| Security and privacy | Define access rules before exposing protected operations or storing sensitive data. |
| Understandability | Keep API contracts, design documents, and diagrams consistent with implemented behavior. |

### 1.3 Stakeholders

| Stakeholder role | Architectural concern |
| --- | --- |
| Project owners | Product scope, licensing, and operating model. |
| Backend contributors | Clear responsibilities, development workflow, and testable contracts. |
| Client developers | API inputs, outputs, errors, and access requirements. |
| Barracuda Fishing users | Correct behavior and appropriate protection of their information. |

The initial user role is the fisher. Specific stakeholder representatives and
additional user roles have not been identified.

## 2. Architecture Constraints

| Constraint | Status |
| --- | --- |
| Python is the backend language. | Confirmed project choice; version not selected. |
| FastAPI is the web framework. | Confirmed project choice. |
| Markdown and PlantUML are used for design documentation. | Established documentation approach. |
| Software licensing | Not selected; see [license research](../licensing.md). |

No database, identity provider, deployment platform, dependency manager, external
integration, or regulatory requirement has been established.

## 3. Context and Scope

### 3.1 Business context

[System context diagram](diagrams/system-context.puml)

Users interact with Barracuda Fishing through a client application. Bobby Jenkins
provides the backend behavior for agreed workflows. A client application is
outside this repository's initial backend scope.

The initial fisher workflow exchanges setup, cast, pull, and barracuda-status
information, as described in the [requirements](fishing-requirements.md).
Additional user roles and external business systems remain to be defined.

### 3.2 Technical context

Clients call Bobby Jenkins over an HTTP API, with HTTPS proposed outside local
development. The backend validates requests, applies the agreed fishing-domain
rules, and returns documented responses.

Client types, endpoint paths, domain schemas, authentication, and external
interfaces have not been chosen. The context diagram is a proposal, not an
inventory of deployed systems.

## 4. Solution Strategy

**Recommend a single deployable FastAPI application initially.** It keeps local
development, deployment, and end-to-end tests straightforward while requirements
are emerging.

Separate services would add network boundaries and operational costs without a
known scaling or ownership need. Revisit this direction only with concrete
evidence.

Keep simple handlers simple; extract shared logic as actual workflows justify it.
Introduce persistence boundaries when storage requirements are known. Do not
select a database, identity provider, background queue, or external weather/maps
service merely to fill out a diagram.

## 5. Building Block View

### 5.1 Level 1: backend responsibilities

The proposed application has two logical responsibilities:

| Building block | Responsibility | Interface |
| --- | --- | --- |
| API boundary | Request/response schemas, HTTP routing, and input validation. | HTTP requests and responses; calls application logic. |
| Application logic | Rules for each confirmed Barracuda Fishing workflow. | Called by the API boundary; contracts remain to be defined. |

These are logical boundaries, not requirements for separate packages or services.
No source-code modules exist yet. More detailed building blocks should be added
when implementation and domain requirements justify them.

## 6. Runtime View

### 6.1 Request validation and successful execution

[Request flow diagram](diagrams/request-flow.puml)

1. A client sends an HTTP request to an endpoint yet to be defined.
2. The API boundary validates the request against its schema.
3. Invalid request input receives FastAPI's typical `422` validation response.
4. For valid input, application logic executes the agreed workflow.
5. A successful result is returned using the endpoint's future response contract.

This scenario is illustrative, not implemented. Domain errors, access denials,
and operational failures need explicit contracts and runtime scenarios when
endpoints are designed.

### 6.2 Agreed fishing lifecycle

[Fishing workflow diagram](diagrams/fishing-workflow.puml)

The lifecycle separates setup, waiting for a bite, pulling the line, and a
completed catch. A fresh setup is required for each cast. Random wait durations
are selected once per cast; random pull thresholds are selected once per bite
and remain fixed for the catch.

The [fishing requirements](fishing-requirements.md) define the agreed defaults,
state transitions, and caught/uncaught status-query responses.
Timing mechanisms, endpoint paths, and storage remain implementation decisions.

## 7. Deployment View

**Open:** No runtime infrastructure or deployment configuration exists yet.

The strategy proposes one deployable backend application, but does not select
hosting, process management, TLS termination, storage, or network topology.
Decide whether this is a hosted service, a self-hosted distribution, or both before
documenting concrete deployment nodes and environments.

Add exact installation, startup, and test commands to the root README with the
FastAPI scaffold.

## 8. Crosscutting Concepts

### 8.1 API contracts and validation

Define request/response schemas and success and failure behavior for each
implemented workflow. Input validation belongs at the API boundary; domain rules
belong in application logic where separation is useful.

### 8.2 Authentication, authorization, and privacy

Authentication and authorization remain unresolved and must be designed before
exposing protected operations. Determine data ownership, access rules, and
sensitivity before storing user records or fishing locations. Do not put
credentials or real sensitive records in documentation examples.

### 8.3 Persistence and operations

Persistence, configuration and secret management, logging, monitoring, and error
handling conventions remain open. Define them as confirmed workflows and
deployment requirements make them necessary.

### 8.4 Documentation

Keep proposed and implemented behavior clearly distinguished. Update design
documents and PlantUML sources alongside changes to system behavior. Check diagram
syntax and render the diagrams using the
[documentation workflow](README.md#render-diagrams-locally).

## 9. Architectural Decisions

| Decision | Status | Rationale / reference |
| --- | --- | --- |
| Use Python and FastAPI for the backend. | Confirmed project choice. | Project's stated technology direction; see section 2. |
| Start with a single deployable application. | Proposed. | Simpler development and operations than separate services at the current scope; see section 4. |
| Defer infrastructure choices until requirements justify them. | Proposed. | Avoid speculative dependencies and operational costs; see section 4. |

Record acceptance and rationale changes here as decisions are made. Substantial
future decisions may link to separate architecture decision records rather than
duplicating their content.

## 10. Quality Requirements

### 10.1 Quality overview

The initial quality concerns are simplicity, testability, security/privacy, and
understandability, as proposed in section 1.2. Stakeholder priorities, performance
targets, availability expectations, and recovery objectives remain open.

### 10.2 Proposed quality scenarios

| Scenario | Expected response / validation |
| --- | --- |
| A client submits valid input for the first workflow. | An API-level test verifies its agreed success response and domain outcome. |
| A client submits malformed input or violates a domain rule. | Tests verify the documented validation or domain-error contract. |
| A caller attempts a protected operation without sufficient access. | If accounts/protected operations are required, tests verify denial without disclosure of protected data. |
| A workflow stores user-owned data. | If persistence is required, tests verify storage behavior and isolation according to agreed access rules. |
| A contributor changes system behavior. | Relevant contracts, design text, and diagrams are updated; PlantUML checks and rendering succeed. |

The [fishing acceptance scenarios](fishing-requirements.md#acceptance-scenarios)
cover random-wait boundaries, fixed per-catch thresholds, fresh setup, and exact
status-query responses. Tests should control time and randomness rather than
sleeping or relying on chance.

These are planned acceptance checks, not evidence of passing application tests.
Agree on measurable service-level targets before introducing performance or
availability claims.

## 11. Risks and Technical Debt

### 11.1 Known risks

| Risk | Proposed mitigation |
| --- | --- |
| Unresolved API edge cases lead to speculative architecture. | Use the agreed fishing requirements and resolve remaining API behavior before choosing supporting infrastructure. |
| Undefined access rules expose sensitive information. | Resolve identity, authorization, and data ownership before protected operations are exposed. |
| An unresolved license creates uncertainty about reuse and contributions. | Identify copyright holders and select a license before presenting the project as open source. |
| Design proposals are mistaken for implemented capabilities. | Preserve status labels and update documentation with implementation changes. |

No implementation technical debt has been assessed because application code has
not been added. Open design choices are not, by themselves, technical debt.

### 11.2 Open questions

1. What endpoint contracts and invalid-action rules should support the agreed
   fishing workflow? See [remaining decisions](fishing-requirements.md#remaining-decisions-and-scope-boundaries).
2. What information must the backend store, and who may read or change it?
3. Are accounts required? Are location data or other sensitive records involved?
4. Will this be a hosted service, a self-hosted distribution, or both?
5. Should downstream improvements remain open, or should proprietary reuse be allowed?
6. What Python version, dependency manager, and deployment environment should we support?

## 12. Glossary

| Term | Meaning in this document |
| --- | --- |
| Barracuda Fishing | The product/domain served by this backend; its initial fishing workflow is defined in the fishing requirements. |
| Bobby Jenkins | The Python/FastAPI backend application described here. |
| API boundary | The logical responsibility for HTTP routing, schemas, and request validation. |
| Application logic | The logical responsibility for agreed fishing-domain rules and workflows. |
| Client | An application that calls the backend API; client types are not yet selected. |
| PlantUML | The text-based diagram tool used for version-controlled design diagrams. |
| Fisher | The user who sets up a pole, casts, and pulls the line to catch a barracuda. |
| Bite | The event after the selected wait that puts a barracuda on the line; it is not a completed catch. |
| Catch threshold | The required pull count selected at a bite and kept fixed until the catch completes. |
