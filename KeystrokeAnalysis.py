from tkinter import *
import numpy as np
import json
from math import fabs
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText

current_kd=[]
current_ku=[]
trained = 0
classification_vector=[]
c_vector_overlap=[]
c_vector_undetected=[]
tbutton = None
tmsg=None
pwd = []
usr = ''
matrix=[]

def get_list(l):
    try:
        return json.loads(l)
    except Exception:
        return []

def get_float(f):
    return float(f) if f else 0


def norm(a,b, coeff):
    diff = np.array(a) - np.array(b)
    return np.matmul(np.matmul(diff,coeff),np.reshape(diff,(-1,1)))

def get_inverse_cov(matrix):
    cov_mat = np.cov(list(zip(*(l for l in matrix))))
    if(np.linalg.matrix_rank(cov_mat)<2):
        return False
    coeff = np.linalg.inv(cov_mat) if np.linalg.det(cov_mat) else np.linalg.pinv(cov_mat)
    return coeff

def verify_vector(username, vector):
    global matrix
    extn = ''
    positive = sum(x>=0 for x in vector)
    negative = sum(x<0 for x in vector)
    if(positive+negative==len(current_kd)*2-1):
        if not negative:
            extn='.vector'
            print('using vector')
        else:
            extn='.vector-overlap'
            print('using vector-overlap')
    else:
        extn='.vector-miss'
        print('using vector-miss')
    f=open(username+extn,'r')
    matrix = get_list(f.readline().strip())
    threshold=get_float(f.readline().strip())
    coeff = get_inverse_cov(matrix)
    if coeff is False:
        return False
    norms=[norm(vector,x,coeff) for x in matrix]
    print(str(norms))
    shortest = min(fabs(x)**0.5 for x in norms)
    print('SHORTEST',shortest)
    return True if shortest<4*threshold else False

def train(entry, parent):
    global trained
    global current_kd
    global current_ku
    global usr
    global tmsg
    processed = transform(current_kd,current_ku)
    positive = sum(x>=0 for x in processed)
    negative = sum(x<0 for x in processed)
    if(positive+negative==len(current_kd)*2-1):
        if not negative:
            classification_vector.append(processed)
        else:
            c_vector_overlap.append(processed)
    else:
        c_vector_undetected.append(processed)
    trained +=1
    tmsg.config(text="Trainings completed (out of 10):"+str(trained))
    entry.delete(0,END)
    current_kd =[]
    current_ku=[]
    if(trained >9):
        tbutton=Button(parent, text="register", command=lambda: save(usr.get(),parent))
        tbutton.grid(row=3, column=1, sticky=EW, padx=10,pady=10)
    return
