import sqlite3
from pathlib import Path

class vlrDBtemplate():
    def __init__(self, dbFile:Path):
        self.dbFile = dbFile
        self.init_tables()

    def runQuery(self, query:str):
        try:
            with sqlite3.connect(self.dbFile) as conn:
                cursor = conn.cursor()

                if type(query) is list and type(query[0]) is str:
                    for statement in query:
                        cursor.execute(statement)
                elif type(query) is str:
                    cursor.execute(query)
                else:
                    raise Exception("query must be a string or list of strings")
                
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Failed to execute query:", e)
        
    

    def init_tables(self):
        sql_statements = [
            """
            CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT,
            url TEXT,
            logo TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT,
            url TEXT,
            teamTag TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT,
            prizepool TEXT,
            dates TEXT,
            country TEXT,
            image TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            team1 TEXT,
            team2 TEXT,
            status TEXT,
            event TEXT,
            tournament TEXT,
            image TEXT,
            date INTEGER
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            teams TEXT,
            score TEXT,
            winner TEXT,
            status TEXT,
            event TEXT,
            image TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS metadata (
            lastupdate TEXT
            );
            """
        ]
        self.runQuery(sql_statements)

if __name__ == "__main__":
    dbLocation = Path("data/vlr.db")
    vlrDB = vlrDBtemplate(dbLocation)

        
