import psycopg
import pytest

from src.persistence.database import get_connection


@pytest.fixture
def database_connection() -> psycopg.Connection:
    with get_connection() as connection:

        yield connection

        connection.rollback()