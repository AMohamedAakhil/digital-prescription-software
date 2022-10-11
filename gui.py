from tkinter import *
import api



instance = api.RxNorm()

root = Tk()
root.title('Digital Prescription Software')
root.geometry('600x600')


search_box = Entry(root, width=40, borderwidth=10, relief=SUNKEN)
search_box.grid(row=0, column=0)


def Search_Click():
    global search_box
    global string
    string = search_box.get()
    x = instance.get_drug_list(string)
    result = x.get('drugGroup').get('conceptGroup')
    
    final_name = result[2]['conceptProperties'][0]['name']
    
    Label1 = Label(root, text='The searched medicine is : ' + final_name)
    Label1.grid(row=5, column=0)

    #label1 = Label(root, text = result)
    #label1.pack()

prescription_list = []

def Add_To_Prescription():
    global add_to_prescription

    x = instance.get_drug_list(string)
    result = x.get('drugGroup').get('conceptGroup')
    
    final_name = result[2]['conceptProperties'][0]['name']
    prescription_list.append(final_name)

    label2 = Label(root, text='Updated prescription list is: ' + str(prescription_list))
    label2.grid(row=6, column=0)

def get_drug_from_rxcui():

    x = instance.get_drug_list(string)
    result = x.get('drugGroup').get('conceptGroup')
    
    final_name = result[2]['conceptProperties']
    y = instance.fetch_drug_from_rxcui(final_name, str(final_name[0]))
    label3 = Label(root, text=y)
    label3.grid(row=10, column=0)


search_button = Button(root, text='Search', command=Search_Click)
search_button.config(width=40)
search_button.grid(row=2, column=0)


add_to_prescription = Button(root, text='Add to Prescription', command=Add_To_Prescription)
add_to_prescription.config(width=40)
add_to_prescription.grid(row=3, column=0)

get_drug_from_rxcui = Button(root, text = 'Search rxcui id', command = get_drug_from_rxcui)
get_drug_from_rxcui.config(width=40)
get_drug_from_rxcui.grid(row=4, column=0)


root.mainloop()
