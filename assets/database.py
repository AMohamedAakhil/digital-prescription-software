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
        self.db.execute("CREATE TABLE prescription "
                        "(rxcui INTEGER,"
                        "drug_name TEXT, "
                        "drug_type TEXT, "
                        "synonym TEXT, "
                        "dosage TEXT, "
                        "frequency TEXT, "
                        "duration TEXT, "
                        "route TEXT, "
                        "instructions TEXT)")
        self.db.commit()

    def insert_data(self, data: dict):
        self.db.execute("INSERT INTO prescription"
                        "(rxcui, drug_name, drug_type, synonym, dosage, frequency, duration, route, instructions) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (data.get("rxcui"), data.get("name"), data.get("type"), data.get("synonym"),
                         data.get("dosage"), data.get("frequency"), data.get("duration"), data.get("route"),
                         data.get("additional_info")))
        self.db.commit()

    def retrieve_data(self):
        cursor = self.db.execute("SELECT * FROM prescription")
        return cursor.fetchall()
