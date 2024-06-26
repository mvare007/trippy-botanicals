import urllib
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import create_engine, inspect


@dataclass(frozen=True)
class ConnectionSettings:
    """Connection Settings."""

    server: str
    database: str
    username: str
    password: str
    driver: str = "{ODBC Driver 18 for SQL Server}"
    timeout: int = 60


class AzureDbConnection:
    """
    Azure SQL database connection.
    """

    def __init__(self, conn_settings: ConnectionSettings, echo: bool = True) -> None:
        conn_params = urllib.parse.quote_plus(
            "Driver=%s;" % conn_settings.driver
            + "Server=tcp:%s.database.windows.net,1433;" % conn_settings.server
            + "Database=%s;" % conn_settings.database
            + "Uid=%s;" % conn_settings.username
            + "Pwd=%s;" % conn_settings.password
            + "Encrypt=yes;"
            + "TrustServerCertificate=no;"
            + "Connection Timeout=%s;" % conn_settings.timeout
        )
        self.conn_string = f"mssql+pyodbc:///?odbc_connect={conn_params}"
        self.db = create_engine(self.conn_string, echo=echo)

    def connect(self) -> None:
        """Estimate connection."""
        self.conn = self.db.connect()

    def get_tables(self) -> Iterable[str]:
        """Get list of tables."""
        inspector = inspect(self.db)
        return [t for t in inspector.get_table_names()]

    def dispose(self) -> None:
        """Dispose opened connections."""
        self.conn.close()
        self.db.dispose()
