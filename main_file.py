from tkinter import *
import sqlite3

#global_variable-----------------------------------------------------------------------------------------------------------------------
final_path=[float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf")]
visited=[0,0,0,0,0]
final_res=float("inf")  

        
city=[]
l=list( i for i in range(6))
c=list( i for i in range(5))
city_mat=[]
e=list( i for i in range(25))

#======================================================================================================================================

def database_entry(path,city,dist):
    fin_path=str(city[path[0]-1])+","+str(city[path[1]-1])+"," +str(city[path[2]-1])+"," +str(city[path[3]-1])+"," +str(city[path[4]-1])        
    conn=sqlite3.connect("result.db")
    c=conn.cursor()
    try:
        c.execute("Insert into result values(?,?)",(fin_path,dist))
    except:
        c.execute("create table result (path text, diatance real)")
        c.execute("Insert into result values(?,?)",(fin_path,dist))
    c.execute("select * from result")
    s=c.fetchall()
    conn.commit()
    conn.close()
    result_visualization(path,city,final_res)

def matrix_entry():
    
    top=Tk()
    top.geometry("1400x700+0+0")
    top.title("CITY MATRIX")
    Top = Frame(top, bd=2)
    Top.pack(side=TOP)
    Form = Frame(top)
    Form.pack(side=TOP)
    lbl_title = Label(Top, text = "ENTER THE PATH DISTANCE BETWEEN THE CITIES", font=(15))
    lbl_title.pack(fill=X)
    for i in range(5):
        l[i]=Label(Form,text=city[i], font=(15))
        l[i].grid(row=0,column=i+1)
    
    k=0
    for i in range(5):
        l[i]=Label(Form,text=city[i], font=(15))
        l[i].grid(row=i+1)
        for j in range(5):
            if i==j:
                e[k]=Entry(Form,bd=5,state='disabled')
                e[k].grid(row=i+1,column=j+1)
                k+=1
            else:
                e[k]=Entry(Form,bd=5)
                e[k].grid(row=i+1,column=j+1)
                k+=1
    b=Button(Form,text="CALCULATE",command=matrix_copy_to_local, font=(15))
    b.grid(row=6)
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)
    top.mainloop()  
def city_entry():
    top=Tk()
    top.title("CITY ENTRY")
    top.geometry("1400x700+0+0")
    Top = Frame(top, bd=2)
    Top.pack(side=TOP)
    Form = Frame(top)
    Form.pack(side=TOP)
    lbl_title = Label(Top, text = "ENTER THE FIVE CITIES", font=(15))
    lbl_title.pack(fill=X)
    for i in range(5):
        l[i]=Label(Form,text="CITY"+str(i+1), font=(15))
        l[i].grid(row=i,column=15)
        c[i]=Entry(Form,bd=5)
        c[i].grid(row=i,column=16)
    b=Button(Form,text="SUBMIT",command=copy_city_to_local, font=(15))
    b.grid(row=5,column=15)
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)
    top.mainloop()
def search_in_database(city):
    final_res=0
    found=0
    conn=sqlite3.connect("result.db")
    c=conn.cursor()
    c.execute("select * from result")  
    rows=c.fetchall()
    for row in rows:
        row=list(row)
        city_lis=row[0].split(",")
        if(city[0] in city_lis and city[1] in city_lis and city[2] in city_lis and city[3] in city_lis and city[4] in city_lis):
            found=1
            final_res=row[1]
            fin_lis=city_lis
    
    if(found==1):
        result_visualization_from_db(fin_lis,final_res)
    else:
        matrix_entry()
        
        
    
    
def copy_city_to_local():
    for i in range(5):
        city.append(c[i].get())
    
    search_in_database(city)
    
def matrix_copy_to_local():
    k=0
    for i in range(5):
        city_mat.append([])
        for j in range(5):
            if i==j:
                city_mat[i].append(0)
                k+=1
            else:
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

    database_entry(final_path,city,final_res)
    
    




#calculation algorithm ends--------------------------------------------------------------------------------------------------------------


 
def result_visualization(path,city,final_res):
    top=Tk()
    top.title("RESULT")
    top.geometry("1400x700+0+0")
    Top = Frame(top, bd=2)
    Top.pack(side=TOP)
    Form = Frame(top)
    Form.pack(side=TOP)
    lbl_title = Label(Top, text = "The shortest path available by visiting each city exactly once and return to the starting city is", font=(15))
    lbl_title.pack(fill=X)
    j=0
    for i in range(6):
        if(i==5):
            l[i]=Label(Form,text=str(city[path[j]-1]), font=(15))
            l[i].grid(row=7,column=8+i)
        else:
            l[i]=Label(Form,text=str(city[path[j]-1])+"-------->", font=(15))
            l[i].grid(row=7,column=8+i)
        j=j+1

    l1=Label(Form,text="Total distance of the path = "+ str(final_res), font=(15))
    l1.grid(row=9)
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)
    top.mainloop()
    
def result_visualization_from_db(city_lis,final_res):
    top=Tk()
    top.geometry("1400x700+0+0")
    top.title("RESULT")
    Top = Frame(top, bd=2)
    Top.pack(side=TOP)
    Form = Frame(top)
    Form.pack(side=TOP)
    lbl_title = Label(Top, text = "The shortest path available by visiting each city exactly once and return to the starting city is", font=(15))
    lbl_title.pack(fill=X)
    j=0
    for i in range(6):
        if(i==5):
            l[i]=Label(Form,text=str(city_lis[0]), font=(15))
            l[i].grid(row=7,column=8+i)
        else:
            l[i]=Label(Form,text=str(city_lis[j])+"-------->", font=(15))
            l[i].grid(row=7,column=8+i)
        j=j+1

    l1=Label(Form,text="Total distance of the path = "+ str(final_res), font=(15))
    l1.grid(row=9)
    lbl_text = Label(Form)
    lbl_text.grid(row=2, columnspan=2)
    top.mainloop()
    
#login_module__________________________________________________________________________________________________________________________

root = Tk()
root.title("LOGIN")
root.geometry("1400x700+0+0")
#canvas = Canvas(root,width = 1400, height = 700)
#canvas.pack(expand = NO)
#img = PhotoImage(file = 'dnd.png')
#canvas.create_image(0, 0, image = img, anchor = NW)
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

flag=0
def Database():
    global conn, cursor,flag
    conn = sqlite3.connect("project.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("CREATE TABLE member (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
        cursor.execute("INSERT INTO member (username, password) VALUES('admin', 'admin')")
    except:
        cursor.execute("SELECT * FROM member WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            flag=1
    conn.commit()
def HomeWindow():
    global Home
    root.withdraw()
    city_entry()
    
    
def Login():
        
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        Database()
        if flag==1:
            lbl_home = Label(root, text="Successfully Login!", font=(20)).pack()
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
#login_module_ends------------------------------------------------------------------------------------------------------------------------------------



 

    
    
    
    
        










