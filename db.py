# -*- coding: utf-8 -*-
import psycopg
from config import DB_NAME


def create_table():
    try:
        conn = psycopg.connect(host='localhost')
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
            