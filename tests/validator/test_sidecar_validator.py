import unittest
import os
import io
import shutil

from hed.errors import HedFileError, ValidationErrors
from hed.models import ColumnMetadata, HedString, Sidecar
from hed.validator import HedValidator
from hed import schema
from hed.models import DefinitionDict
from hed.errors import ErrorHandler
from hed.validator.sidecar_validator import SidecarValidator


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/')
        cls.base_data_dir = base_data_dir
        hed_xml_file = os.path.join(base_data_dir, "schema_tests/HED8.0.0t.xml")
        cls.hed_schema = schema.load_schema(hed_xml_file)
        cls._refs_json_filename = os.path.join(base_data_dir, "sidecar_tests/basic_refs_test.json")
        cls._bad_refs_json_filename = os.path.join(base_data_dir, "sidecar_tests/bad_refs_test2.json")
        cls._malformed_refs_json_filename = os.path.join(base_data_dir, "sidecar_tests/malformed_refs_test.json")

    def test_basic_refs(self):
        sidecar = Sidecar(self._refs_json_filename)
        issues = sidecar.validate(self.hed_schema)

        self.assertEqual(len(issues), 0)
        refs = sidecar.get_column_refs()
        self.assertEqual(len(refs), 2)

    def test_bad_refs(self):
        sidecar = Sidecar(self._bad_refs_json_filename)
        issues = sidecar.validate(self.hed_schema)

        self.assertEqual(len(issues), 2)

    def test_malformed_refs(self):
        sidecar = Sidecar(self._malformed_refs_json_filename)
        issues = sidecar.validate(self.hed_schema)

        self.assertEqual(len(issues), 4)

    def test_malformed_braces(self):
        hed_strings = [
            "column2}, Event, Action",
             "{column, Event, Action",
             "This is a {malformed {input string}} with extra {opening brackets",
             "{Event{Action}}",
             "Event, Action}"
        ]
        error_counts = [
            1,
            1,
            3,
            2,
            1
        ]

        for string, error_count in zip(hed_strings, error_counts):
            issues = SidecarValidator._find_non_matching_braces(string)

            self.assertEqual(len(issues), error_count)

