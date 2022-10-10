import json

import requests


class RxNorm:

    def __init__(self):
        self.base_url = "https://rxnav.nlm.nih.gov/REST/drugs.json?name="
        self.headers = {'Content-Type': 'application/json'}
        self.tty_dict = {
            "SCD": "Clinical Drug",
            "GPCK": "Clinical Pack",
            "SBD": "Branded Drug",
            "BPCK": "Branded Pack"
        }

    def get_drug_list(self, name: str):
        url = self.base_url + name
        response = requests.get(url, headers=self.headers)
        return response.json()

    def parse_result(self, concept_group: list):
        for entry in concept_group:
            if entry.get("conceptProperties"):
                for property in entry.get("conceptProperties"):
                    rxcui = property.get("rxcui")
                    name = property.get("name")
                    synonym = property.get("synonym")
                    type = self.tty_dict.get(property.get("tty"), "Generic Product")
                    print(f"RXCUI: {rxcui}")
                    print(f"Name: {name}")
                    print(f"Synonym: {synonym}")
                    print(f"Type: {type}")
                    print()
