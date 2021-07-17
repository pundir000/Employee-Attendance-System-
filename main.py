from tkinter import*
import tkinter
import qrcode
from PIL import Image,ImageTk
from resizeimage import resizeimage
import cv2
import numpy as numpy
import pyzbar.pyzbar as pyzbar
import time
from time import strftime
from datetime import datetime
import pybase64
import mysql.connector
from tkinter import messagebox
import csv




class Qr_Generator:
    def __init__(self,root):
        self.root=root
        self.root.geometry("900x500+200+50")
        self.root.title("Employee Attendance System")
        #self.root.resizable(False,False)
        

        title=Label(self.root,text="Employee Attendence System ",font=("times new roman",40),bg='#053245',fg='white').place(x=0,y=0,relwidth=1)
    #-------------------------------Employee Details Window----------------------------------#
    #-----------------Variable-----------------#
        self.var_emp_code=StringVar()
        self.var_name=StringVar()
        self.var_department=StringVar()
        self.var_designation=StringVar()


        emp_Frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        emp_Frame.place(x=50,y=100,width=500,height=380)

        emp_title=Label(emp_Frame,text="Employee Details ",font=("goudy old style",20),bg='#043256',fg="white").place(x=0,y=0,relwidth=1)
        lbl_emp_code=Label(emp_Frame,text="Employee ID ",font=("times new roman",15,'bold'),bg='white').place(x=20,y=60)
        lbl_emp_name=Label(emp_Frame,text="Name ",font=("times new roman",15,'bold'),bg='white').place(x=20,y=100)
        lbl_emp_department=Label(emp_Frame,text="Department",font=("times new roman",15,'bold'),bg='white').place(x=20,y=140)
        lbl_emp_designation=Label(emp_Frame,text="Designation",font=("times new roman",15,'bold'),bg='white').place(x=20,y=180)


        txt_emp_code=Entry(emp_Frame,font=("times new roman",15),textvariable=self.var_emp_code,bg='lightyellow').place(x=200,y=60)
        txt_emp_name=Entry(emp_Frame,font=("times new roman",15),textvariable=self.var_name,bg='lightyellow').place(x=200,y=100)
        txt_emp_department=Entry(emp_Frame,font=("times new roman",15),textvariable=self.var_department,bg='lightyellow').place(x=200,y=140)
        txt_emp_designation=Entry(emp_Frame,font=("times new roman",15),textvariable=self.var_designation,bg='lightyellow').place(x=200,y=180)


        btn_generate=Button(emp_Frame,text='QR Generator',command=self.generate,font=("times new roman",18,'bold'),bg="#2196f3",fg="white").place(x=60,y=250,width=180,height=30)
        

        btn_scan=Button(emp_Frame,text='QR Scanner',command=self.Qr_Read,font=("times new roman",18,'bold'),bg="#2196f3",fg="white").place(x=270,y=250,width=180,height=30)

        btn_list=Button(emp_Frame,text='Register',command=self.store,font=("times new roman",18,'bold'),bg="#2196f3",fg="white").place(x=60,y=290,width=180,height=30)
        btn_clear=Button(emp_Frame,text='Clear',command=self.clear,font=("times new roman",18),bg="#607d8b",fg="white").place(x=270,y=290,width=120,height=30)
        self.msg=''
        self.lbl_msg=Label(emp_Frame,text=self.msg,font=("times new roman",15,'bold'),bg='white',fg='green')
        self.lbl_msg.place(x=0,y=330,relwidth=1)



        #-------------------------------Employee QR Code Window----------------------------------#
       
        qr_Frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        qr_Frame.place(x=600,y=100,width=250,height=380)

        qr_title=Label(qr_Frame,text="QR Code ",font=("goudy old style",20),bg='#043256',fg="white").place(x=0,y=0,relwidth=1)

        self.qr_code=Label(qr_Frame,text="No QR Code\nAvailable",font=("times new roman",15),bg='#3f51b5',fg="white",bd=1,relief=RIDGE)
        self.qr_code.place(x=35,y=100,width=180,height=180)

    def clear(self):

        self.var_emp_code.set(' ')
        self.var_name.set(' ')
        self.var_department.set(' ')
        self.var_designation.set(' ')
        self.msg=''
        self.lbl_msg.config(text=self.msg)
        self.qr_code.config(image='')
    
    def generate(self):
        if self.var_name.get()=='' or self.var_department.get()=='' or self.var_designation.get()=='':
            self.msg='All Fields are Required!!!'
            self.lbl_msg.config(text=self.msg,fg="red")
        else:
        
            qr_data=(f"Employee ID:{self.var_emp_code.get()} Employee Name:{self.var_name.get()} Department:{self.var_department.get()} Designation:{self.var_designation.get()}")
            qr_code=qrcode.make(qr_data)
            qr_code=resizeimage.resize_cover(qr_code,[180,180])
            qr_code.save("Employee_Qr/Emp_"+str(self.var_emp_code.get())+'.png')
            #---------------------QR Code Image Update----------------#
            self.im=ImageTk.PhotoImage(file="Employee_Qr/Emp_"+str(self.var_emp_code.get())+'.png')
            self.qr_code.config(image=self.im)

            
            #=------------------updating Notification------------------#
            self.msg='QR Generated Successfully!!!'
            self.lbl_msg.config(text=self.msg,fg="green")
    
    
    def Qr_Read(self):
       cap= cv2.VideoCapture(0)
       names=[]
# function  for attendence file
       fob=open('AttendenceList.csv','a+')
       
       def enterData(z):
           
           if z in names:
               pass
           else:
               names.append(z)
               z=''.join(str(z))
               now=datetime.now()
               d1=now.strftime("%d/%m/%Y")
               dtString=now.strftime("%H:%M:%S")
               fob.write(z+" "+d1 +" "+dtString +'\n')
#             self.mark_Attendence(i,n,d,dg)
           return names
       print('Reading......')
# function data present or not
       def checkData(data):
           data=str(data,'UTF-8')
           if data in names:
               print('Already Present')
           else:
               print('\n'+str(len(names)+1)+'\n'+'Present done')
               enterData(data)

       while True:
           _,frame=cap.read()
           decodedObject= pyzbar.decode(frame)
           for obj in decodedObject:
               checkData(obj.data)
               time.sleep(1)

           cv2.imshow('Frame',frame)
    #close
           if cv2.waitKey(1)& 0xff==ord('s'):
               cv2.destroyAllWindows()
               break
       fob.close()


#-------------------attendence-------------------------#
#    def mark_Attendence(self,i,n,d,dg):
#        i=self.var_emp_code.get() 
#        n=self.var_name.get()
#        d=self.var_department.get()
#        dg=self.var_designation.get()
#        with open("AttendenceList.csv","r+",newline="\n") as f:
#            myDataList=f.readlines()
#            name_List=[]
#            for line in myDataList:
#                entry=line.split((","))
#                name_List.append(entry[0])
#                if((i not in name_List) and (n not in name_List) and (d not in name_List) and (dg not in name_List)):
#                    now=datetime.now()
#                    d1=now.strftime("%d/%m/%Y")
#                    dtString=now.strftime("%H:%M:%S")
#                    f.writelines(f"\n{i},{n},{d},{dg},{dtString},{d1},Present")
                
                


    def store(self):
        id=self.var_emp_code.get()
        n=self.var_name.get()
        d=self.var_department.get()
        des=self.var_designation.get()


        if(id=="" or n=="" or d=="" or des==""):
            print("Error")
            tkinter.messagebox.showerror("Error","There was issue with some information")
            self.var_emp_code.set("")
            self.var_name.set("")
            self.var_department.set("")
            self.var_designation.set("")
        else:
            result=tkinter.messagebox.askquestion("Submit","You are about to enter the following data\n"+id+"\n"+n+"\n"+d+"\n"+des+"\n")
            if(result=='yes'):
                print("Done")
                with open('EmployeeList.csv','a') as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow([id,n,d,des])
                csvfile.close()
            else:

                self.var_emp_code.set("")
                self.var_name.set("")
                self.var_department.set("")
                self.var_designation.set("")

root=Tk()
obj=Qr_Generator(root)
root.mainloop()