class SQLQueryBuilder:
    @staticmethod
    def select(table: str,
               columns: list[str] = None,
               where: list[tuple[str, str]] = None) -> str:
        if columns is None:
            columns = ["*"]
        if where is None:
            where = []

        # SELECT clause
        if len(columns) == 1 and columns[0] == "*":
            query = "SELECT *"
        else:
            query = "SELECT " + ", ".join(columns)

        # FROM clause
        query += f" FROM {table}"

        # WHERE clause
        if where:
            conditions = [f"{k}='{v}'" for k, v in where]
            query += " WHERE " + " AND ".join(conditions)

        return query

    @staticmethod
    def insert(table: str,
               data: list[tuple[str, str]]) -> str:
        cols = ", ".join(col for col, _ in data)
        vals = ", ".join(f"'{val}'" for _, val in data)
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete_(table: str,
                where: list[tuple[str, str]] = None) -> str:
        if where is None:
            where = []
        query = f"DELETE FROM {table}"
        if where:
            conditions = [f"{k}='{v}'" for k, v in where]
            query += " WHERE " + " AND ".join(conditions)
        return query

    @staticmethod
    def update(table: str,
               data: list[tuple[str, str]],
               where: list[tuple[str, str]] = None) -> str:
        if where is None:
            where = []
        set_clause = ", ".join(f"{col}='{val}'" for col, val in data)
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            conditions = [f"{k}='{v}'" for k, v in where]
            query += " WHERE " + " AND ".join(conditions)
        return query
