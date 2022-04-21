import unittest
import os
from unittest import mock
import pandas as pd
from hed.errors import HedFileError
from hed.tools import KeyTemplate
from hed.util.data_util import get_row_hash
from hed.util import get_new_dataframe


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curation_base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data/curation')
        cls.stern_map_path = os.path.join(curation_base_dir, "sternberg_map.tsv")
        cls.stern_test1_path = os.path.join(curation_base_dir, "sternberg_test_events.tsv")
        cls.stern_test2_path = os.path.join(curation_base_dir, "sternberg_with_quotes_events.tsv")
        cls.stern_test3_path = os.path.join(curation_base_dir, "sternberg_no_quotes_events.tsv")
        cls.attention_shift_path = os.path.join(curation_base_dir,
                                                "sub-001_task-AuditoryVisualShiftHed2_run-01_events.tsv")
        cls.key_cols = ['type']
        cls.target_cols = ['event_type', 'task_role', 'letter']
        cls.count_col = ['counts']

    def test_constructor(self):
        t_map = KeyTemplate(self.key_cols)
        self.assertIsInstance(t_map, KeyTemplate)
        df = t_map.col_map
        self.assertIsInstance(df, pd.DataFrame)
        try:
            KeyTemplate([])
        except HedFileError:
            pass
        except Exception as ex:
            self.fail(f'KeyTemplate threw the wrong exception {ex} when no columns')
        else:
            self.fail('KeyTemplate should have thrown a HedFileError exception when no columns')

        emap1 = KeyTemplate(['a', 'b', 'c'], name='baloney')
        self.assertIsInstance(emap1, KeyTemplate, "KeyTemplate: multiple columns are okay")
        self.assertEqual(len(emap1.col_map.columns), 3, "The column map should have correct number of columns")

    def test_key_hash_use(self):
        t_map = KeyTemplate(['type'])
        stern_df = get_new_dataframe(self.stern_map_path)
        t_map.update(stern_df)
        t_col = t_map.col_map
        for index, row in stern_df.iterrows():
            key = get_row_hash(row, t_map.columns)
            key_value = t_map.map_dict[key]
            self.assertEqual(t_col.iloc[key_value]['type'], row['type'], "The key should be looked up for same map")

        stern_test1 = get_new_dataframe(self.stern_test1_path)
        for index, row in stern_test1.iterrows():
            key = get_row_hash(row, t_map.columns)
            key_value = t_map.map_dict[key]
            self.assertEqual(t_col.iloc[key_value]['type'], row['type'], "The key should be looked up for other file")

    def test_make_template(self):
        t_map = KeyTemplate(self.key_cols)
        stern_df = get_new_dataframe(self.stern_map_path)
        t_map.update(stern_df)
        df1 = t_map.make_template()
        self.assertIsInstance(df1, pd.DataFrame, "make_template should return a DataFrame")
        self.assertEqual(len(df1.columns), 1, "make_template should return 1 column single key, no additional columns")
        t_map2 = KeyTemplate(['event_type', 'type'])
        t_map2.update(self.stern_map_path)
        df2 = t_map2.make_template()
        self.assertIsInstance(df2, pd.DataFrame, "make_template should return a DataFrame")
        self.assertEqual(len(df2.columns), 2, "make_template should return 2 columns w 2 keys, no additional columns")
        df3 = t_map2.make_template(['bananas', 'pears', 'apples'])
        self.assertIsInstance(df3, pd.DataFrame, "make_template should return a DataFrame")
        self.assertEqual(len(df3.columns), 5, "make_template should return 5 columns w 2 keys, 3 additional columns")

    def test_make_template_key_overlap(self):
        t_map = KeyTemplate(['event_type', 'type'])
        t_map.update(self.stern_map_path)
        try:
            t_map.make_template(['Bananas', 'type', 'Pears'])
        except HedFileError:
            pass
        except Exception as ex:
            self.fail(f'make_template threw the wrong exception {ex} when additional columns overlapped keys')
        else:
            self.fail('KeyTemplate should have thrown a HedFileError exception when key overlap but threw none')

    def test_update_key(self):
        t_map = KeyTemplate(self.target_cols)
        has_duplicate = t_map.update_by_tuple(('apple', 'banana', 'pear'))
        df_map = t_map.col_map
        df_dict = t_map.map_dict
        self.assertEqual(len(df_map), 1, "update map should contain all the entries")
        self.assertEqual(len(df_map.columns), 3, "update_by_tuple should have all of the keys")
        self.assertEqual(len(df_dict.keys()), 1, "update dictionary should contain all columns")
        self.assertFalse(has_duplicate, "update should not have any duplicates for stern map")

    def test_update_map(self):
        t_map = KeyTemplate(self.key_cols)
        stern_df = get_new_dataframe(self.stern_map_path)
        t_map.update(stern_df)
        df_map = t_map.col_map
        df_dict = t_map.map_dict
        self.assertEqual(len(df_map), len(stern_df), "update map should contain all the entries")
        self.assertEqual(len(df_dict.keys()), len(stern_df),
                         "update dictionary should contain all the entries")

    def test_update_map_duplicate_keys(self):
        t_map = KeyTemplate(self.key_cols)
        stern_df = get_new_dataframe(self.stern_test2_path)
        t_map.update(stern_df)
        self.assertEqual(len(t_map.count_dict), len(t_map.map_dict),
                         "The count dictionary and key dictionary should have same number of values")

    def test__str__(self):
        t_map = KeyTemplate(self.key_cols+self.target_cols, name="Test map")
        map_str1 = str(t_map)

        self.assertTrue(map_str1, "__str__ should return a non-empty string")
        self.assertEqual(-1, map_str1.find("\n"), "__str__ should not have a new line if no contents")
        t_map.update(self.stern_map_path)
        map_str2 = str(t_map)
        self.assertTrue(map_str2, "__str__ should return a non-empty string")

    def test_update_map_missing_key(self):
        keys = self.key_cols + ['another']
        t_map = KeyTemplate(keys)
        stern_df = get_new_dataframe(self.stern_map_path)
        t_map.update(stern_df)
        self.assertEqual(len(t_map.col_map.columns), len(self.key_cols) + 1,
                         "update should have all of the columns")

    def test_update_map_not_unique(self):
        t_map = KeyTemplate(self.target_cols)
        stern_df = get_new_dataframe(self.stern_map_path)
        t_map.update(stern_df)
        self.assertEqual(len(t_map.col_map.columns), 3, "update should produce correct number of columns")
        self.assertEqual(len(t_map.col_map), len(stern_df) - 1, "update should produce the correct number of rows")
        for key, value in t_map.count_dict.items():
            self.assertGreaterEqual(value, 1, "update the counts should all be one for unique map")
        t_map.update(stern_df)
        for key, value in t_map.count_dict.items():
            self.assertGreaterEqual(value, 2, "update the counts should all be one for second update with same map")
        self.assertEqual(len(t_map.col_map.columns), 3, "update should produce correct number of columns")
        self.assertEqual(len(t_map.col_map), len(stern_df) - 1,
                         "update should produce the correct number of rows")


if __name__ == '__main__':
    unittest.main()
