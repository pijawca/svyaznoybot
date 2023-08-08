# -*- coding: utf-8 -*-
import psycopg
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_table():
    try:
        conn = psycopg.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        with conn.cursor() as cur:
            cur.execute(
                f"""CREATE TABLE {DB_NAME} (
                    id serial,
                    discord text, 
                    nickname text PRIMARY KEY, 
                    clan text, 
                    allbattles text, 
                    allwins text, 
                    wn8 text,
                    wgr text, 
                    eff text, 
                    lvl text, 
                    dmg text)""")
            conn.commit()
            conn.close()
            cur.close()
            print(f'[DATABASE] База данных {DB_NAME} была создана.')
    except:
        pass
    