from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2 as ps
from psycopg2 import sql
import logging

class DataBase:
    def __init__(self, host, user, password, dbname):
        self.conn = ps.connect(
            host = host,
            password = password,
            user= user,
            dbname =dbname
        )
        self.conn.set_isolation_level(ps.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


    def push_content(self, link, ):
