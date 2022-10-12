import api
from assets import database
from tkinter import *


instance = api.RxNorm()


root = Tk()
root.title('Digital Prescription Software')
root.geometry('600x600')


search_box = Entry(root, width=40, borderwidth=10, relief=SUNKEN)
search_box.grid(row=0, column=0)

final_name = {}

def Search_Click():
    global search_box
    global string
    

    
    string = search_box.get()
    x = instance.get_drug_list(string)
    result = x.get('drugGroup').get('conceptGroup')
    
    final_name = instance.parse_result(result)
    
    Label1 = Label(root, text='The searched medicine is : ' + str(final_name))
    Label1.grid(row=5, column=0)

    #label1 = Label(root, text = result)
    #label1.pack()

prescription_list = final_name

def Add_To_Prescription():
    global add_to_prescription

    x = instance.get_drug_list(string)
    result = x.get('drugGroup').get('conceptGroup')
    
    final_name = result[2]['conceptProperties'][0]['name']


    label2 = Label(root, text='Updated prescription list is: ' + str(final_name))
    label2.grid(row=6, column=0)



search_button = Button(root, text='Search', command=Search_Click)
search_button.config(width=40)
search_button.grid(row=2, column=0)


add_to_prescription = Button(root, text='Add to Prescription', command=Add_To_Prescription)
add_to_prescription.config(width=40)
add_to_prescription.grid(row=3, column=0)


root.mainloop()


db = database.Database()

db.connect_db()
db.create_db()

prescription = prescription_list

db.insert_data(prescription)


""""
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
"""
