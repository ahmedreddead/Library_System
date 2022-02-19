
import os
from tkinter import ttk

import numpy as np
import threading
import socket
import sys
import binascii
import tkinter as tk
import pandas as pd
from datetime import date
from functools import partial
#pip install openpyxl
d = pd.read_csv("Final_Data.csv")
NamesOfBooks = d.Name.unique()
level = d.Level.unique()
dataf =pd.DataFrame
counter = 0
con = 0
'''
ds = pd.read_csv("code.csv")
print(ds['Unnamed: 1'].dropna())
num = ds['Unnamed: 1'].unique()
print(num)
print(ds['Unnamed: 3'].dropna())
num1 = ds['Unnamed: 3'].unique()
num_namecode =list(num)
num1_code =list(num1)
num1_code.pop(0)
num_namecode.pop(0)
'''
try:
    def selected_delete ():
        global mylistglob,dataf
        for i in mylistglob.curselection():
            deleted_index = mylistglob.index(i)
            print(mylistglob.index(i))
            mylistglob.delete(i)
        dataf = dataf.drop(deleted_index)
        new_index = range(len(dataf.index))
        dataf.reset_index(drop=True, inplace=True)
        print(dataf)


    def result(name, level, head, amount, discount):
        d1 = d.copy()
        Data1 = d1[d1['Name'] == name]
        Data1 = Data1[Data1['Level'] == level]
        Data1 = Data1[Data1['head'] == head]

        Data1.index = np.arange(1, len(Data1) + 1)

        Data1 = Data1.to_dict()

        PUB = Data1["PUB"][1]

        ISPN = Data1["code"][1]

        Price = Data1["Price"][1]

        price = float(Data1["Price"][1])

        Net = price - (float(discount) * price / 100.0)

        Before_discount = int(amount) * price

        total = int(amount) * Net

        data = {'PUB': PUB,
                'ISPN ': ISPN,
                'Title ': head,
                'OTY': int(amount),
                'Price': float(price),
                'DIS': str(discount) + "%",
                'Net': Net,
                'Amount': total,
                'Before discount': Before_discount
                }

        return data
    def finalize () :
        global  dataf
        finalprice = dataf['Amount'].sum()

        dataf.loc[dataf.index[-1] + 1, 'Amount'] = "_____"
        dataf.loc[dataf.index[-1], 'Net'] = "_____"

        dataf.loc[dataf.index[-1] + 1, 'Amount'] = dataf['Before discount'].sum()
        dataf.loc[dataf.index[-1], 'Net'] = "Before Discount "

        dataf.loc[dataf.index[-1] + 1, 'Amount'] = finalprice
        dataf.loc[dataf.index[-1], 'Net'] = "After Discount "

        dataf.loc[dataf.index[-1] + 1, 'Amount'] = "_____"
        dataf.loc[dataf.index[-1], 'Net'] = "_____"

        dataf.loc[dataf.index[-1] + 1, 'Amount'] = finalprice
        dataf.loc[dataf.index[-1], 'Net'] = "Final Price "

        dataf = dataf.fillna("")

        dataf = dataf.drop("Before discount", axis="columns")

        print(dataf)
        dataf.to_excel("output.xlsx")
        exit()
    def Final_cal(disc,num,listofBooks,book_name,levelname):
        global mylistglob
        dicount = float (disc.get() )
        number = int (num.get() )
        print(dicount,number,listofBooks,book_name,levelname)
        for head in listofBooks :
            global dataf
            name = book_name
            level = levelname
            global counter
            res = result(name, level, head, number, dicount)
            if counter ==0 :
                dataf = pd.DataFrame(res, index=[counter])
                counter+=1
            else:
                dataf = dataf.append(res, ignore_index=True)

        print(dataf)
        global scrollbar1
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y,ipadx=5,ipady=5)
        scrollbar1.place(x=770, y=500, height=200, width=20)
        #mylistglob = tk.Listbox(root, yscrollcommand=scrollbar.set, bd=1, height=10)
        #for line in len (dataf ):
        #mylist.insert(tk.END, dataf['Title'].to_string())
        liscol =[]
        for col_name in dataf.columns:
            liscol.append(col_name)
        global  con
        numo =len(listofBooks)
        for i in reversed(range(numo)):
            n = dataf[[liscol[2], liscol[3], liscol[-2]]] .iloc[-1-int (i)]
            nameofs=n[liscol[2]]
            nameofs1=n[liscol[3]]
            nameofs2=n[liscol[-2]]
            mylistglob.insert(tk.END,str (nameofs )+ "   " + str (nameofs1)+ "   "+str (int (nameofs2)))
            con +=1
            mylistglob.place(x=10, y=500, height=200, width=720)
            scrollbar.config(command=mylist.yview)
        btn2 = tk.Button(root, text="delete item", fg='blue', command=partial(selected_delete), compound="right",
                         font=("arial", 15, "bold"), bd=3, bg="white")
        btn2.place(x=800, y=550)
    def add_discountplusnumbers (listofBooks,book_name,levelname):
        entry1 = ttk.Entry(root, font=('courier', 15, 'bold'))
        style = ttk.Style()
        style.configure('TEntry', foreground='blue')
        entry1.place(x=170, y=400, width=70, height=35)
        label11 = tk.Label(root, text="Discount :", bg="white",font=('courier', 15, 'bold'))
        label11.place(x=30, y=400)
        entry2 = ttk.Entry(root, font=('courier', 15, 'bold'))
        style = ttk.Style()
        style.configure('TEntry', foreground='blue')
        entry2.place(x=520, y=400, width=70, height=35)
        label11 = tk.Label(root, text="Number Of Books :", bg="white",font=('courier', 15, 'bold'))
        label11.place(x=270, y=400)
        btn4 = tk.Button(root, text="Add To Excel", fg='blue', font=("arial", 10, "bold"), bd=3, bg="white",
                         command=partial(Final_cal, entry1,entry2,listofBooks,book_name,levelname))
        btn4.place(x=600, y=400)
    def selected_book (mylist_level,book_name,levelname):
        listbox = mylist_level
        listofBooks = []
        for i in listbox.curselection():
            listofBooks.append(listbox.get(i))
        add_discountplusnumbers (listofBooks,book_name,levelname)
    def add_book(listoflevel , bookname) :
        levelname = listoflevel[0]
        book_name = bookname
        head = d[d['Name'] == book_name]
        head = head[head['Level'] == levelname]
        Data1 =head['head'].unique()
        scrollbar = tk.Scrollbar(root, bg='white')
        scrollbar.place(x=900, y=100, height=200, width=20)
        mylist_level = tk.Listbox(root, yscrollcommand=scrollbar.set, bd=1, height=10, selectmode=tk.MULTIPLE)
        for line in range(len(Data1)):
            mylist_level.insert(tk.END, Data1[line])
        mylist_level.place(x=500, y=100, height=200, width=400)
        scrollbar.config(command=mylist_level.yview)
        btn5 = tk.Button(root, text="Select Books", fg='blue', font=("arial", 10, "bold"), bd=3, bg="white",
                         command=partial(selected_book,mylist_level,book_name,levelname) )
        btn5.place(x=660, y=300)
    def selected_level (list,bookname) :
        listbox = list
        listofselection = []
        for i in listbox.curselection():
            listofselection.append(listbox.get(i))
        add_book(listofselection,bookname)
    def add_level (list) :
        book_name = list[0]
        Data1 = d[d['Name'] == book_name]
        Data1 = Data1['Level'].unique()
        scrollbar = tk.Scrollbar(root, bg='white')
        scrollbar.place(x=470, y=100, height=200, width=20)
        mylist_level = tk.Listbox(root, yscrollcommand=scrollbar.set, bd=1, height=10)
        for line in range(len(Data1)):
            mylist_level.insert(tk.END, Data1[line])
        mylist_level.place(x=400, y=100, height=200, width=70)
        scrollbar.config(command=mylist_level.yview)
        btn5 = tk.Button(root, text="Select Level ", fg='blue', font=("arial", 10, "bold"), bd=3, bg="white",
                         command=partial(selected_level,mylist_level,book_name) )
        btn5.place(x=380, y=300)
    def selected_item(mylist):
        listbox = mylist
        listofselection = []
        for i in listbox.curselection():
            listofselection.append( listbox.get(i))
        add_level(listofselection)
    listOfEnteries = []
    GatewayEntery = ''
    root = tk.Tk()
    root.title("Dar Masr ")
    canvas1 = tk.Canvas(root, width=1000, height=900)
    canvas1.configure(bg="white")
    scrollbar1 = tk.Scrollbar(root, bg='white')

    mylistglob = tk.Listbox(root, yscrollcommand=scrollbar1.set, bd=1, height=10)

    #button1 = tk.Button(text='Click Me', command=hello, bg='brown', fg='white')
    canvas1.pack()
    logowidth = canvas1.winfo_reqwidth() // 2 - 90
    #image = tk.PhotoImage(file="skarpt.gif")
    #label = tk.Label(image=image)
    #label.place(x=logowidth, y=0)
    #######################################################
    #######################################################

    style = ttk.Style()
    style.configure('TEntry', foreground='blue')
    label1 = tk.Label(root, text="Select Book Name: ", bg="white",font=('courier', 15, 'bold'))
    label1.place(x=10, y=70)


    ########################################################

    #######################################################

    photo = tk.PhotoImage(file="button.png")
    photoimage = photo.subsample(12, 12)
    #btn1 = tk.Button(root, text='Enter', image=photoimage, compound="right", bg="white", command=getSensornumber, bd=3,
     #                fg="black")
    #btn1.place(x=220, y=62)

    btn2 = tk.Button(root, text="Finish", fg='blue',command= finalize, image=photoimage, compound="right", font=("arial", 15, "bold") ,bd=3,bg="white")
    btn2.place(x=800, y=600)
    #var = tk.StringVar()
    #droplist = tk.OptionMenu(root, var, *NamesOfBooks)
    #var.set("Select book ")
    #droplist.config(width=30,bg="white")
    #droplist.place(x=10, y=100)

    scrollbar = tk.Scrollbar(root,bg ='white')
    #scrollbar.pack(side=tk.RIGHT, fill=tk.Y,ipadx=5,ipady=5)
    scrollbar.place(x=370, y=100 ,height = 200,width = 20 )
    mylist = tk.Listbox(root, yscrollcommand=scrollbar.set, bd=1, height=10 )
    for line in range(len(NamesOfBooks)):
        mylist.insert(tk.END,NamesOfBooks[line] )
    mylist.place(x=10, y=100 ,height = 200 ,width = 320)
    scrollbar.config(command=mylist.yview)
    btn4 = tk.Button(root, text="Select Book", fg='blue', font=("arial", 10, "bold") ,bd=3,bg="white",
                     command =partial(selected_item,mylist))
    btn4.place(x=30, y=300)




except :

    print("gui error ")
    exit()


root.mainloop()