import psycopg2
import config

conn = psycopg2.connect(
    host=config.HOST,
    database=config.DATABASE,
    user=config.USER,
    password=config.PASSWORD)

conn.autocommit = True
cur = conn.cursor()