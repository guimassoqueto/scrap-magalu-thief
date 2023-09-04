import psycopg
from app.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)


def upsert_query(item: dict) -> str:
    insert = f"INSERT INTO items("
    values = "VALUES("
    on_conflict = "ON CONFLICT (id)\nDO UPDATE SET "
    for key, value in item.items():
        insert += f"{key},"

        if isinstance(value, str):
            values += f"'{value}',"
            on_conflict += f"{key} = '{value}',"
        else:
            values += f"{value},"
            on_conflict += f"{key} = {value},"

    insert += "updated_at)\n"
    values += f"NOW())\n"
    on_conflict += f"updated_at = NOW();"
    return insert + values + on_conflict


class PostgresDB:
    @staticmethod
    def upsert_item(item: dict) -> None:
        conninfo = f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}"
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(upsert_query(item))
                conn.commit()


class AsyncPostgresDB:
    @staticmethod
    async def upsert_item(item: dict) -> None:
        conninfo = f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOST} port={POSTGRES_PORT}"
        async with await psycopg.AsyncConnection.connect(conninfo) as aconn:
            async with aconn.cursor() as cur:
                await cur.execute(upsert_query(item))