"""
Documentation:
Name: Snehith, Siddhi Vinayak, Sriram
Roll: 1727274
Title: Student Academic Calendar
"""

from tkinter import*
from tkcalendar import*
import sqlite3
connection = sqlite3.connect("mydatabase.db")# Connecting to database
crsr = connection.cursor()
event = ''
old_event =  ''
new_event = ''
username=''
password=''
win=Tk()
win.geometry("600x400")
win.title("Student Academic Calendar")
win.configure(bg="sky blue")


def Teacher():
    top=Toplevel(win)
    top.geometry("1100x1000")
    top.configure(bg="sky blue")
    title=Label(top,text="STUDENT ACADEMIC CALENDAR",font=("times new roman",20),bg="white").grid(row=0,column=0,padx=20,pady=10)
    cal=Calendar(top,selectmode="day")
    cal.grid(padx=50,pady=10,ipadx=150,ipady=200)

    def fetch_event():
        global date1
        date1=cal.get_date()
        sql_command = """SELECT DISTINCT * FROM events WHERE event_date = '""" + date1 + """'""" 
        crsr.execute(sql_command)
        ans = crsr.fetchall()
        if(ans == []):
            topne=Toplevel(win)
            topne.geometry("200x200+800+300")
            topne.configure(bg="sky blue")
            print("No events")
            noevents=Label(topne,text="No Events",font=("calibri",25)).pack(padx=20,pady=20)
            topne.after(2500,topne.destroy)
            return
        tope=Toplevel(win)
        tope.geometry("350x400+785+200")
        tope.configure(bg="sky blue")
        thevents=Label(tope,text="The Events are-",font=("calibri",20)).grid(padx=20,pady=5)
        for i in ans:
            print(i[1])
            event= Label(tope,text=i[1],font=("Calibri",15)).grid(padx=10,pady=10)
        tope.after(2500,tope.destroy)
        
                
    def insert_event():
        topi=Toplevel(win)
        topi.geometry("500x500")
        topi.configure(bg="sky blue")
        global date1
        global event
        Label(topi,text="Enter event",font=("Calibri",10)).pack(padx=10,pady=10)
        entry= Entry(topi, width= 40)
        entry.focus_set()
        entry.pack(padx=1,pady=10)
        def calendar():
            def grabdate():
                date1=cal.get_date()
                event=entry.get()
                event=event.upper()
                if(event==''):
                    Label(topi,text="Enter event",font=("Calibri",15)).pack(padx=10,pady=10)
                    return
                sql_command = """SELECT DISTINCT * FROM events WHERE event_date = '""" + date1 + """'""" 
                crsr.execute(sql_command)
                ans = crsr.fetchall()
                found = False
                for i in ans:
                    if(event == ans[0][1]):
                        found = True
                if(found):
                    topne=Toplevel(win)
                    topne.geometry("300x200+500+500")
                    topne.configure(bg="sky blue")  
                    print("event already exists")
                    noevents=Label(topne,text="Event already exists",font=("calibri",15)).pack(padx=15,pady=20)
                    topne.after(2000,topne.destroy)
                    return
                
                sql_command = """INSERT INTO events (event_date, event_title) VALUES (?,?)"""
                print(sql_command)
                params = (date1,event)
                crsr.execute(sql_command,params)
                connection.commit()
                success=Label(topi,text="Event added Successfully",font=("calibri",15)).pack(padx =5,pady=5)
            cal=Calendar(topi,selectmode="day")
            cal.pack(padx=10,pady=10)
            okbutton=Button(topi,text="OK",command=grabdate).pack()
        Button(topi,text="See Calendar",command=calendar).pack(padx=10,pady=10)
        Label(topi,text="Select date from Calendar",font=("calibri",10),).pack(padx=10,pady=10)
        topi.after(50000,topi.destroy)
        
    def update_event():
        topu=Toplevel(win)
        topu.geometry("720x600")
        topu.configure(bg="sky blue")
        global date1
        global old_event
        global new_event
        Label(topu,text="Select date from Calendar",font=("calibri",10),).pack()
        Label(topu,text="Enter event to be updated",font=("Calibri",10)).pack(padx=10,pady=10)
        entry1= Entry(topu, width= 40)
        entry1.focus_set()
        entry1.pack(padx=1,pady=10)
        Label(topu,text="Enter event",font=("Calibri",10)).pack(padx=10,pady=10)
        entry2= Entry(topu, width= 40)
        entry2.focus_set()
        entry2.pack(padx=1,pady=10)
        def calendar():
            def grabdate():
                date1=cal.get_date()
                old_event=entry1.get()
                new_event=entry2.get()
                old_event=old_event.upper()
                new_event=new_event.upper()
                if(old_event=='')or(new_event==''):
                    Label(topu,text="Enter events",font=("Calibri",15)).pack(padx=10,pady=10)
                    return
                sql_command = """SELECT DISTINCT * FROM events WHERE event_date = '""" + date1 + """'""" 
                crsr.execute(sql_command)
                ans = crsr.fetchall()
                print(ans)
                found = False
                for i in ans:
                    if(old_event == ans[0][1]):
                        found = True
                if(not found):
                    topne=Toplevel(win)
                    topne.geometry("200x200+600+500")
                    topne.configure(bg="sky blue")  
                    print("no events")
                    noevents=Label(topne,text="No Events",font=("calibri",25)).pack(padx=20,pady=20)
                    topne.after(2000,topne.destroy)
                    return
                sql_command  = """UPDATE events SET event_title = '"""+ new_event + """' WHERE event_date ='"""+date1+"""'"""+ """and event_title = '"""+old_event+"""'"""
                print(sql_command)
                crsr.execute(sql_command)
                connection.commit()
                success=Label(topu,text="Event Updated Successfully",font=("calibri",20)).pack(padx =10,pady=10)
            cal=Calendar(topu,selectmode="day")
            cal.pack()
            okbutton=Button(topu,text="OK",command=grabdate,activebackground="grey").pack()
        Button(topu,text="See Calendar",command=calendar).pack(padx=10,pady=10)
        topu.after(50000,topu.destroy)    
    def delete_event():
        topd=Toplevel(win)
        topd.geometry("720x720")
        topd.configure(bg="sky blue")
        global date1
        Label(topd,text="Select date from Calendar",font=("calibri",10),).pack()
        Label(topd,text="Enter event to be deleted",font=("Calibri",10)).pack(padx=10,pady=10)
        entry= Entry(topd, width= 40)
        entry.focus_set()
        entry.pack(padx=1,pady=10)
        def calendar():
            def grabdate():
                date1=cal.get_date()
                event=entry.get()
                event=event.upper()
                if(event==''):
                    Label(topd,text="Enter event",font=("Calibri",15)).pack(padx=10,pady=10)
                    return
                sql_command = """SELECT DISTINCT * FROM events WHERE event_date = '""" + date1 + """'""" 
                crsr.execute(sql_command)
                ans = crsr.fetchall()
                found = False
                for i in ans:
                    if(event == ans[0][1]):
                        found = True
                if(not found):
                    topne=Toplevel(win)
                    topne.geometry("200x200+500+500")
                    topne.configure(bg="sky blue")
                    print("no events")
                    noevents=Label(topne,text="No Events",font=("calibri",25)).pack(padx=20,pady=20)
                    topne.after(2000,topne.destroy)
                    return
                sql_command  = """DELETE FROM events WHERE event_title = '"""+event+"""'"""+ """and event_date = '"""+date1+"""'"""
                print(sql_command)
                crsr.execute(sql_command)
                connection.commit()
                success=Label(topd,text="Event deleted Successfully",font=("calibri",15)).pack(padx=5,pady=5)
            cal=Calendar(topd,selectmode="day")
            cal.pack()
            okbutton=Button(topd,text="OK",command=grabdate,activebackground="grey",height=1,width=4).pack()
        Button(topd,text="See Calendar",command=calendar).pack(padx=10,pady=10)
        topd.after(50000,topd.destroy)

    tviewbutton=Button(top,text="View Event",activebackground="grey",command=fetch_event,height=3,width=10).place(x=300,y=700)
    addbutton=Button(top,text="Add Event",activebackground="grey",command=insert_event,height=3,width=10).place(x=400,y=700)
    updatebutton=Button(top,text="Update Event",activebackground="grey",command=update_event,height=3,width=10).place(x=500,y=700)
    deletebutton=Button(top,text="Delete Event",activebackground="grey",command=delete_event,height=3,width=10).place(x=600,y=700)
def credentials():
    global username
    global password
    verified = False
    topc=Toplevel(win)
    topc.geometry("400x400")
    topc.configure(bg="sky blue")
    lusername=Label(topc,text="Username",font=("Times new roman",15)).pack(padx=5,pady=5)
    entryu= Entry(topc, width= 40)
    entryu.focus_set()
    entryu.pack(padx=1,pady=10)
    lpassword=Label(topc,text="Password",font=("Times new roman",15)).pack(padx=5,pady=5)
    entryp= Entry(topc,show='*', width= 40)
    entryp.focus_set()
    entryp.pack(padx=1,pady=10)
    def submit():
        username=entryu.get()
        username=username.lower()
        password=entryp.get()
        password=password.lower()
        sql_command="""SELECT user_name,pass_word FROM credentials WHERE user_name = ? and pass_word = ?"""
        params = (username,password)
        res = list(crsr.execute(sql_command,params))
        print(res)
        if(res != []):
            Teacher()
        else:
            Invalid=Label(topc,text="INVALID CREDENTIALS",font=("Times new roman",15)).pack(padx=5,pady=10)
    submit=Button(topc,text="Submit",font=("times new roman",15),activeforeground="grey",command=submit).pack(padx=5,pady=5)
    topc.after(30000,topc.destroy)
        
title=Label(win,text="STUDENT ACADEMIC CALENDAR",font=("times new roman",25),bg="sky blue").grid(padx=10,pady=10)
choice= Label(win,text="Iam a",font=("calibri",20)).grid(padx=10,pady=10)
teacherbutton= Button(win,text="Teacher",command=credentials,height=3,width=10,activebackground="grey",bg ="white",font =("Times new roman",10)).grid(padx=10,pady=20)
def Student():
    top=Toplevel(win)
    top.geometry("1100x1000")
    top.configure(bg="sky blue")
    title=Label(top,text="STUDENT ACADEMIC CALENDAR",font=("times new roman",20),bg="white").grid(row=0,column=0,padx=20,pady=10)
    cal=Calendar(top,selectmode="day")
    cal.grid(padx=50,pady=10,ipadx=150,ipady=200)

    def fetch_event():
        global date1
        date1=cal.get_date()
        sql_command = """SELECT DISTINCT * FROM events WHERE event_date = '""" + date1 + """'""" 
        crsr.execute(sql_command)
        ans = crsr.fetchall()
        if(ans == []):
            topne=Toplevel(win)
            topne.geometry("200x200+800+300")
            topne.configure(bg="sky blue")
            print("no events")
            noevents=Label(topne,text="No Events",font=("calibri",25)).pack(padx=20,pady=20)
            topne.after(2000,topne.destroy)
            return
        tope=Toplevel(win)
        tope.geometry("350x400+785+200")
        tope.configure(bg="sky blue")
        thevents=Label(tope,text="The Events are-",font=("calibri",20)).grid(padx=20,pady=5)
        for i in ans:
            print(i[1])
            event= Label(tope,text=i[1],font=("Calibri",15)).grid(padx=10,pady=10)
        tope.after(2000,tope.destroy)
    sviewbutton=Button(top,text="View Event",activebackground="grey",command=fetch_event,height=3,width=10).place(x=300,y=700)
studentbutton= Button(win,text="Student",height=3,width=10,activebackground="grey",bg="white",command=Student,font =("Times new roman",10)).grid(padx=10,pady=30)
win.mainloop()
