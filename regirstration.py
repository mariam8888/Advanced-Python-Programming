from tkinter import *
from PIL import Image , ImageTk


def user_auth(name , email , date , loc):
  auth = Toplevel()
  auth.title('Account Creation')
  auth.minsize(800,420)
  auth.maxsize(800,420)
  auth.config(bg="white")
  auth.iconbitmap(f'{loc}iconbitmap.ico')
  # creating the canvas
  verification_logo = Image.open(f"{loc}account_ver.png")
  account_background = Canvas(auth,width=242,height=233 ,bg="white", highlightthickness=0)
  account_background.image = ImageTk.PhotoImage(verification_logo)
  account_background.create_image(0,0,image=account_background.image, anchor=NW)
  account_background.place(x=50,y=100)
  # Label
  Label(auth , text="Welcome On Board", bg="white",font=("Verdana",15 , "bold")).place(x=300,y=30)
  Label(auth , text=name, bg="white",font=("Verdana",15)).place(x=330,y=120)
  Label(auth , text=email, bg="white",font=("Verdana",15)).place(x=330,y=180)
  Label(auth , text=date, bg="white",font=("Verdana",15)).place(x=330,y=240)
  Label(auth , text="Click here to Exit", bg="white",font=("Verdana",15)).place(x=330,y=300)
  Button(auth, text="exit",font=("Verdana",15),bg="white",relief=GROOVE , command=auth.destroy).place(x=525, y=300, height=35,width=100)
  auth.mainloop()
