import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));
const packageJsonUrl = new URL("package.json", new URL("..", import.meta.url));
const packageJson = JSON.parse(readFileSync(packageJsonUrl, "utf8"));

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
  assert.equal(path.basename(packageRoot), "codex-cli");
});
