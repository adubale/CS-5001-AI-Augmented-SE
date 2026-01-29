import sqlite3
from typing import List, Dict


class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def open_database(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.database_name)
            return conn
        except sqlite3.Error:
            raise RuntimeError("Failed to open database")

    def create_table(self, table_name: str, key1: str, key2: str) -> None:
        conn = self.open_database()
        try:
            create_table_query = (
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"(id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
            )
            conn.execute(create_table_query)
            conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to create table: {e}")
        finally:
            conn.close()

    def insert_into_database(
        self,
        table_name: str,
        data: List[Dict[str, str]],
    ) -> None:
        conn = self.open_database()
        try:
            insert_query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
            stmt = conn.cursor()
            for item in data:
                try:
                    name = item["name"]
                    age = int(item["age"])
                except KeyError as e:
                    raise RuntimeError(f"Missing required field: {e}")
                except ValueError:
                    raise RuntimeError("Invalid integer value for age")
                try:
                    stmt.execute(insert_query, (name, age))
                except sqlite3.Error as e:
                    raise RuntimeError(f"Failed to execute statement: {e}")
            conn.commit()
        finally:
            stmt.close()
            conn.close()

    def search_database(self, table_name: str, name: str) -> List[List[str]]:
        result: List[List[str]] = []
        try:
            conn = sqlite3.connect(self.database_name)
        except sqlite3.Error:
            return result

        try:
            query = f"SELECT * FROM {table_name} WHERE name = ?"
            stmt = conn.cursor()
            stmt.execute(query, (name,))
            rows = stmt.fetchall()
            for row in rows:
                str_row = [str(col) if col is not None else "" for col in row]
                result.append(str_row)
        finally:
            stmt.close()
            conn.close()
        return result

    def delete_from_database(self, table_name: str, name: str) -> None:
        conn = self.open_database()
        try:
            delete_query = f"DELETE FROM {table_name} WHERE name = ?"
            stmt = conn.cursor()
            try:
                stmt.execute(delete_query, (name,))
            except sqlite3.Error as e:
                raise RuntimeError(f"Failed to execute statement: {e}")
            conn.commit()
        finally:
            stmt.close()
            conn.close()
