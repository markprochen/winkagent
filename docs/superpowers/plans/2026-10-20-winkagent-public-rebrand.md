# WinkAgent Public Rebrand Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebrand the public Codex CLI package, command, and visible product name as WinkAgent without changing compatibility identifiers or runtime behavior.

**Architecture:** Keep all internal `codex-*` crates, `CODEX_*` environment variables, `.codex` directories, protocol fields, and helper executables intact. Change only the public npm package names, primary CLI package and binary, public artifact names, user-facing brand text, and matching tests.

**Tech Stack:** Rust 2024/Cargo/Clap, Node.js ESM, Python packaging scripts, npm package metadata, shell/PowerShell installers, Insta snapshots.

## Global Constraints

- Product display name is exactly `WinkAgent`.
- Public command and npm package name are exactly `winkagent`.
- Platform npm packages use `winkagent-<platform>`.
- Rust CLI package is `winkagent-cli`; its primary binary is `winkagent`.
- `CODEX_HOME`, every `CODEX_*` environment variable, `~/.codex`, `.codex`, app-server protocol fields, and helper names beginning with `codex-` remain unchanged.
- Internal Rust crates remain named `codex-*`.
- OpenAI service URLs, authentication, updates, models, sandbox behavior, and protocol behavior remain unchanged.
- Apache license, notices, and upstream attribution remain intact.
- Do not publish packages.

---

### Task 1: Rename Public Node and npm Package Surfaces

**Files:**
- Create: `codex-cli/tests/rebrand.test.mjs`
- Create: `codex-cli/tests/test_rebrand.py`
- Rename: `codex-cli/bin/codex.js` to `codex-cli/bin/winkagent.js`
- Modify: `codex-cli/package.json`
- Modify: `codex-cli/scripts/build_npm_package.py`

**Interfaces:**
- Consumes: no earlier task outputs.
- Produces: npm package `winkagent`, binary entry `winkagent`, launcher file `bin/winkagent.js`, and platform package map `winkagent-*`.

- [ ] **Step 1: Write the failing Node package contract test**

Create `codex-cli/tests/rebrand.test.mjs`:

```javascript
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import test from "node:test";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));
const packageJson = JSON.parse(
  readFileSync(new URL("package.json", new URL("..", import.meta.url)), "utf8"),
);

test("npm package exposes the winkagent command", () => {
  assert.equal(packageJson.name, "winkagent");
  assert.deepEqual(packageJson.bin, {
    winkagent: "bin/winkagent.js",
  });
  assert.match(packageJson.description, /WinkAgent/);
});

test("launcher resolves WinkAgent platform packages and binary", () => {
  const launcher = readFileSync(
    new URL("bin/winkagent.js", new URL("..", import.meta.url)),
    "utf8",
  );
  assert.match(launcher, /winkagent-win32-x64/);
  assert.match(launcher, /winkagent-linux-x64/);
  assert.match(launcher, /winkagent\.exe/);
  assert.match(launcher, /CODEX_MANAGED_PACKAGE_ROOT/);
  assert.doesNotMatch(launcher, /@openai\/codex/);
  assert.equal(packageRoot.endsWith("codex-cli/"), true);
});
```

- [ ] **Step 2: Write the failing Python build-script test**

Create `codex-cli/tests/test_rebrand.py`:

```python
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_npm_package.py"
SPEC = importlib.util.spec_from_file_location("build_npm_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RebrandTests(unittest.TestCase):
    def test_meta_package_name(self) -> None:
        self.assertEqual(MODULE.CODEX_NPM_NAME, "winkagent")

    def test_platform_package_names(self) -> None:
        self.assertEqual(
            MODULE.CODEX_PLATFORM_PACKAGES["winkagent-linux-x64"]["npm_name"],
            "winkagent-linux-x64",
        )
        self.assertEqual(
            MODULE.CODEX_PLATFORM_PACKAGES["winkagent-win32-arm64"]["npm_name"],
            "winkagent-win32-arm64",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run both tests and verify RED**

Run: `node --test codex-cli/tests/rebrand.test.mjs`
Expected: FAIL because package name is still `@openai/codex`.

Run: `python codex-cli/tests/test_rebrand.py`
Expected: FAIL because `CODEX_NPM_NAME` is still `@openai/codex`.

- [ ] **Step 4: Rename the launcher and update its public identifiers**

Run: `Move-Item -LiteralPath 'codex-cli/bin/codex.js' -Destination 'codex-cli/bin/winkagent.js'`

In `codex-cli/bin/winkagent.js`, make these exact public changes:

```javascript
// Unified entry point for the WinkAgent CLI.
const PLATFORM_PACKAGE_BY_TARGET = {
  "x86_64-unknown-linux-musl": "winkagent-linux-x64",
  "aarch64-unknown-linux-musl": "winkagent-linux-arm64",
  "x86_64-apple-darwin": "winkagent-darwin-x64",
  "aarch64-apple-darwin": "winkagent-darwin-arm64",
  "x86_64-pc-windows-msvc": "winkagent-win32-x64",
  "aarch64-pc-windows-msvc": "winkagent-win32-arm64",
};

const executableName =
  process.platform === "win32" ? "winkagent.exe" : "winkagent";
```

Replace package-manager update commands with `winkagent@latest` and error text with `Reinstall WinkAgent`. Keep all `CODEX_MANAGED_*` environment variables unchanged.

- [ ] **Step 5: Update npm metadata and build script**

Set `codex-cli/package.json` to:

```json
{
  "name": "winkagent",
  "version": "0.0.0-dev",
  "description": "WinkAgent is a coding agent that runs locally on your computer.",
  "license": "Apache-2.0",
  "bin": {
    "winkagent": "bin/winkagent.js"
  },
  "type": "module",
  "engines": {
    "node": ">=16"
  },
  "files": [
    "bin/winkagent.js"
  ],
  "repository": {
    "type": "git",
    "url": "git+https://github.com/openai/codex.git",
    "directory": "codex-cli"
  },
  "packageManager": "pnpm@10.34.5+sha512.a4ee05f2f73658255bd6a89859c065a45c28a57daefae2c893a168ee2b73168c37b91e83e57ea67654ad03f03031746430e8bce38e362e042605fb8abc80192e"
}
```

In `codex-cli/scripts/build_npm_package.py`, rename the public constants and keys:

```python
CODEX_NPM_NAME = "winkagent"

CODEX_PLATFORM_PACKAGES = {
    "winkagent-linux-x64": {
        "npm_name": "winkagent-linux-x64",
        "npm_tag": "linux-x64",
        "target_triple": "x86_64-unknown-linux-musl",
        "os": "linux",
        "cpu": "x64",
    },
}

PACKAGE_EXPANSIONS = {
    "winkagent": ["winkagent", *CODEX_PLATFORM_PACKAGES],
}

PACKAGE_NATIVE_COMPONENTS = {
    "winkagent": [],
}
```

Populate all six platform entries with the same naming pattern. Change the default package to `winkagent`, copy `bin/winkagent.js`, and use `bin/winkagent.js` in `files`.

- [ ] **Step 6: Run both tests and verify GREEN**

Run: `node --test codex-cli/tests/rebrand.test.mjs`
Expected: PASS.

Run: `python codex-cli/tests/test_rebrand.py`
Expected: PASS.

- [ ] **Step 7: Commit Task 1**

```powershell
git add codex-cli
git -c user.name="WinkAgent" -c user.email="winkagent@localhost" commit -m "feat: rebrand public npm package as WinkAgent"
```

---

### Task 2: Rename the Rust CLI Package and Primary Binary

**Files:**
- Modify: `codex-rs/cli/Cargo.toml`
- Modify: `codex-rs/cli/src/main.rs`
- Modify: all Rust tests containing `cargo_bin("codex")`
- Modify: `codex-rs/cli/tests/app_server_daemon/package.rs`
- Modify: `codex-rs/cli/tests/app_server_daemon_windows.rs`

**Interfaces:**
- Consumes: public command name `winkagent` from Task 1.
- Produces: Cargo package `winkagent-cli`, binary target and `CARGO_BIN_EXE_winkagent`, Clap `bin_name = "winkagent"`.

- [ ] **Step 1: Add a failing Rust branding test**

Inside the existing `#[cfg(test)] mod tests` in `codex-rs/cli/src/main.rs`, add:

```rust
#[test]
fn winkagent_branding_is_public() {
    let command = MultitoolCli::command();
    assert_eq!(command.get_name(), "winkagent");
    assert!(
        command
            .get_about()
            .is_some_and(|about| about.to_string().contains("WinkAgent"))
    );
}
```

- [ ] **Step 2: Run the test and verify RED**

Run: `cargo test -p codex-cli winkagent_branding_is_public -- --exact`
Expected: FAIL because the command name is `codex`.

- [ ] **Step 3: Update Cargo and Clap metadata**

Change `codex-rs/cli/Cargo.toml`:

```toml
[package]
name = "winkagent-cli"
default-run = "winkagent"

[[bin]]
name = "winkagent"
path = "src/main.rs"
```

Keep `logs_client`, the test target, and the `[lib] name = "codex_cli"` unchanged.

Change `MultitoolCli` in `codex-rs/cli/src/main.rs`:

```rust
/// WinkAgent CLI
///
/// If no subcommand is specified, options will be forwarded to the interactive CLI.
#[derive(Debug, Parser)]
#[clap(
    author,
    version,
    subcommand_negates_reqs = true,
    bin_name = "winkagent",
    override_usage = "winkagent [OPTIONS] [PROMPT]\n       winkagent [OPTIONS] <COMMAND> [ARGS]"
)]
struct MultitoolCli {
    // fields unchanged
}
```

Replace public help text in this file from `Codex` to `WinkAgent`, including examples that currently say `codex login`.

- [ ] **Step 4: Update Rust test binary lookups**

Run:

```powershell
$files = rg -l 'cargo_bin\("codex"\)' codex-rs
foreach ($file in $files) {
  $text = [System.IO.File]::ReadAllText((Join-Path (Get-Location) $file))
  $text = $text.Replace('cargo_bin("codex")', 'cargo_bin("winkagent")')
  [System.IO.File]::WriteAllText((Join-Path (Get-Location) $file), $text)
}
```

Update package tests so the primary entrypoint is `bin/winkagent` and the package manifest is `winkagent-package.json`. Keep `codex-path`, `codex-resources`, `codex-code-mode-host`, `codex-command-runner`, and `codex-windows-sandbox-setup` unchanged.

- [ ] **Step 5: Run the branding test and verify GREEN**

Run: `cargo test -p winkagent-cli winkagent_branding_is_public -- --exact`
Expected: PASS.

- [ ] **Step 6: Build and inspect the public CLI**

Run: `cargo build -p winkagent-cli --bin winkagent`
Expected: PASS and produce `winkagent[.exe]`.

Run: `cargo run -p winkagent-cli --bin winkagent -- --help`
Expected: usage starts with `winkagent` and about text contains `WinkAgent`.

- [ ] **Step 7: Commit Task 2**

```powershell
git add codex-rs/cli
git -c user.name="WinkAgent" -c user.email="winkagent@localhost" commit -m "feat: rename primary CLI to winkagent"
```

---

### Task 3: Replace User-Facing TUI, CLI, Doctor, and README Branding

**Files:**
- Modify: `codex-rs/tui/src/history_cell/session.rs`
- Modify: `codex-rs/tui/src/onboarding/welcome.rs`
- Modify: `codex-rs/cli/src/doctor/output.rs`
- Modify: `codex-rs/cli/src/main.rs`
- Modify: `README.md`
- Modify: all snapshots containing `OpenAI Codex`

**Interfaces:**
- Consumes: `winkagent` command from Tasks 1 and 2.
- Produces: display brand `WinkAgent` on all primary user-visible surfaces.

- [ ] **Step 1: Add a failing welcome-brand test**

In `codex-rs/tui/src/onboarding/welcome.rs`, inside `welcome_renders_animation_on_first_draw`, add:

```rust
assert!(
    row_containing(&buf, "WinkAgent").is_some(),
    "welcome screen should display the WinkAgent brand"
);
```

- [ ] **Step 2: Verify RED**

Run: `cargo test -p codex-tui welcome_renders_animation_on_first_draw -- --exact`
Expected: FAIL because the rendered text still contains `Codex`.

- [ ] **Step 3: Update production branding strings**

Change `codex-rs/tui/src/history_cell/session.rs`:

```rust
">_ ".fg(accent_color()),
"WinkAgent".bold(),
format!(" (v{version})").dim(),
```

and:

```rust
Line::from(format!("WinkAgent (v{})", self.version)),
```

Change `codex-rs/tui/src/onboarding/welcome.rs`:

```rust
lines.push(Line::from(vec![
    "  ".into(),
    "Welcome to ".into(),
    "WinkAgent".bold(),
    ", a command-line coding agent".into(),
]));
```

Change `codex-rs/cli/src/doctor/output.rs` public title:

```rust
bold("WinkAgent Doctor", options),
```

Replace remaining public `Codex` labels in `codex-rs/cli/src/main.rs` and doctor output with `WinkAgent`.

- [ ] **Step 4: Update snapshots mechanically**

Run:

```powershell
$files = rg -l 'OpenAI Codex' codex-rs/tui
foreach ($file in $files) {
  $path = Join-Path (Get-Location) $file
  $text = [System.IO.File]::ReadAllText($path)
  $text = $text.Replace('OpenAI Codex', 'WinkAgent')
  [System.IO.File]::WriteAllText($path, $text)
}

$files = rg -l "Welcome to Codex, OpenAI's command-line coding agent" codex-rs/tui
foreach ($file in $files) {
  $path = Join-Path (Get-Location) $file
  $text = [System.IO.File]::ReadAllText($path)
  $text = $text.Replace(
    "Welcome to Codex, OpenAI's command-line coding agent",
    "Welcome to WinkAgent, a command-line coding agent"
  )
  [System.IO.File]::WriteAllText($path, $text)
}
```

- [ ] **Step 5: Update README install and product text**

Replace the title and installation instructions:

```markdown
<p align="center"><strong>WinkAgent</strong> is a coding agent that runs locally on your computer.</p>

### Installing and running WinkAgent

Run the following on Mac or Linux to install WinkAgent:

curl -fsSL https://raw.githubusercontent.com/openai/codex/main/scripts/install/install.sh | sh

Run the following on Windows to install WinkAgent:

irm https://raw.githubusercontent.com/openai/codex/main/scripts/install/install.ps1 | iex

WinkAgent can also be installed via the following package managers:

npm install -g winkagent
```

Change public `codex` command examples to `winkagent` and public `Codex` brand labels to `WinkAgent`. Keep upstream documentation URLs and OpenAI service references unchanged.

- [ ] **Step 6: Verify TUI and doctor tests**

Run: `cargo test -p codex-tui welcome_renders_animation_on_first_draw -- --exact`
Expected: PASS.

Run: `cargo test -p codex-tui session_header -- --nocapture`
Expected: PASS after snapshots contain `WinkAgent`.

Run: `cargo test -p winkagent-cli doctor --lib -- --nocapture`
Expected: PASS after doctor snapshots are updated.

- [ ] **Step 7: Commit Task 3**

```powershell
git add README.md codex-rs/tui codex-rs/cli/src
git -c user.name="WinkAgent" -c user.email="winkagent@localhost" commit -m "feat: apply WinkAgent product branding"
```

---

### Task 4: Update Public Release and Installation Metadata

**Files:**
- Modify: `scripts/codex_package/targets.py`
- Modify: `scripts/codex_package/layout.py`
- Modify: `scripts/codex_package/cli.py`
- Modify: `scripts/codex_package/cargo.py`
- Modify: `scripts/stage_npm_packages.py`
- Modify: `scripts/install/install.sh`
- Modify: `scripts/install/install.ps1`
- Modify: `.github/scripts/build-codex-package-archive.sh`
- Modify: `.github/actions/build-codex-packages/action.yml`
- Modify: `.github/dotslash-config.json`
- Modify: release tests referencing `codex-package` or primary `codex`

**Interfaces:**
- Consumes: `winkagent` binary and npm names from Tasks 1 and 2.
- Produces: `winkagent-package-*`, `winkagent-package.json`, and installer paths that select `bin/winkagent`.

- [ ] **Step 1: Add a failing packaging assertion**

Extend `codex-cli/tests/test_rebrand.py`:

```python
def test_release_variant_uses_winkagent(self) -> None:
    targets = (
        Path(__file__).resolve().parents[2]
        / "scripts"
        / "codex_package"
        / "targets.py"
    ).read_text(encoding="utf-8")
    self.assertIn('"winkagent": PackageVariant(', targets)
    self.assertIn('cargo_bin="winkagent"', targets)
    self.assertIn('executable_stem="winkagent"', targets)
```

- [ ] **Step 2: Verify RED**

Run: `python codex-cli/tests/test_rebrand.py`
Expected: FAIL because the variant is still named `codex`.

- [ ] **Step 3: Update package variant and manifest paths**

In `scripts/codex_package/targets.py`:

```python
PACKAGE_VARIANTS = {
    "winkagent": PackageVariant(
        name="winkagent",
        cargo_bin="winkagent",
        executable_stem="winkagent",
    ),
}
```

In `scripts/codex_package/layout.py`, use `winkagent-package.json` as the manifest file. Keep `codex-resources`, `codex-path`, and helper names unchanged.

In `scripts/codex_package/cli.py`, change the default package to `winkagent` and user-facing descriptions to WinkAgent.

In `scripts/codex_package/cargo.py`, build the `winkagent` primary binary when `build_entrypoint` is true.

In `scripts/stage_npm_packages.py`, rename archive lookup and tarball naming:

```python
archive_path = artifact_subdir / f"winkagent-package-{target}.tar.gz"
return f"winkagent-npm-{platform}-{version}.tgz"
```

- [ ] **Step 4: Update installers and release workflows**

Mechanically replace public package-artifact names:

```powershell
$roots = @('scripts/install', '.github', 'scripts/codex_package', 'scripts/stage_npm_packages.py')
$files = rg -l 'codex-package' @roots
foreach ($file in $files) {
  $path = Join-Path (Get-Location) $file
  $text = [System.IO.File]::ReadAllText($path)
  $text = $text.Replace('codex-package', 'winkagent-package')
  [System.IO.File]::WriteAllText($path, $text)
}
```

Then change primary entrypoint references:

- `bin/codex` becomes `bin/winkagent`
- `bin/codex.exe` becomes `bin/winkagent.exe`
- installed visible command `codex` becomes `winkagent`
- generated completion/package entrypoint `codex` becomes `winkagent`

Do not change `codex-code-mode-host`, `codex-command-runner`,
`codex-windows-sandbox-setup`, `CODEX_HOME`, or `CODEX_*`.

- [ ] **Step 5: Verify packaging tests**

Run: `python codex-cli/tests/test_rebrand.py`
Expected: PASS.

Run: `python -m unittest discover -s scripts/codex_package -p 'test_*.py'`
Expected: PASS.

Run: `python -m unittest discover -s scripts/install -p 'test_*.py'`
Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```powershell
git add scripts .github codex-cli/tests/test_rebrand.py
git -c user.name="WinkAgent" -c user.email="winkagent@localhost" commit -m "build: publish WinkAgent package artifacts"
```

---

### Task 5: Compatibility Audit and Final Verification

**Files:**
- Modify: `docs/superpowers/specs/2026-10-20-winkagent-rebrand-design.md` only if implementation reveals a contradiction.
- Verify: repository-wide.

**Interfaces:**
- Consumes: all prior tasks.
- Produces: documented evidence that public branding changed and compatibility identifiers did not.

- [ ] **Step 1: Verify public names**

Run:

```powershell
node --test codex-cli/tests/rebrand.test.mjs
python codex-cli/tests/test_rebrand.py
cargo test -p winkagent-cli winkagent_branding_is_public -- --exact
```

Expected: all PASS.

- [ ] **Step 2: Verify compatibility identifiers remain**

Run:

```powershell
rg -n 'CODEX_HOME' codex-cli/bin/winkagent.js codex-rs/cli/src scripts/install
rg -n 'codex-code-mode-host|codex-command-runner|codex-windows-sandbox-setup' codex-rs/cli scripts/codex_package
git diff --name-only | rg 'codex-home|protocol|app-server-protocol|CODEX_HOME'
```

Expected: environment variables and helper names are present; no protocol files are modified.

- [ ] **Step 3: Verify stale public package references are gone**

Run:

```powershell
rg -n '@openai/codex' codex-cli README.md scripts/install scripts/stage_npm_packages.py
rg -n 'bin/codex|codex-package' codex-cli scripts/install scripts/codex_package scripts/stage_npm_packages.py
```

Expected: no matches in public package/installer files, except intentionally retained helper names that also contain `codex-`.

- [ ] **Step 4: Run formatting and focused test suites**

Run: `cargo fmt --all --check`
Expected: PASS.

Run: `cargo test -p winkagent-cli --tests --no-run`
Expected: PASS.

Run: `cargo test -p codex-tui --lib onboarding::welcome::tests --no-run`
Expected: PASS.

- [ ] **Step 5: Verify CLI output**

Run: `cargo run -p winkagent-cli --bin winkagent -- --version`
Expected: output identifies WinkAgent.

Run: `cargo run -p winkagent-cli --bin winkagent -- --help`
Expected: usage begins with `winkagent` and contains `WinkAgent`.

- [ ] **Step 6: Commit final verification adjustments**

```powershell
git add -A
git -c user.name="WinkAgent" -c user.email="winkagent@localhost" commit -m "test: verify WinkAgent rebrand compatibility"
```

