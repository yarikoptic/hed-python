import unittest
from hed.errors import error_reporter
from hed.errors.error_types import ErrorContext, ErrorSeverity, ValidationErrors, SchemaWarnings


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.error_handler = error_reporter.ErrorHandler()
        pass

    def test_push_error_context(self):
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        display_filename = "DummyFileName.txt"
        self.error_handler.push_error_context(ErrorContext.FILE_NAME, display_filename)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(display_filename in error_list[0][ErrorContext.FILE_NAME])
        column_name = "DummyColumnName"
        self.error_handler.push_error_context(ErrorContext.SIDECAR_COLUMN_NAME, column_name)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(column_name in error_list[0][ErrorContext.SIDECAR_COLUMN_NAME])
        self.error_handler.reset_error_context()
        self.error_handler.push_error_context(ErrorContext.FILE_NAME, display_filename)
        self.error_handler.push_error_context(ErrorContext.SIDECAR_COLUMN_NAME, column_name)
        self.error_handler.push_error_context(ErrorContext.COLUMN, 1)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(display_filename in error_list[0][ErrorContext.FILE_NAME])
        self.assertTrue(column_name in error_list[0][ErrorContext.SIDECAR_COLUMN_NAME])
        self.assertTrue(1 in error_list[0][ErrorContext.COLUMN])
        self.assertTrue(len(error_list) == 1)
        self.error_handler.reset_error_context()

    def test_pop_error_context(self):
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        display_filename = "DummyFileName.txt"
        self.error_handler.push_error_context(ErrorContext.FILE_NAME, display_filename)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        self.assertTrue(display_filename in error_list[0][ErrorContext.FILE_NAME])
        self.error_handler.pop_error_context()
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        column_name = "DummyColumnName"
        self.error_handler.push_error_context(ErrorContext.SIDECAR_COLUMN_NAME, column_name)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        self.error_handler.push_error_context(ErrorContext.FILE_NAME, display_filename)
        self.error_handler.push_error_context(ErrorContext.SIDECAR_COLUMN_NAME, column_name)
        self.error_handler.push_error_context(ErrorContext.COLUMN, 1)
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        self.assertTrue(display_filename in error_list[0][ErrorContext.FILE_NAME])
        self.assertTrue(column_name in error_list[0][ErrorContext.SIDECAR_COLUMN_NAME])
        self.assertTrue(1 in error_list[0][ErrorContext.COLUMN])
        self.error_handler.pop_error_context()
        self.error_handler.pop_error_context()
        self.error_handler.pop_error_context()
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        self.assertTrue(ErrorContext.COLUMN not in error_list[0])
        self.error_handler.pop_error_context()
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        self.assertTrue(len(error_list) == 1)
        self.error_handler.reset_error_context()

    def test_filter_issues_by_severity(self):
        error_list = self.error_handler.format_error(ValidationErrors.MULTIPLE_UNIQUE, "")
        error_list += self.error_handler.format_error(SchemaWarnings.INVALID_CAPITALIZATION, "dummy", problem_char="#", char_index=0)
        self.assertTrue(len(error_list) == 2)
        filtered_list = self.error_handler.filter_issues_by_severity(issues_list=error_list, severity=ErrorSeverity.ERROR)
        self.assertTrue(len(filtered_list) == 1)
