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

    def get_drug_list(self, name):
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
                    
                    dict = {'rxcui' : rxcui, 'name' : name, 'synonym' : synonym, 'type' : type}
                    return dict

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
        dosage = input("Enter dosage (Morn,Afn,Eve,Ngt): ")
        duration = input("Enter duration (in days): ")
        route = input("Enter administration route: ")
        frequency = input("Enter frequency: ")
        additional_info = input("Enter additional info (enter to skip): ")
        return {
            "dosage": dosage,
            "duration": duration,
            "route": route,
            "frequency": frequency,
            "additional_info": additional_info if additional_info else "None"
        }

    def merge_data(self, drug: dict, other_info: dict):
        final_dict = {
            "rxcui": drug.get("rxcui"),
            "name": drug.get("name"),
            "synonym": drug.get("synonym", "None"),
            "type": drug.get("type"),
            "dosage": other_info.get("dosage"),
            "duration": other_info.get("duration"),
            "route": other_info.get("route"),
            "frequency": other_info.get("frequency"),
            "additional_info": other_info.get("additional_info")
        }
        return final_dict

    def pretty_print(self, data):
        print("{:<7} | {:<25} | {:<15} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10}".format(
            'RXCUI', 'Name', 'Type', 'Synonym', 'Dosage', 'Frequency', 'Duration', 'Route', 'Instructions'))
        for entry in data:
            rxcui, name, type, synonym, dosage, frequency, duration, route, additional_info = entry
            print("{:<7} | {:<25} | {:<15} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10}".format(
                str(rxcui), name[:25], type[:15], synonym[:10], dosage[:10], frequency[:10], duration[:10], route[:10], additional_info[:10]))
