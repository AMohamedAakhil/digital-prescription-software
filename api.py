import json

import requests

from assets import shell_assets

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
                    print(f"RXCUI: {shell_assets.colour_yellow(rxcui)}")
                    print(f"Name: {shell_assets.colour_blue(name)}")
                    if synonym:
                        print(f"Synonym: {synonym}")
                    print(f"Type: {shell_assets.colour_cyan(type)}")
                    print()

    def fetch_drug_from_rxcui(self, concept_group: list, rxcui: str):
        for entry in concept_group:
            if entry.get("conceptProperties"):
                for property in entry.get("conceptProperties"):
                    fetched_rxcui = property.get("rxcui")
                    name = property.get("name")
                    synonym = property.get("synonym")
                    type = self.tty_dict.get(property.get("tty"), "Generic Product")
                    if fetched_rxcui == rxcui:
                        return {
                            "rxcui": fetched_rxcui,
                            "name": name,
                            "synonym": synonym,
                            "type": type
                        }
        return {}

    def get_required_drug(self):
        name = input("Enter drug name: ")
        results = self.get_drug_list(name).get("drugGroup").get("conceptGroup")
        if results:
            self.parse_result(results)
            rxcui = input("\nPaste the RXCUI of the required drug: ")
            if not rxcui.isdigit():
                print(shell_assets.colour_red("Invalid RXCUI"))
                return {}
            drug = self.fetch_drug_from_rxcui(results, rxcui)
            return drug
        else:
            print(shell_assets.colour_red("No results found"))
            return {}

    def get_other_info(self):
        dosage = input("Enter dosage (Morn,Afn,Eve,Ngt): ").split(",")
        duration = input("Enter duration (in days): ")
        route = input("Enter administration route: ")
        frequency = input("Enter frequency: ")
        additional_info = input("Enter additional info (enter to skip): ")
        return {
            "dosage": dosage,
            "duration": duration,
            "route": route,
            "frequency": frequency,
            "additional_info": additional_info
        }
