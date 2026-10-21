# npm releases

Use the staging helper in the repo root to generate npm tarballs for a release. For
example, to stage the CLI, responses proxy, and SDK packages for version `0.6.0`:

```bash
./scripts/stage_npm_packages.py \
  --release-version 0.6.0 \
  --package winkagent \
  --package codex-responses-api-proxy \
  --package codex-sdk
```

This downloads the required native package archive artifacts, hydrates `vendor/` for
each package, and writes tarballs to `dist/npm/`.

When `--package winkagent` is provided, the staging helper builds the lightweight
`winkagent` meta package plus all platform-native `winkagent-*` variants
that are later published under platform-specific dist-tags.

Direct `build_npm_package.py` invocations are still useful for package-specific
debugging, but native packages expect `--vendor-src` to point at a prehydrated
`vendor/` tree. Release packaging should use `scripts/stage_npm_packages.py`

For a self-contained local Windows package, point `--vendor-src` at a directory
containing `x86_64-pc-windows-msvc/` and add
`--bundle-target x86_64-pc-windows-msvc`. This bundles the native package under
`vendor/` and removes the unpublished platform optional dependencies.
