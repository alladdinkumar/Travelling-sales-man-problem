from tkinter import *
import sqlite3

def database_entry():
    print("New datbase entry")
def matrix_entry():
    top=Tk()
    
    for i in range(5):
        l[i]=Label(top,text=city[i])
        l[i].grid(row=0,column=i+1)
    
    k=0
    for i in range(5):
        l[i]=Label(top,text=city[i])
        l[i].grid(row=i+1)
        for j in range(5):
            e[k]=Entry(top,bd=5)
            e[k].grid(row=i+1,column=j+1)
            k+=1
    b=Button(top,text="Enter",command=matrix_copy_to_local)
    b.grid(row=6) 
    top.mainloop()  
def city_entry():
    top=Tk()
    for i in range(5):
        l[i]=Label(top,text="City"+str(i+1))
        l[i].grid(row=i,column=0)
        c[i]=Entry(top,bd=5)
        c[i].grid(row=i,column=1)
    b=Button(top,text="calculate",command=copy_city_to_local)
    b.grid(row=5)
    top.mainloop()
def copy_city_to_local():
    for i in range(5):
        city.append(c[i].get())
    matrix_entry()
    
def matrix_copy_to_local():
    k=0
    for i in range(5):
        city_mat.append([])
        for j in range(5):
            city_mat[i].append(e[k].get())
            k+=1
    calculation()
            
def calculation():
    print("calculating....")
    
    
    

        
city=[]
l=list( i for i in range(5))
c=list( i for i in range(5))
city_mat=[]
e=list( i for i in range(25))
city_entry()


    
    
    
    
        










