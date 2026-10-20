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

    def test_rust_cli_uses_winkagent(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        cargo_manifest = (repo_root / "codex-rs" / "cli" / "Cargo.toml").read_text(
            encoding="utf-8"
        )
        main_source = (repo_root / "codex-rs" / "cli" / "src" / "main.rs").read_text(
            encoding="utf-8"
        )
        self.assertIn('name = "winkagent-cli"', cargo_manifest)
        self.assertIn('default-run = "winkagent"', cargo_manifest)
        self.assertIn('name = "winkagent"', cargo_manifest)
        self.assertIn('bin_name = "winkagent"', main_source)
        self.assertIn("/// WinkAgent CLI", main_source)

    def test_tui_uses_winkagent_brand(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        session_source = (
            repo_root / "codex-rs" / "tui" / "src" / "history_cell" / "session.rs"
        ).read_text(encoding="utf-8")
        welcome_source = (
            repo_root / "codex-rs" / "tui" / "src" / "onboarding" / "welcome.rs"
        ).read_text(encoding="utf-8")
        self.assertIn('"WinkAgent".bold()', session_source)
        self.assertIn('"WinkAgent".bold()', welcome_source)
        self.assertIn('"Welcome to ".into()', welcome_source)

    def test_release_variant_uses_winkagent(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        targets = (
            repo_root / "scripts" / "codex_package" / "targets.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"winkagent": PackageVariant(', targets)
        self.assertIn('cargo_bin="winkagent"', targets)
        self.assertIn('executable_stem="winkagent"', targets)


if __name__ == "__main__":
    unittest.main()
