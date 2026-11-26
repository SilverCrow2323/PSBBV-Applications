import copy
import unittest
from pathlib import Path
from validate_package import ROOT, load, validate_package

class PackageManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load(ROOT / "schemas/application-package.schema.json")
        cls.example = load(ROOT / "application-package.example.json")

    def test_example_is_valid(self):
        self.assertEqual(validate_package(self.example, self.schema), [])

    def test_path_traversal_is_rejected(self):
        item = copy.deepcopy(self.example)
        item["files"][0]["path"] = "app/../../ur0/tai/config.txt"
        self.assertTrue(validate_package(item, self.schema))

    def test_absolute_and_windows_paths_are_rejected(self):
        for path in ("/ur0/tai/config.txt", "app\\evil.vpk", "C:/payload"):
            item = copy.deepcopy(self.example)
            item["files"][0]["path"] = path
            self.assertTrue(validate_package(item, self.schema), path)

    def test_duplicate_paths_are_rejected(self):
        item = copy.deepcopy(self.example)
        item["files"][1]["path"] = item["files"][0]["path"]
        self.assertTrue(validate_package(item, self.schema))

    def test_file_size_cannot_exceed_package_size(self):
        item = copy.deepcopy(self.example)
        item["files"][0]["sizeBytes"] = item["sizeBytes"] + 1
        self.assertTrue(validate_package(item, self.schema))

    def test_non_https_source_is_rejected(self):
        item = copy.deepcopy(self.example)
        item["source"] = "http://example.org/file.vpk"
        self.assertTrue(validate_package(item, self.schema))

if __name__ == "__main__":
    unittest.main()
