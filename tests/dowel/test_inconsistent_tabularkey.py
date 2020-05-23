import csv
import tempfile
import pytest
from dowel import CsvOutput, TabularInput
from dowel.csv_output import CsvOutputWarning


class TestInconsistent:

    def setup_method(self):
        self.log_file = tempfile.NamedTemporaryFile()
        self.csv_output = CsvOutput(self.log_file.name)
        self.tabular = TabularInput()
        self.tabular.clear()

    def teardown_method(self):
        self.log_file.close()

    def assert_csv_matches(self, correct):
        """Check the first row of a csv file and compare it to known values."""
        with open(self.log_file.name, 'r') as file:
            reader = csv.DictReader(file)

            for correct_row in correct:
                row = next(reader)
                assert row == correct_row

    def test_add_newkey(self):
        foo = 1
        bar = 10
        self.tabular.record('foo', foo)
        self.csv_output.record(self.tabular)

        self.tabular.record('foo', foo * 2)
        self.tabular.record('bar', bar * 2)
        self.csv_output.record(self.tabular)

        self.csv_output.dump()

        correct = [
            {'foo': str(foo), 'bar': ''},
            {'foo': str(foo * 2), 'bar': str(bar * 2)},
        ]  # yapf: disable
        self.assert_csv_matches(correct)

    def test_reduce_oldkey(self):
        foo = 1
        bar = 10
        self.tabular.record('foo', foo)
        self.tabular.record('bar', bar * 2)
        self.csv_output.record(self.tabular)
        self.tabular.record('foo', foo * 2)
        self.tabular.delete('bar')

        # this should not produce a warning, because we only warn once
        self.csv_output.record(self.tabular)

        self.csv_output.dump()

        correct = [
            {'foo': str(foo), 'bar': str(bar * 2)},
            {'foo': str(foo * 2), 'bar': ''},
        ]  # yapf: disable
        self.assert_csv_matches(correct)

    def test_add_newkey_reduce_oldkey(self):
        foo = 1
        bar = 10
        new = 5
        self.tabular.record('foo', foo)
        self.tabular.record('bar', bar)
        self.csv_output.record(self.tabular)

        self.tabular.record('foo', foo * 2)
        self.tabular.record('new_key', new)
        self.tabular.delete('bar')
        self.csv_output.record(self.tabular)

        self.csv_output.dump()

        correct = [
            {'foo': str(foo), 'bar': str(bar), 'new_key': ''},
            {'foo': str(foo * 2), 'bar': '', 'new_key': str(new)},
        ]  # yapf: disable
        self.assert_csv_matches(correct)