# Bobby Jenkins

Bobby Jenkins is a Python web application built with [FastAPI](https://fastapi.tiangolo.com/)
to provide a backend for Barracuda Fishing.

## Project status

This repository currently contains project documentation and proposed designs.
Application code, dependencies, API endpoints, and deployment configuration have
not been added yet. The diagrams describe a starting proposal, not a running system.

## Documentation

- [Architecture proposal](docs/design/architecture.md): scope, boundaries, and open questions.
- [Fishing requirements](docs/design/fishing-requirements.md): agreed mechanics and acceptance scenarios.
- [Design documentation workflow](docs/design/README.md): write and render PlantUML locally.
- [License research](docs/licensing.md): MIT, BSD, GPL, and the implications for a hosted API.

## Getting started

Start with the agreed fishing requirements and the architecture proposal.
The first workflow is defined, but endpoint design remains open. There is no
application installation or startup command yet; those instructions will be
added with the FastAPI scaffold.

To work on design documents, install PlantUML and Graphviz and follow the
[local rendering instructions](docs/design/README.md#render-diagrams-locally).
Python is not required to render the diagrams.

## Initial roadmap

- [x] Confirm the first user workflow and fishing mechanics.
- [ ] Define endpoint contracts and remaining API behavior.
- [ ] Choose a project license and identify the copyright holder.
- [ ] Scaffold the FastAPI application, dependency management, and tests.
- [ ] Implement and test the first end-to-end API workflow.
- [ ] Document persistence, authentication, and deployment as requirements become clear.

## Contributing

Keep proposals clearly distinguished from implemented behavior. Update relevant
design documents and PlantUML sources alongside changes to system behavior.
Do not put credentials, real user records, or sensitive fishing locations in examples.

## License

No project license has been selected. Publicly accessible source is not, by itself,
an open-source license grant. See the [license comparison](docs/licensing.md)
before deciding how to license or reuse the project.
