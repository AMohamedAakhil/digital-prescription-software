import sqlite3


class Database:

    def __init__(self):
        self.db = None
        self.connect_db()

    def connect_db(self):
        self.create_db()
        self.db = sqlite3.connect("prescription.db")

    def create_db(self):
        open("prescription.db", "w").close()
        self.db = sqlite3.connect("prescription.db")
        self.db.execute("CREATE TABLE prescription (rxcui INTEGER, drug_name TEXT, synonym TEXT, drug_type TEXT)")
        self.db.commit()

    def insert_data(self, data: dict):
        self.db.execute("INSERT INTO prescription"
                        "(rxcui, drug_name, synonym, drug_type)"
                        "VALUES (?, ?, ?, ?)",
                        (data.get("rxcui"), data.get("name"), data.get("synonym"), data.get("type"),
                         ))
        self.db.commit()

    def retrieve_data(self):
        cursor = self.db.execute("SELECT * FROM prescription")
        return cursor.fetchall()
