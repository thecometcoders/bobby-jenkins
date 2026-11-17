# Design documentation workflow

Use Markdown for context, decisions, alternatives, and unresolved questions.
Use PlantUML (`.puml`) for diagrams stored and reviewed alongside those documents.

## Documents and diagrams

- [Architecture proposal](architecture.md)
- [Agreed fishing requirements](fishing-requirements.md)
- [Postman integration plan](postman-integration.md)
- [Fishing workflow source](diagrams/fishing-workflow.puml)
- [System context source](diagrams/system-context.puml)
- [Request flow source](diagrams/request-flow.puml)

The context and request-flow diagrams are proposals; the fishing workflow diagram
records agreed requirements. No application behavior is implemented yet.

## Render diagrams locally

Prerequisites:

- Java supported by your PlantUML release.
- [PlantUML](https://plantuml.com/download), available as the `plantuml` command.
- [Graphviz](https://graphviz.org/download/), with `dot` on your `PATH`.

For example, on macOS with Homebrew, install the tools with
`brew install plantuml graphviz`. On other platforms use the linked installation
instructions. If you use the standalone JAR, replace `plantuml` below with
`java -jar /path/to/plantuml.jar`.

Run these commands from the repository root:

```sh
# Check all diagram sources without generating images.
plantuml -checkonly docs/design/diagrams/*.puml

# Render SVGs; the output directory is relative to each source directory.
plantuml -failfast2 -tsvg -o rendered docs/design/diagrams/*.puml
```

Open `docs/design/diagrams/rendered/system-context.svg`,
`docs/design/diagrams/rendered/request-flow.svg`, and
`docs/design/diagrams/rendered/fishing-workflow.svg` in a browser.
Generated files are ignored by Git; `.puml` files are the source of truth.
Plain Markdown viewers generally do not render `.puml` files automatically.

Render locally rather than submitting private designs to public PlantUML servers.
If using an editor extension, configure its local renderer and verify it does not
send diagram content to a remote service. Do not use remote `!includeurl` assets.

## Writing a design document

For each substantial design, describe:

1. **Status:** proposed, accepted, superseded, or implemented.
2. **Problem and scope:** the workflow and what is intentionally excluded.
3. **Requirements:** inputs, outputs, access rules, and failure behavior.
4. **Design:** responsibilities and links to `.puml` sources.
5. **Alternatives:** the meaningful tradeoffs and why a direction is recommended.
6. **Validation:** how tests or a real workflow will demonstrate success.
7. **Open questions:** decisions still needed before implementation.

Keep one diagram per `.puml` file, use descriptive filenames, and keep labels
consistent with the prose. Review the rendered diagrams as well as the source.
When a proposal is accepted, record the decision and rationale in its document.

## References

- [PlantUML command-line documentation](https://plantuml.com/command-line)
- [PlantUML integrations](https://plantuml.com/running)
