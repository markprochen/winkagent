# WinkAgent Public Rebrand Design

## Goal

Rebrand the public-facing Codex CLI as WinkAgent without changing runtime
behavior or breaking existing user configuration.

## Scope

The public product name changes from Codex to WinkAgent.

The primary command changes from `codex` to `winkagent`.

The npm meta package changes from `@openai/codex` to `winkagent`. Platform
packages change from `@openai/codex-*` to `winkagent-*`.

The top-level Rust CLI package changes from `codex-cli` to `winkagent-cli`.
Its primary binary and default run target change from `codex` to `winkagent`.

User-visible names in the README, CLI help, TUI, diagnostics, package
descriptions, release instructions, and relevant snapshots change to
WinkAgent. Upstream documentation links and required legal attribution remain
intact.

## Compatibility Boundaries

The following identifiers remain unchanged:

- `CODEX_HOME` and all other `CODEX_*` environment variables
- `~/.codex` and project-local `.codex` configuration directories
- Internal `codex-*` Rust crates, module names, exported types, and protocol
  fields
- App-server and API protocol identifiers
- Helper executable names such as `codex-command-runner`,
  `codex-code-mode-host`, and `codex-windows-sandbox-setup`
- OpenAI service URLs, update feeds, authentication flows, and model metadata
- Apache license, notices, and required upstream attribution

These boundaries preserve existing configuration, compatibility, and
behavior. Internal symbols are not renamed merely for branding.

## Components

### Rust CLI

Update the top-level package metadata, default run target, primary binary
name, and user-facing Clap descriptions. Keep the library crate name and all
internal crate dependencies unchanged.

### Node Launcher and npm Packages

Rename the launcher entry point and package metadata to `winkagent`. Update
platform package aliases, executable lookup, install guidance, staging
scripts, archive names, and package smoke-test expectations.

### User-Facing Branding

Replace public Codex brand text with WinkAgent in the README, CLI/TUI output,
doctor output, and related snapshots. Do not rewrite internal comments,
protocol documentation, or compatibility identifiers that are not normally
shown to users.

### Build and Release Metadata

Update package and artifact names where they describe the public WinkAgent
product. Keep helper binary names and compatibility environment variables
unchanged.

## Data Flow

The user invokes `winkagent`. The Node launcher resolves the renamed
platform package and launches the `winkagent` native binary. The native
process continues to use `CODEX_HOME`, `~/.codex`, existing configuration,
protocol messages, authentication, and helper executables exactly as before.

## Error Handling

No new error behavior is introduced. Missing-package and missing-binary
messages refer to WinkAgent and instruct the user to reinstall or update
WinkAgent. Existing retry, fallback, sandbox, and authentication behavior
remains unchanged.

## Testing

Verification will cover:

- Rust workspace metadata and compilation of the renamed CLI target
- Node launcher package metadata and binary lookup tests
- CLI help/version output using `winkagent`
- User-visible TUI and doctor snapshot updates
- Package staging and archive-name tests
- A repository audit confirming compatibility identifiers such as
  `CODEX_HOME`, `.codex`, and internal helper names were not changed

The implementation is complete when WinkAgent builds and runs through the
renamed public entry points while existing Codex configuration and runtime
behavior remain compatible.

## Non-Goals

- Renaming every internal `codex` symbol or source directory
- Changing configuration paths or environment variables
- Changing authentication, model, protocol, sandbox, or update behavior
- Publishing packages or creating release infrastructure
- Removing OpenAI license notices or upstream attribution
