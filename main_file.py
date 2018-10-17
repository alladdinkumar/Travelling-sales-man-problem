#login and admin modules-----------------------------------------------------------------------------------------------------------
from tkinter import *
import sqlite3
root = Tk()
root.title("Python: PROJECT")

USERNAME = StringVar()
PASSWORD = StringVar()
 
Top = Frame(root, bd=2)
Top.pack(side=TOP)
Form = Frame(root)
Form.pack(side=TOP)
 
lbl_title = Label(Top, text = "LOGIN", font=(15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=(14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=(14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)
 
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)

def Database():
    global conn, cursor
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE member")
    cursor.execute("CREATE TABLE member (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM member WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO member (username, password) VALUES('admin', 'admin')")
        conn.commit()

def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    lbl_home = Label(Home, text="Successfully Login!", font=(20)).pack()
    

def Login():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM member WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()


btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(row=3, columnspan=2)
btn_login.bind('<Return>', Login)

if __name__ == '__main__':
    root.mainloop()

#mathamatical calculation starts:
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
            city_mat[i].append(int(e[k].get()))
            k+=1
    TSP(city_mat)
            



#calculation algorithm starts-------------------------------------------------------------------------------------------------------------
def copy_to_final(curr_path):
    global final_path
    for i in range(5):
        final_path[i]=curr_path[i]
    final_path[5]=curr_path[0]
    

def first_min(city_mat,i):
    mini=float("inf")
    for k in range(5):
        if (city_mat[i][k]<mini and i!=k):
            mini=city_mat[i][k]
    return mini
def secondmin(city_mat,i):
    first=float("inf")
    second=float("inf")
    for j in range(5):
        if(i==j):
            continue
        if(city_mat[i][j]<=first):
            second=first
            first=city_mat[i][j]
        elif(city_mat[i][j]<=second and first!=city_mat[i][j]):
            second=city_mat[i][j]
    return second

def tsprec(city_mat,curr_bound,curr_weight,level,curr_path):
    
    global final_res,visited,final_path
    if level==5:
        if(city_mat[curr_path[level-1]][curr_path[0]]!=0):
            curr_res=curr_weight+city_mat[curr_path[level-1]][curr_path[0]]
            #print(curr_res)
            if(curr_res<final_res):
                copy_to_final(curr_path)
                final_res=curr_res
                
        return 

    for i in range(5):
        if(city_mat[curr_path[level-1]][i]!=0 and visited[i]==False):
            temp=curr_bound
            curr_weight+=city_mat[curr_path[level-1]][i]
            if(level==1):
                curr_bound-=((first_min(city_mat,curr_path[level-1])+first_min(city_mat,i))/2)
            elif(level!=1):
                curr_bound -= ((secondmin(city_mat, curr_path[level-1]) + 
							first_min(city_mat, i))/2)
            if(curr_bound+curr_weight< final_res):
                curr_path[level]=i
                visited[i] = True
              
                tsprec(city_mat,curr_bound, curr_weight, level+1,curr_path)
            curr_weight -= city_mat[curr_path[level-1]][i]
            curr_bound = temp
            for l in range(5):
                visited[l]= False
            for j in range(level):
                visited[curr_path[j]] = True
def TSP(city_mat):
    
    
    global final_res,visited,final_path
    curr_path=[-1,-1,-1,-1,-1,-1]
    curr_bound=0
    for j in range(5):
                visited[j] = 0
	
    for i in range(5):
        curr_bound += (first_min(city_mat, i) + secondmin(city_mat, i))

	
    if (curr_bound %2 !=0):
         curr_bound=curr_bound/2 + 1
    else:
         curr_bound=curr_bound/2
    
    visited[0] = True
    curr_path[0] = 0

	
    tsprec(city_mat,curr_bound, 0, 1,curr_path);

    
    result_visualization(final_path,city,final_res)
    




#calculation algorithm ends--------------------------------------------------------------------------------------------------------------


 
def result_visualization(path,city,final_res):
    top=Tk()
    j=0
    for i in range(6):
        if(i==5):
            l[i]=Label(top,text=str(city[path[j]-1]))
            l[i].grid(row=7,column=8+i)
        else:
            l[i]=Label(top,text=str(city[path[j]-1])+"-------->")
            l[i].grid(row=7,column=8+i)
        j=j+1

    l1=Label(top,text="Total distance of the path = "+ str(final_res))
    l1.grid(row=9)
    top.mainloop()

    

final_path=[float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf")]
visited=[0,0,0,0,0]
final_res=float("inf")  

        
city=[]
l=list( i for i in range(6))
c=list( i for i in range(5))
city_mat=[]
e=list( i for i in range(25))

city_entry()
 

    
    
    
    
        










