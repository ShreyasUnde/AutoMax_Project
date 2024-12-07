#wapp to make a GUI to get random motivational messages

from tkinter import *
import requests
from tkinter.messagebox import *



root=Tk()
root.title("Motivational Messages ")
root.geometry('1000x500+100+100')
f=("Arial",25,"bold","italic")
lab_name=Label(root,text="Motivational Message",font=f,)
lab_name.pack(pady=20)

def getQuote():
    try:
        wa="https://api.quotable.io/random"
        res=requests.get(wa)
        # print(res)
        data=res.json()
        # print(data)
        msg=data['content']
        print(msg)
        lab_msg.configure(text=msg)
    except Exception as e:
        print("Issue",e)
btn_quote=Button(root,text="Quote",font=f,command=getQuote,bg="palegreen",relief="sunken")
btn_quote.pack(pady=25)
lab_msg=Label(root,text="",font=f,wraplength=500)
lab_msg.pack(pady=30)
root.mainloop()
