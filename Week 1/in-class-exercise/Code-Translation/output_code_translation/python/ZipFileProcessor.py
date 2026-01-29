import os
import sys
import zipfile
import shutil
from dataclasses import dataclass
from typing import List


@dataclass
class ZipFileInfo:
    filename: str
    mode: str


class ZipFileProcessor:
    def __init__(self, zip_file_path: str):
        self.zip_file_path_ = zip_file_path

    def read_zip_file(self) -> ZipFileInfo:
        archive = self._open_zip_file('r')
        info = ZipFileInfo(filename=self.zip_file_path_, mode='r')
        if archive:
            archive.close()
        return info

    def extract_all(self, output_directory: str) -> bool:
        if not output_directory:
            return False
        if not self._create_directory_if_not_exists(output_directory):
            return False

        archive = self._open_zip_file('r')
        if not archive:
            return False

        success = True
        for zip_info in archive.infolist():
            output_path = os.path.join(output_directory, zip_info.filename)
            if not self._extract_file_from_zip(archive, zip_info.filename, output_path):
                success = False

        archive.close()
        return success

    def extract_file(self, file_name: str, output_directory: str) -> bool:
        if not output_directory:
            return False
        if not self._create_directory_if_not_exists(output_directory):
            print(f"Failed to create output directory: {output_directory}", file=sys.stderr)
            return False

        archive = self._open_zip_file('r')
        if not archive:
            return False

        try:
            zip_info = archive.getinfo(file_name)
        except KeyError:
            print(f"File not found in zip: {file_name}", file=sys.stderr)
            archive.close()
            return False

        output_path = os.path.join(output_directory, file_name)
        success = self._extract_file_from_zip(archive, zip_info.filename, output_path)

        archive.close()
        return success

    def create_zip_file(self, files: List[str], output_zip_file: str) -> bool:
        try:
            with zipfile.ZipFile(output_zip_file, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
                for file_path in files:
                    if not os.path.isfile(file_path):
                        print(f"Error: file does not exist: {file_path}", file=sys.stderr)
                        return False
                    try:
                        archive.write(file_path, arcname=file_path)
                    except Exception as e:
                        print(f"Error adding file to zip: {file_path}", file=sys.stderr)
                        return False
        except Exception as e:
            print(f"Error opening zip file: {output_zip_file}", file=sys.stderr)
            return False
        return True

    # ----- private helpers -----
    def _extract_file_from_zip(self, archive: zipfile.ZipFile, member_name: str, output_file_path: str) -> bool:
        try:
            with archive.open(member_name, 'r') as src, open(output_file_path, 'wb') as dst:
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                shutil.copyfileobj(src, dst, length=4096)
        except Exception as e:
            print(f"Failed to extract {member_name} to {output_file_path}: {e}", file=sys.stderr)
            return False
        return True

    def _create_directory_if_not_exists(self, dir_path: str) -> bool:
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create directory {dir_path}: {e}", file=sys.stderr)
            return False

    def _open_zip_file(self, mode: str) -> zipfile.ZipFile | None:
        try:
            return zipfile.ZipFile(self.zip_file_path_, mode=mode)
        except Exception as e:
            print(f"Failed to open zip file: {self.zip_file_path_}", file=sys.stderr)
            return None
