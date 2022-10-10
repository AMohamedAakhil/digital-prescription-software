import json

import api

instance = api.RxNorm()

count = 1
continue_loop = True


def confirm_continue():
    global continue_loop
    if input("Enter more? (y/n)").lower().strip() == "n":
        continue_loop = False


while continue_loop:
    print("Drug Count", count)
    count += 1
    drug_details = instance.get_required_drug()
    if not drug_details:
        confirm_continue()
        break

    other_info = instance.get_other_info()
    # todo: enter this in a database or a json object?

instance.parse_result(drug_details)
