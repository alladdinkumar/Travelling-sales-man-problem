from tkinter import *
import sqlite3

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
    
    if(found==1):
        result_visualization_from_db(city_lis,final_res)
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
    
def result_visualization_from_db(city_lis,final_res):
    top=Tk()
    j=0
    for i in range(6):
        if(i==5):
            l[i]=Label(top,text=str(city_lis[0]))
            l[i].grid(row=7,column=8+i)
        else:
            l[i]=Label(top,text=str(city_lis[j])+"-------->")
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
 

    
    
    
    
        










