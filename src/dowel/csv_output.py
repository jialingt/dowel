"""A `dowel.logger.LogOutput` for CSV files."""
import csv
import warnings

from dowel import TabularInput
from dowel.simple_outputs import FileOutput
from dowel.utils import colorize


class CsvOutput(FileOutput):
    """CSV file output for logger.

    :param file_name: The file this output should log to.
    """

    def __init__(self, file_name):
        super().__init__(file_name)
        self._writer = None
        self._fieldnames = None
        self._warned_once = set()
        self._disable_warnings = False
        # Store the name of file_name, preparing to reread the stored data from this file
        self._filename = file_name

    @property
    def types_accepted(self):
        """Accept TabularInput objects only."""
        return (TabularInput, )

    def record(self, data, prefix=''):
        """Log tabular data to CSV."""
        if isinstance(data, TabularInput):
            to_csv = data.as_primitive_dict

            if not to_csv.keys() and not self._writer:
                return

            if not self._writer:
                self._fieldnames = set(to_csv.keys())
                # self._longestHeader = self._fieldnames
                self._writer = csv.DictWriter(
                    self._log_file,
                    fieldnames=self._fieldnames,
                    extrasaction='ignore')
                self._writer.writeheader()

            # If the current keys are not inconsistent with the original keys
            if to_csv.keys() != self._fieldnames:

                with open(self._filename, "r") as old:
                    # Read the data from current file which contain all information stored previously
                    old_data = csv.DictReader(old)

                    # Update the header with new keys
                    # For example: old iteration key: 1,2,3 new iteration key: 4
                    # The longestHeader will be updated as: 1,2,3,4
                    self._fieldnames = set(self._fieldnames)|set(to_csv.keys())

                    # Change the writer contains the new keys
                    self._writer.fieldnames = self._fieldnames

                    # Seek(0) means write from the start of the file
                    self._log_file.seek(0)
                    self._writer.writeheader()

                    # Writerow function will map dictionaries onto output rows
                    # Rewrite the old_data into the file
                    for i in old_data:
                        self._writer.writerow(i)
                        
            self._writer.writerow(to_csv)

            for k in to_csv.keys():
                data.mark(k)
        else:
            raise ValueError('Unacceptable type.')

    def _warn(self, msg):
        """Warns the user using warnings.warn.

        The stacklevel parameter needs to be 3 to ensure the call to logger.log
        is the one printed.
        """
        if not self._disable_warnings and msg not in self._warned_once:
            warnings.warn(
                colorize(msg, 'yellow'), CsvOutputWarning, stacklevel=3)
        self._warned_once.add(msg)
        return msg

    def disable_warnings(self):
        """Disable logger warnings for testing."""
        self._disable_warnings = True


class CsvOutputWarning(UserWarning):
    """Warning class for CsvOutput."""

    pass
