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
