#!/usr/bin/env python3
"""Filtered Logger"""
from typing import List
import re
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter Datum function"""
    extract = r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator)
    return re.sub(extract, r'\g<field>={}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Get Logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Create a database connection"""
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(host=host, port=3306, user=db_user,
                                   password=pwd, database=db_name)
    return conn


def main():
    "Main function"
    columns = [*PII_FIELDS, "ip", "last_login", "user_agent"]
    logger = get_logger()
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        for row in cursor:
            msg = msg = '; '.join('{}={}'.format(col, val)
                                  for col, val in zip(columns, row))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


if __name__ == "__main__":
    """Call the main function"""
    main()
