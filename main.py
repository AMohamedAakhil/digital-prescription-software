import api
from assets import database

instance = api.RxNorm()
db = database.Database()

count = 1
continue_loop = True


def confirm_continue():
    global continue_loop
    if input("Enter more? (y/n): ").lower().strip() == "n":
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
    final_dict = instance.merge_data(drug_details, other_info)
    db.insert_data(final_dict)
    confirm_continue()

print("\nFinal Data\n")
final_data = db.retrieve_data()
instance.pretty_print(final_data)
