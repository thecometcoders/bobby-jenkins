# Development workflow

## Toolchain and setup

Use uv 0.13.6 (the version pinned in CI) and Python 3.14. Install uv using
[Astral's installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
uv can download Python if a suitable interpreter is not already installed.

```sh
uv sync --locked
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
uv build
```

Select `.venv`'s Python interpreter in your editor. Environment activation is
optional when commands use `uv run`. The package is installed in editable mode,
so source changes take effect without reinstalling. There is no server command
yet: this scaffold does not implement FastAPI endpoints.

`pyproject.toml` declares metadata and dependencies; `uv.lock` records exact
resolved versions. Commit both when they change. Never commit `.venv` or edit
the lockfile manually. The supported Python range is initially limited to 3.14;
`.python-version` selects that minor version locally. Supporting another minor
version requires an explicit change and corresponding CI coverage.

## Feature branches and main

Create feature branches from current `main`. For example, with a clean checkout:

```sh
git switch main
git pull --ff-only
git switch -c feature/catch-validation
uv sync --locked
```

After switching branches or pulling changes, run `uv sync --locked` again:
the environment must follow the checked-out branch's lockfile. Sync removes
packages not selected for that environment. Ordinary `uv run` can update the
lockfile automatically; `--locked` instead fails when it needs updating.
`--frozen` skips consistency checking and is not our default for CI.

Add dependencies on the branch that needs them:

```sh
uv add some-package
uv add --dev some-tool
uv remove some-package
```

Runtime dependencies belong in `project.dependencies`; development tools belong
in `dependency-groups.dev`, installed by default. Avoid unrelated upgrades.
For intentional upgrades within the declared constraints:

```sh
uv lock --upgrade-package some-package
uv sync
```

Use `uv lock --upgrade` only for an intentional full dependency refresh.
When merging concurrent dependency changes, resolve `pyproject.toml` first,
reconcile the lockfile with `uv lock`, and review the resulting versions.
Do not delete the lockfile as a routine conflict-resolution strategy.

Update the branch with current `main` according to the team's Git policy,
then run the setup/check commands above. Submit the change for review;
CI checks the committed lockfile, tests, lint, formatting, and package build.
Keep `main` passing. Neither a passing check nor this workflow authorizes an
agent to merge or push a change to `main` without explicit approval.

## Application versions and releases

Use [Semantic Versioning](https://semver.org/) in `MAJOR.MINOR.PATCH` form.
After 1.0, increment the major version for incompatible public API changes,
the minor version for backward-compatible functionality, and the patch version
for backward-compatible fixes.

We currently follow a pre-1.0 (`0.y.z`) release strategy: the public API is
still evolving and is not considered stable. Increment the minor version for
new functionality or breaking changes, and the patch version for
backward-compatible fixes. Document breaking changes explicitly in release
notes. Reaching 1.0 will signal a stable public API and the compatibility
guarantees described above.

Feature branches normally leave the package version unchanged; update it when
preparing a release. Commit SHAs identify intermediate builds, including builds
of `main`. Package metadata alone does not mean a release has occurred.

Prepare releases as reviewed changes:

1. Set `[project].version` in `pyproject.toml` to the intended `x.y.z` version
   (without a `v` prefix).
2. Run `uv lock` to update root-package metadata.
3. Run all checks and review the release changes.
4. After authorized merging, tag the exact approved commit as `vx.y.z`, matching
   the package version, and build/deploy that commit through the chosen release
   process.

Package versions do not automatically define API route versions. Publishing to
PyPI is not required and is not configured.

For a runtime-only installation, use
`uv sync --locked --no-dev --no-editable`. Deployment configuration is still
future work. Treat Python and uv upgrades as deliberate toolchain changes:
update their pins and documentation together and revalidate the lockfile.
