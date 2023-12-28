from tkinter import *
from tkinter import ttk,messagebox,filedialog

import pandas
import ttkthemes
import time  # Add this import statement
import pymysql

# Functionality Part

def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.cvs')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')

def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,nameEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, )
    idEntry = Entry(screen, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'))
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'))
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'))
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'))
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, )
    genderEntry = Entry(screen, font=('roman', 15, 'bold'))
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'))
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update Student':

        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        listdata=content['values']
        idEntry.insert(0,listdata[0])
        nameEntry.insert(0,listdata[1])
        phoneEntry.insert(0,listdata[2])
        emailEntry.insert(0,listdata[3])
        addressEntry.insert(0,listdata[4])
        genderEntry.insert(0,listdata[5])
        dobEntry.insert(0,listdata[6])

def update_data():
    query='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modifide successfilly')
    screen.destroy()
    show_student()

def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'This {content_id} is deleted succesfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)

def search_data():
    query='select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)

def add_data():
    if idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()=='' or dobEntry.get()=='':
        messagebox.showerror('error','All Feilds are required',parent=add_window)

    else:
        currentdate = time.strftime('%d/%m/%y')
        currenttime = time.strftime('%H:%M:%S')
        try:
            query = 'Insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get(), currentdate, currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully, Do you want to clean the form?')
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)

            else:
                pass
        except:
            messagebox.showerror('Error','Id can not be repeated',parent=add_window)
            return

            query='select *from student'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            studentTable.delet(*studentTable.get_children())
            for data in fetched_data:
                studentTable.insert('',END,values=datalist)


def connect_database():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host='localhost',user='root',password='')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)
            query=('create table student(id int not null primary key, name varchar(30),mobile varchar(10), email varchar(30),'
                   ' address varchar(100), gender varchar(30), dob varchar(20), date varchar(50), time varchar(50))')
            mycursor.execute(query)
        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
            messagebox.showinfo('Success','Database Connection is successful', parent=connectWindow)
            connectWindow.destroy()
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.geometry('430x160+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=10)

    hostEntry=Entry(connectWindow,font=('romam',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=20)

    usenameLabel=Label(connectWindow,text='User Name',font=('arial',20,'bold'))
    usenameLabel.grid(row=1,column=0,padx=10)

    usenameEntry=Entry(connectWindow,font=('romam',15,'bold'),bd=2)
    usenameEntry.grid(row=1,column=1,padx=20)

    passwordLabel=Label(connectWindow,text='Password',font=('arial',20,'bold'))
    passwordLabel.grid(row=2,column=0,padx=10)

    passwordEntry=Entry(connectWindow,font=('romam',15,'bold'),bd=2)
    passwordEntry.grid(row=2,column=1,padx=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

count = 0
text = ''
s = 'Student Management System'

def slider():
    global text, count, s
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

def clock():
    global  date,currenttime
    date = time.strftime('%d/%m/%y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

# GUI Part
root = ttkthemes.ThemedTk()

# Create a themed style
style = ttk.Style(root)

# Set the theme using the theme_use method
style.theme_use('radiance')  # Replace 'radiance' with the theme you prefer

root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

datetimeLabel = Label(root, text='hello', font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

sliderLabel = Label(root, text=s, font=('arial', 28, 'bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect database',command=connect_database)
connectButton.place(x=900, y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='Image/studen.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda :toplevel_data('Add Student','Add',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda :toplevel_data('Serch student','Search',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda :toplevel_data('Update Student','Update',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitstudentButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitstudentButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root,bg='yellow')
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,column=('Id','Name','Mobile No','Email','Address','Gender','D.O.B','Added Date','Added Time'),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No',text='Mobile No')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Mobile No',width=200,anchor=CENTER)
studentTable.column('Email',width=300,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=100,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=200,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),foreground='red',background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='red')

studentTable.config(show='headings')

root.mainloop()
