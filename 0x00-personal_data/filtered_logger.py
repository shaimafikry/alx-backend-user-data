#!/usr/bin/env python3
"""
filter file
"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to filter PII data """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.

    Arguments:
    - fields: List of fields to obfuscate.
    - redaction: String used to replace sensitive field values.
    - message: The log line as a string.
    - separator: Character used to separate fields in the log message.

    Returns:
    Obfuscated log message.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}', f'{field}={redaction}{separator}', message)
    return message
