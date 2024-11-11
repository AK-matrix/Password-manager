#libraries
from deepface import DeepFace
import cv2 
import tkinter as tk
from tkinter import ttk
from tkinter import *
import time
import os
import pickle
label_font = font.Font(weight="bold",20)

#functions
def home():
    global btn
    global btn1
    global btn2
    global lbl2
    lbl2 = Label(root, text = "Choose one of the operations below:",font=label_font)
    lbl2.grid(column = 0,row = 2)
    btn = Button(root,text = "View passwords",fg = "black", command = view,font=label_font)
    btn.grid(column = 0, row = 4)
    btn1 = Button(root,text = "Delete password",fg = "black", command = delete,font=label_font)
    btn1.grid(column = 0, row = 6)
    btn2 = Button(root,text = "Update password",fg = "black", command = update,font=label_font)
    btn2.grid(column = 0, row = 8)

    root.mainloop()

def back():
    global btn4
    head.destroy()
    u.destroy()
    btn4.destroy()
    home()
    
def clear():
    btn.destroy()
    btn1.destroy()
    btn2.destroy()
    lbl2.destroy()

def view():
    global btn1
    global btn4
    global u
    global head
    clear() #clears home page
    f = open("passwords.bin","rb")
    head = Label(root, text ="Here are your passwords",font=label_font)
    head.grid(column = 0, row = 2)
    y = pickle.load(f)
    t = ""
    for x in y:
        t+=x + ": " + y[x] + 2*"\n"
    
    u = Label(root, text = t,font=label_font)
    u.grid(column = 1,row = 5)

    btn4 = Button(root,text = "Back to home",fg = "black", command = back,font=label_font)
    btn4.grid(column = 0, row = 15)

    f.close()
    root.mainloop()

def delete():
    global u
    global btn4
    global head
    clear()
    def deleteinput():
        del z[u.get().lower()]
        btn5.destroy()
        f = open("passwords.bin","wb")
        pickle.dump(z,f)
        f.close()
        btn5.destroy()
    head = Label(root, text="Enter the password to be deleted (e.g:gmail):",font=label_font) #TBD
    u = Entry(root, width=10)
    u.grid(column =1, row =0)
    head.grid(column = 0, row = 4)
    f = open("passwords.bin","rb+")
    z = pickle.load(f)
    btn5 = Button(root,text = "Submit",fg = "black", command =deleteinput,font=label_font )
    btn5.grid(column = 2, row = 15)
    f.close()
    os.remove("passwords.bin")
    btn4 = Button(root,text = "Back to home",fg = "black", command = back,font=label_font)
    btn4.grid(column = 0, row = 15)
    #print("Password successfully deleted") #TBD
    root.mainloop

def update():
    global u
    global btn4
    global head
    clear()
    f = open("passwords.bin","rb+")
    m = pickle.load(f)
    def add():
        m[txt.get().lower()] = u.get()
        txt.destroy()
        f = open("passwords.bin", "wb")
        pickle.dump(m, f)
        f.close()
        btn6.destroy()
    head = Label(root, text = """Enter the password to added or updated (eg:gmail):


Enter new password""", font=(slant="italic",weight= "bold"))
    btn6 = Button(root,text = "Submit",fg = "black", command = add,font=label_font)
    btn6.grid(column = 0, row = 20)
    head.grid(column=0, row = 2)
    txt = Entry(root, width = 15) #TBD
    txt.grid(column = 6, row = 2)
    u = Entry(root, width = 15)
    u.grid(column = 6, row = 5)
    f.close()
    os.remove("passwords.bin")
    btn4 = Button(root,text = "Back to home",fg = "black", command = back,font=label_font)
    btn4.grid(column = 0, row = 15)
    root.mainloop()
    
def popup(msg):
     pop =tk.Tk()
     pop.wm_title("Attention!")
     label = ttk.Label(pop,text=msg,font = ("Verdana", 18))
     label.pack(side = "top", fill = "x", pady = "10")
     button = ttk.Button(pop, text = "Okay", command = pop.destroy)
     button.pack()
     pop.mainloop()  

def facerecognition(): #the face recogition system using machine learning  

    #to capture camera frames and display them
    video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    #frame width and height
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 700)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

    frame_count = 0 #frame number
    sec = 0 #time 
    face_match = False #verification result
    ref_img = cv2.imread("ABC.jpeg") #reference image

    

    #verification loop
    while True:
        image,frame = video.read()

        if image: #if there's a return value

            if frame_count%40  == 0: #verification once in 40 frames

                
                    try:
                         if DeepFace.verify(frame,ref_img.copy())['verified']: #checks deepface's dictionary's value for the key 'verified'
                              face_match = True 

                         else:
                              face_match = False 
            
                    except ValueError:
                         face_match = False #when camera pointed at objects
                    
            frame_count+=1

            if face_match == True: #displays result of the verification on the screen

                cv2.putText(frame,"Access Granted", (15,250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0)) #MUST BE DISPLAYED ON THE APP
                popup("""Face verification successful""")
                cv2.destroyAllWindows()
                return True

            else:
                cv2.putText(frame,"Adjust Face", (15,250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0))
                if frame_count>500:
                    popup("""Face verification failed
                      ACCESS DENIED""")
                    cv2.destroyAllWindows()
                    return False

            cv2.imshow("Verifying face",frame)
            x = cv2.waitKey(1)
        else:
               time.sleep(0.1)
               sec+=0.1

        if(video.isOpened()==False) and sec>10: #incase camera is not accessable
               popup("""Your camera device is not accessible
               ACCESS DENIED""")
               cv2.destroyAllWindows()
               return False
        
#main
if facerecognition():
     root = Tk()
     root.config(bg="#5fb3b3")
     style = ttk.Style(root)
     style.theme_use('clam')
     root.state('zoomed')
     root.title("Password manager")
     root.geometry('800x400')
     lbl = Label(root, text = "Face verification successful!",font=label_font)
     lbl.grid(column = 0,row = 0)
     loop = 0
     home()
     root.mainloop()
       
        
        








