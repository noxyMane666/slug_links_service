import os


class Configuration:
    def __init__(self):
        self.db_connection_string = os.getenv("DB_CONNECTION_STRING")