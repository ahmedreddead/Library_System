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
NamesOfBooks = d.Name.unique()
level = d.Level.unique()
nbook ='Aim High'
Data1 = d[d['Name'] == nbook]
Data1 = Data1['Level'].unique()
print(Data1)
head = d[  d['Name'] == nbook ]
head =head [ head['Level']==Data1[0] ]
print(head['head'].unique())
'''