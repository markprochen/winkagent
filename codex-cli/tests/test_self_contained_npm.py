import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_npm_package.py"
TARGET = "x86_64-pc-windows-msvc"


class SelfContainedNpmPackageTests(unittest.TestCase):
    def test_meta_package_can_bundle_a_native_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            vendor_src = root / "vendor-src"
            binary = vendor_src / TARGET / "bin" / "winkagent.exe"
            binary.parent.mkdir(parents=True)
            binary.write_bytes(b"native winkagent")
            package = root / "winkagent-0.0.0.tgz"

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--package",
                    "winkagent",
                    "--version",
                    "0.0.0",
                    "--staging-dir",
                    str(root / "stage"),
                    "--vendor-src",
                    str(vendor_src),
                    "--bundle-target",
                    TARGET,
                    "--pack-output",
                    str(package),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            with tarfile.open(package, "r:gz") as archive:
                manifest = json.loads(
                    archive.extractfile("package/package.json").read()
                )
                bundled = archive.extractfile(
                    f"package/vendor/{TARGET}/bin/winkagent.exe"
                ).read()

            self.assertEqual(manifest["files"], ["bin/winkagent.js", "vendor"])
            self.assertNotIn("optionalDependencies", manifest)
            self.assertEqual(bundled, b"native winkagent")
            self.assertEqual(
                manifest["repository"]["url"],
                "git+https://github.com/markprochen/winkagent.git",
            )


if __name__ == "__main__":
    unittest.main()
