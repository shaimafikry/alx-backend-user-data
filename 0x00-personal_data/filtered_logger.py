import re
import logging
import os
import mysql.connector
from mysql.connector import MySQLConnection
from typing import List, Tuple

# Sensitive fields to redact from logs
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class that filters sensitive information from log messages.
    """
    REDACTION: str = "***"
    FORMAT: str = ("name={name}; email={email}; phone={phone}; ssn={ssn}; "
                   "password={password}; ip={ip}; last_login={last_login}; user_agent={user_agent};")
    SEPARATOR: str = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Overridden format method to redact PII fields from the log message.
        """
        message = super(RedactingFormatter, self).format(record)
        return self.filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

    @staticmethod
    def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
        """
        Redacts sensitive information in a log message.

        Args:
        - fields: List of fields to redact.
        - redaction: The string to replace sensitive information with.
        - message: The original log message.
        - separator: Separator used between fields in the message.

        Returns:
        - The message with sensitive fields redacted.
        """
        for field in fields:
            message = re.sub(f"{field}=[^;]+", f"{field}={redaction}", message)
        return message


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger named 'user_data' with a stream handler 
    and a RedactingFormatter that filters sensitive fields.

    Returns:
    - A configured logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """
    Connects to the MySQL database using credentials from environment variables.

    Returns:
    - A MySQLConnection object to interact with the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the database
    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection


def main() -> None:
    """
    Main function to retrieve user data from the database and log each row
    with filtered PII fields.
    """
    db = get_db()
    cursor = db.cursor()

    # Retrieve data from the 'users' table
    cursor.execute(
        "SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;"
    )

    logger = get_logger()

    # Log each row with filtered PII
    for row in cursor.fetchall():
        log_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        )
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
