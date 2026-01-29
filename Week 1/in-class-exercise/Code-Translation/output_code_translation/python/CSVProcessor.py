import os
from typing import List, Tuple


class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name: str) -> Tuple[List[str], List[List[str]]]:
        title: List[str] = []
        data: List[List[str]] = []
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                # Read header
                line = file.readline()
                if not line:
                    return title, data
                title = line.rstrip('\n').split(',')

                # Read rows
                for line in file:
                    row = line.rstrip('\n').split(',')
                    data.append(row)
        except (IOError, OSError):
            # Return empty lists on failure to open
            pass
        return title, data

    def write_csv(self, data: List[List[str]], file_name: str) -> int:
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                for row in data:
                    file.write(','.join(row) + '\n')
        except (IOError, OSError):
            return 0
        return 1

    def process_csv_data(self, N: int, save_file_name: str) -> int:
        title, data = self.read_csv(save_file_name)

        # Validate column index
        if not data or N >= len(data[0]):
            return 0

        column_data: List[str] = []
        for row in data:
            if N < len(row):
                column_data.append(row[N].upper())

        new_data = [title, column_data]

        base, _ = os.path.splitext(save_file_name)
        new_file_name = f"{base}_process.csv"
        return self.write_csv(new_data, new_file_name)
