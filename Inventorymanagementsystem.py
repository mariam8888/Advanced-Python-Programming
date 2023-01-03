# INVENTORY MANAGEMENT SYSTEM
from tkinter import *
from PIL import Image , ImageTk
from tkinter import ttk , messagebox , simpledialog
import sys
import hashlib # encryption cha
import sqlite3
import colorama
import customtkinter
from regirstration import user_auth
from security import sendemail
import random
import time


# THOSE ARE COLORS USED.
colorama.init(autoreset=True)
GREEN= colorama.Fore.GREEN
RED= colorama.Fore.RED
BLUE = colorama.Fore.BLUE


# TRY TO CHANGE THIS LOCATION AND DON'T FORGET, ADD ANOTHER \
LOCATION = "C:\\Users\\Maryam\\Desktop\\AGUI-IN-MA-SYS\\AGUI-IN-MA-SYS\\Project-images\\"
PRODUCT_LOCATION = "C:\\Users\\Maryam\\Desktop\\AGUI-IN-MA-SYS\\AGUI-IN-MA-SYS\\Product Images\\"


# ADMIN EMAIL:
ADMINEMAIL  = "mariambhatti8989@gmail.com"

# THIS IS THE BACKGROUND DESIGN AS WELL AS THE INCONBITMAP USED.
GUI_DESIGN = LOCATION+"Design.jpg"
VECTOR= LOCATION+"na_feb_10.ico"


# THOSE ARE THE FONT USED IN TEH WHOLE PROJECR.
TITLE = ("Candara",22)
INPUT = ("Verdana",15)
CUSTOM_FONT = ("Microsoft YaHei UI Light",19)
btn_font = ("Verdana" , 13)
font_applied = ('Verdana',14)
NEW_FONT= ('Tahoma', 14)
fnt= ('Verdana',16)

# DATABASE CONNECTION

database_name = "database.db"
database = sqlite3.connect(database_name , check_same_thread=False)
query = database.cursor() #identifier associated with a group of rows; enables traversal over rows of a result set 

SQL_TABLENAME = "User"
PRODUCT_TABLENAME = "Product"
ORDERTABLE = "Orders"



# THIS FUNCTION WILL TAKE A TREE VARIABLE AND CUSTOMIZE IT.
def style_tree(t):
  style = ttk.Style()
  style.theme_use("red")
  style.configure("Treeview" ,  
    background = "#D3D3D3",
    foreground = "black",
    rowheight = 30,
    fieldbackgound = "#D3D3D3"
  )
  t.tag_configure('oddrow' , background="white")
  t.tag_configure('evenrow' , background="lightblue")

def GUI():

  # THIS PART IS ONLY FOR USE
  # RS.
  def user_dahsboard(em,us):

    def place_an_order():
      
      def return_product():

        def order():

          def cancel_order():
            if messagebox.askokcancel(title='Order Confirmation', message="Are you sure you want to cancel your order."):
              or_cn.destroy()

          def confirm_order():
            message = f"""
            Dear {us},

            Thank you for shopping with us! We wanted to take a moment to confirm your recent purchase of [product name] and to thank you for your business.

            Here are the details of your order:

            Product: {product_details[0][1]}
            Quantity: {quantity}
            Final price: {fn_pr}
            Your account username is: {us}

            We will keep you updated on each step in the process, from the time your order is placed until it is delivered to your doorstep. You can track the progress of your order by logging in to your account on our website.

            We hope you are satisfied with your purchase and that you'll continue to shop with us in the future. If you have any questions or concerns, please don't hesitate to reach out to us.

            Sincerely,
            Order Fullfilment Team
          
            """
            if sendemail(em,message, "Order Confirmation"): 
              if messagebox.showinfo(title="Order Confirmation", message="Order has been confirmed successfully. An Email has been send to you, Please check your Inbox"):
                # We will insert this order in the Admin Order Fullfilement.
                data = [
                  (product_details[0][1],fn_pr,quantity,em, "False")
                ]
                query.executemany(f"INSERT INTO {ORDERTABLE} (Product_Title,Price_charged,Quantity_purchased,Customer_Email,Fullfiled) VALUES (?,?,?,?,?)",data)
                # Update the Product Quantity
                query.execute(F'UPDATE {PRODUCT_TABLENAME} Set Quantity= Quantity - (?) WHERE ID = (?)', (quantity,product_details[0][0]))
                database.commit() #saving everything in the database
                or_cn.destroy()
                order_quantity.delete(0,END)
            else:
              messagebox.showerror(title="Order Error", message="An Error has occured while sending the Email confirmation, please wait a little")
              time.sleep(2)
              sendemail(em,message)

          
          quantity= int(order_quantity.get())

          or_cn = Toplevel()
          or_cn.title('Order Confirmation')
          or_cn.minsize(500,425)         
          or_cn.maxsize(500,425)
          or_cn.config(bg="white")

          # LABELS:
          Label(or_cn, text="Order Confirmation", font=INPUT, bg="white").pack()
          Label(or_cn, text=f"Product Name:  {product_details[0][1]}",font=btn_font, bg="white").place(x=25,y=100)
          Label(or_cn, text=f"Quantity:  {quantity}",font=btn_font, bg="white").place(x=25,y=150)
          fn_pr = quantity*float(product_details[0][5])
          Label(or_cn, text=f"Final Price:  ${fn_pr}",font=btn_font, bg="white").place(x=25,y=200)

          # BUTTONS
          confirm = customtkinter.CTkButton(or_cn, text="Confirm", font=NEW_FONT, fg_color="Blue", command=confirm_order)
          confirm.place(x=50,y=250,width=150,height=35)
          cancel = customtkinter.CTkButton(or_cn, text="cancel", font=NEW_FONT, fg_color="Blue", command=cancel_order)
          cancel.place(x=250,y=250,width=150,height=35)


        # Getting Data From Client
        name = product_chosed.get()
        product_details = [pr_de for pr_de in query.execute(f'SELECT * FROM {PRODUCT_TABLENAME} WHERE Name = (?)',(name,)).fetchall()]
        
        # WE WILL CREATE A FRAME THAT WILL PUT THE PRODUCT INFORMATION ON IT.

        # PRODUCT IMAGE
        pr_img = Image.open(PRODUCT_LOCATION+product_details[0][7])

        product_image = Canvas(order_frame,width=400,height=475, highlightthickness=0)

        resizing = pr_img.resize((400,475), Image.ANTIALIAS)
        
        product_image.image = ImageTk.PhotoImage(resizing)
        product_image.create_image(0,0,image=product_image.image, anchor="nw")
        product_image.place(x=80,y=75)


        # FASH SHIPPING CANVAS
        fash_shipping = Image.open(LOCATION+"Faster_shipping.jpg")

        f_s_canvas = Canvas(order_frame,width=150,height=52, highlightthickness=0)

        resizing = fash_shipping.resize((150,52), Image.ANTIALIAS)
        
        f_s_canvas.image = ImageTk.PhotoImage(resizing)
        f_s_canvas.create_image(0,0,image=f_s_canvas.image, anchor="nw")
        f_s_canvas.place(x=550,y=430)

        # # MoneyBack 
        moneyback = Image.open(LOCATION+"moneyback.jpg")

        f_s_canvas = Canvas(order_frame,width=227,height=52, highlightthickness=0)

        resizing = moneyback.resize((227,52), Image.ANTIALIAS)
        
        f_s_canvas.image = ImageTk.PhotoImage(resizing)
        f_s_canvas.create_image(0,0,image=f_s_canvas.image, anchor="nw")
        f_s_canvas.place(x=550,y=490)


        # LABELS

        title.config(text=product_details[0][1])

        desc.config(text=f"{product_details[0][2]}\n")

        Label(order_frame, text=f"Estimated Delivery Day will be sent to \n", font=font_applied, bg="White").place(x=530,y=180)

        eml.config(text=em)
        
        pr.config(text=f"Price : \t ${product_details[0][5]}")

        qu= Label(order_frame, text=f"Quantity", font=font_applied, bg="White")
        qu.place(x=530,y=330)

        # Entry for order quantities
        order_quantity = customtkinter.CTkEntry(order_frame, placeholder_text=f"{product_details[0][6]} Left", fg_color="White", text_color="Black")
        order_quantity.place(x=646,y=330)


        # Place an Order.
        ordernow = customtkinter.CTkButton(order_frame, text="Order Now", font=NEW_FONT, fg_color="Black", command=order)
        ordernow.place(x=550,y=380,width=245,height=35)

      # FRAME
      global order_frame
      order_frame = Frame(user_dash,background="White", highlightthickness=0)
      order_frame.place(x=300,y=0, width=980,height=615)
      

      # LABELS
      ourproduct = customtkinter.CTkLabel(order_frame,text="Our Products", font=NEW_FONT,text_color="Black")
      ourproduct.place(x=200,y=16.5)


      # ANOTHER LABELS.
              # PRODUCT NAME.

      title= Label(order_frame, text=f"", font=font_applied, bg="White")
      title.place(x=530,y=80)

      desc= Label(order_frame, text=f"", font=font_applied, bg="White")
      desc.place(x=530,y=130)

      eml = Label(order_frame, text=f"", font=font_applied, bg="White")
      eml.place(x=530,y=230)
        
      pr= Label(order_frame, text=f"", font=font_applied, bg="White")
      pr.place(x=530,y=280)



      # COMBOBOX
      product_chosed = StringVar()
      product_chosed.set('Choose Your Product')
      product_list = ttk.Combobox(order_frame, textvariable=product_chosed, values=[each_product[1] for each_product in query.execute(f'SELECT * FROM {PRODUCT_TABLENAME}').fetchall()])
      product_list.place(x=350,y=16.5,width=250,height=25)

      # ENTRIES


      # BUTTONS
      search_for_product = customtkinter.CTkButton(order_frame,text="Search", text_color="White", width=150,height=32,font=btn_font,fg_color="Black", command=return_product)
      search_for_product.place(x=640, y=13.5)

    def contact_us():

      def submit_request():   #customer service request
        name= username_entry.get()
        email = email_entry.get()
        message_sent = f"""
        
        Customer Name : {name}
        Customer Email : {email}
        
        {msg_sent.get("1.0",END)}"""

        if len(name) == 0 or len(email) == 0 or len(message_sent) == 0:
          messagebox.showerror(title="Submit Error", message="Please fill out all the fields")
        else:
          if sendemail(ADMINEMAIL,message_sent, "Ticket"):
            messagebox.showinfo(title="Submit Message", message="Your Concern has been submitted successfully, our contact support will contact you as soon as possible.")
            username_entry.delete(0,END)
            email_entry.delete(0,END)
            msg_sent.delete("1.0",END)
          else:
            messagebox.showerror(title="Submit Message", message="An Error has occured while submitting your ticker. Please Try Again")
      

      try:
        order_frame.destroy()
      except Exception:
        pass
      
      # Frame
      global contact_frame
      contact_frame = Frame(user_dash, background="White")
      contact_frame.place(x=300,y=0,width=980,height=618)

      # Labels;
      msgs = customtkinter.CTkLabel(contact_frame, text="Submit Your Request", text_color="Black", font=TITLE)
      msgs.pack()
      user_name = customtkinter.CTkLabel(contact_frame, text="Full Name", text_color="Black", font=font_applied)
      user_name.place(x=50, y=80)

      em_sent = customtkinter.CTkLabel(contact_frame, text="Email", text_color="Black", font=font_applied)
      em_sent.place(x=385, y=80)

      comment = customtkinter.CTkLabel(contact_frame, text="Message", text_color="Black", font=font_applied)
      comment.place(x=48, y=140)
    
      # Entries:
      username_entry = customtkinter.CTkEntry(contact_frame, placeholder_text="Enter your Name", width=200,fg_color="White", text_color="Black")
      username_entry.place(x=175,y=80)

      email_entry = customtkinter.CTkEntry(contact_frame, placeholder_text="Enter your Email", width=310,fg_color="White", text_color="Black")
      email_entry.place(x=505,y=80)


      msg_sent = Text(contact_frame, bg="White")
      msg_sent.place(x=175,y=145,width=615,height=150)

      # Buttons
      submit = customtkinter.CTkButton(contact_frame,text="Submit", text_color="White", width=150,height=32,font=btn_font,fg_color="Black", command=submit_request)
      submit.place(x=70, y=315)

    
    def mysettings():
      
      def edit_account():
        fn = fullname.get()
        user_mail = email.get()
        passwrd = password.get()
        phonenumber = ph_num.get()
        if len(fn) == 0 or len(user_mail) == 0 or len(phonenumber) == 0:
          messagebox.showerror(title="Edit Account Error", message="PLease Fill out all the fields")
        elif len(passwrd) == 0:
          query.execute(f"""UPDATE User SET FullName = (?), Email = (?), Phonenumber = (?) WHERE ID = (?)""",(fn,user_mail,phonenumber,user_details[0][0]))
          messagebox.showinfo(title="Database Message", message="Your Account has been successfully edited.")
          database.commit()
          fullname.delete(0,END)
          email.delete(0,END)
          password.delete(0,END)
          ph_num.delete(0,END)
        else:
          query.execute(f"""UPDATE User SET FullName = ?, Email = ?,Password = ?,Phonenumber = ? WHERE ID = ?""",(fn,user_mail,hashlib.sha1(str(passwrd).encode()).hexdigest(),phonenumber,user_details[0][0]))
          database.commit()
          messagebox.showinfo(title="Database Message", message="Your Account has been successfully edited.")
          fullname.delete(0,END)
          email.delete(0,END)
          password.delete(0,END)
          ph_num.delete(0,END)
      
      try:
        contact_frame.destroy()
        order_frame.destroy()
      except Exception:
        pass
      

      # We will query all user details here using the Email
      user_details= [user_data for user_data in query.execute(f'SELECT * FROM {SQL_TABLENAME} WHERE Email= (?)', (em,)).fetchall()]
      # Frame
      user_setting_frame = Frame(user_dash, bg='White')
      user_setting_frame.place(x=300, y=0, width=980, height=618)

      Label(user_setting_frame, text="User Details", font=TITLE, bg="White").pack()

      # LABELS
      Label(user_setting_frame, text="Full Name", font=font_applied, bg="white").place(x=100, y=80)
      Label(user_setting_frame, text="Email", font=font_applied, bg="white").place(x=100, y=130)
      Label(user_setting_frame, text="Password", font=font_applied, bg="white").place(x=100, y=180)
      Label(user_setting_frame, text="Phone Number", font=font_applied, bg="white").place(x=100, y=230)

      # ENTRIES
      fullname =customtkinter.CTkEntry(user_setting_frame, width=350,fg_color="White", text_color="Black")
      fullname.place(x=380,y=80)
      fullname.insert(0,user_details[0][1])
      
      email =customtkinter.CTkEntry(user_setting_frame, width=350,fg_color="White", text_color="Black")
      email.place(x=380,y=130)
      email.insert(0,user_details[0][2])
      
      
      password =customtkinter.CTkEntry(user_setting_frame,placeholder_text="Enter your new password",width=350,fg_color="White", text_color="Black")
      password.place(x=380,y=180)


      ph_num =customtkinter.CTkEntry(user_setting_frame, width=350,fg_color="White", text_color="Black")
      ph_num.place(x=380,y=230)
      ph_num.insert(0,user_details[0][5])

      # BUTTONS
      edit_button = customtkinter.CTkButton(user_setting_frame,text="Edit Account",font=NEW_FONT,text_color="White", fg_color="Black", command=edit_account)
      edit_button.place(x=200,y=300,width=180 , height=45)
      cancel_edit = customtkinter.CTkButton(user_setting_frame,text="Cancel Process",font=NEW_FONT,text_color="White", fg_color="Black")
      cancel_edit.place(x=400,y=300,width=180 , height=45)

    # QUITTING FUNCTION.
    def user_quit():
      if messagebox.askokcancel(title="Quit Message", message="Are you sure you want to quit"):
        user_dash.destroy()


    global user_dash 
    
    user_dash=Tk()
    user_dash.title('User Area')
    user_dash.config(bg="white")
    user_dash.minsize(1300,635)
    user_dash.maxsize(1300,635)
    user_dash.iconbitmap(LOCATION+"user_design.ico")

    # FRAME that contains all the Buttons (Add , Edit ,Delete, Search)
    all_actions = Frame(user_dash,width=275,height=650,bg="#efbbff")
    all_actions.place(x=0,y=0)


    # LABEL
    Label(all_actions,text=f"Welcome {str(us).title()}", font=INPUT , bg="#efbbff" , fg="White").place(x=15,y=10)
    
    
    # Buttons :

    place_order = customtkinter.CTkButton(all_actions,text="Place an Order",text_color="Black" ,font=NEW_FONT,fg_color="White", command=place_an_order)
    place_order.place(x=15,y=70 , width=250 , height=50)
    track_order = customtkinter.CTkButton(all_actions,text="Contact Us",text_color="Black",font=NEW_FONT, fg_color="white", command=contact_us)
    track_order.place(x=15,y=130,width=250 , height=50)
    Contact_support = customtkinter.CTkButton(all_actions,text="My Account",font=NEW_FONT,text_color="Black", fg_color="white", command=mysettings)
    Contact_support.place(x=15,y=190,width=250 , height=50)
    My_Account = customtkinter.CTkButton(all_actions,text="Quit",text_color="Black",font=NEW_FONT, fg_color="white", command=user_quit)
    My_Account.place(x=15,y=250,width=250 , height=50)

    user_dash.mainloop()


  # THIS PART IS ONLY FOR ADMIN<

  def add_product():

    def reset_all_entries():
      product_infos.delete(0,END)
      product_category.delete(0,END)
      product_description.delete(0,END)
      product_price.delete(0,END)
      product_quantity.delete(0,END)
      product_size.delete(0,END)
      product_image.delete(0,END)

    def add():
      # saving all the data in variables.
      name = product_infos.get()
      description = product_description.get()
      category = product_category.get()
      size= product_size.get()
      price = product_price.get()
      quantity = product_quantity.get()
      img = product_image.get()

      counter =0
      # Testing those variables.
      if len(name)==0 or len(description)==0 or len(category) == 0 or len(size) == 0 or len(price) == 0 or len(quantity) == 0 or len(img) == 0:
        messagebox.showerror(title="Input Error" , message="Please fill out all the fields")
      else:
        #  THIS SQL QUERY WILL INSERT ALL THE PRODUCT DETAILS IN THE DATABASE , AND THE PRODUCT WILL  BE INCREMENTED.
         data= [
          (name,description,category,size,price,quantity,img)
         ]
         if query.executemany(f'INSERT INTO {PRODUCT_TABLENAME} (Name, Description, Category,Size,Price, Quantity,product_image) VALUES(?,?,?,?,?,?,?)', data):
            messagebox.showinfo(title="Database Confirmation" , message="This product is added successfully to the database.")
            database.commit()
            if counter %2 ==0:
              tree.insert("" ,"end",tags=('evenrow'), values=(name,description,category,size,price,quantity,img))
            else:  
              tree.insert("" ,"end",tags=('evenodd'), values=(name,description,category,size,price,quantity,img))
            reset_all_entries()
         else:
          messagebox.showerror(title="Database Error", message="Database insert error, please re-fill the fields and pay attention to the input type")
         counter+=1


    try:
      edit_frame.destroy()
      table_frame.destroy()
      customsearch_frame.destroy()
      ord_full_frame.destroy()    
    except Exception:
      pass


    global frame_area
    frame_area = Frame(bg="white",highlightthickness=0,background="white")
    frame_area.place(x=300,y=0,width=1000,height=590)

    # Label
    Label(frame_area,text="Product information", font=TITLE , bg="white" , fg="#06283D").place(x=400,y=10)
    Label(frame_area,text="Product Name",font=font_applied,bg="white",fg="#06283D").place(x=10,y=70)
    Label(frame_area,text="Product Description",font=font_applied,bg="white",fg="#06283D").place(x=10,y=120)
    Label(frame_area,text="Product Category",font=font_applied,bg="white",fg="#06283D").place(x=10,y=170)
    Label(frame_area,text="Product Size ",font=font_applied,bg="white",fg="#06283D").place(x=525,y=170)
    Label(frame_area,text="Product Price",font=font_applied,bg="white",fg="#06283D").place(x=10,y=220)
    Label(frame_area,text="Quantity",font=font_applied,bg="white",fg="#06283D").place(x=525,y=220)
    Label(frame_area,text="Product Image",font=font_applied,bg="white",fg="#06283D").place(x=10,y=270)



    # Entries:
    product_infos = customtkinter.CTkEntry(master=frame_area, width=600, placeholder_text="Enter the Name of the Product",fg_color="white", height=35, 
    text_color="Black")
    product_infos.place(x=210, y=70)
    product_description = customtkinter.CTkEntry(master=frame_area, width=600, placeholder_text="Enter the Description of the Product",fg_color="white", height=35, 
    text_color="Black")
    product_description.place(x=210, y=120)
    product_category = customtkinter.CTkEntry(master=frame_area, width=300, placeholder_text="Enter the category of the Product",fg_color="white", height=35, 
    text_color="Black")
    product_category.place(x=210, y=170)
    product_size = customtkinter.CTkEntry(master=frame_area, width=300, placeholder_text="Product Size",fg_color="white", height=35, text_color="Black")
    product_size.place(x=670, y=170)
    product_price = customtkinter.CTkEntry(master=frame_area, width=300, placeholder_text="$",fg_color="white", height=35, text_color="Black")
    product_price.place(x=210, y=220)
    product_quantity = customtkinter.CTkEntry(master=frame_area, width=300, placeholder_text="Product Quantity",fg_color="white", height=35, text_color="Black")
    product_quantity.place(x=670, y=220)
    product_image = customtkinter.CTkEntry(master=frame_area, width=300, placeholder_text="Imagename.extension",fg_color="white", height=35, text_color="Black")
    product_image.place(x=210, y=270)


    # TABLEVIEW

    tree_frame = Frame(frame_area, bg="#DFF6FF")
    tree_frame.place(x=0,y=325,width=980, height=220)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT , fill=Y)

    tree =ttk.Treeview(tree_frame,  columns = ("Name" , "Description" , "Category" , "Size" ,"Price" ,"Quantity","Image"))
    tree.place(x=0,y=0,width=965, height=220)
    tree_scroll.config(command=tree.yview)
    style_tree(tree)
    tree.column ( "#0", width = 0,minwidth=0,stretch=False) 
    tree.column ( "#1", width = 50 , anchor = "center"  )
    tree.column ( "#2" , width = 200 , anchor = "center" )
    tree.column ( "#3" , width = 50 , anchor = "center" )
    tree.column ( "#4" , width = 25 , anchor = "center" )
    tree.column ( "#5" , width = 25 , anchor = "center" )
    tree.column ( "#6" , width = 25 , anchor = "center" )
    tree.column ( "#7" , width = 25 , anchor = "center" )

    tree.heading ( "#1" , text = "Nom" , anchor = "center" )
    tree.heading ( "#2" , text = "Description" , anchor = "center" )
    tree.heading ( "#3" , text = "Category" , anchor = "center" )
    tree.heading ( "#4" , text = "Size" , anchor = "center" )
    tree.heading ( "#5" , text = "Price" , anchor = "center" )
    tree.heading ( "#6" , text = "Quantity" , anchor = "center" )
    tree.heading ( "#7" , text = "Image" , anchor = "center" )


    # BUTTON:
    Add= customtkinter.CTkButton(frame_area,text="Add Product", text_color="White", width=150,height=40,font=btn_font, command=add)
    Add.place(x=795, y=550)

    
  def edit_product():

    def reset_all_entries():
      # THIS FUNCTION WILL RESET ALL THE ENTRIES.
      product_infos.delete(0,END)
      product_description.delete(0,END)
      product_category.delete(0,END)
      product_size.delete(0,END)
      product_price.delete(0,END)
      product_quantity.delete(0,END)


    def search_for_product():
      # THIS FUNCTION WILL SEARCH FOR A CERTAIN PRODUCT
      # grab the product id.
      reset_all_entries()
      global product_id
      product_id = str(product_chosed.get()).split('/')[0].strip()
      for product_details in query.execute(f"SELECT * FROM {PRODUCT_TABLENAME} WHERE ID= (?)" , (product_id,)).fetchall():
          product_infos.insert(0, product_details[1])
          product_description.insert(0, product_details[2])
          product_category.insert(0, product_details[3])
          product_size.insert(0, product_details[4])
          product_price.insert(0, product_details[5])
          product_quantity.insert(0, product_details[6])

    def editing_process():
      # saving all data
      edit_counter = 0 
      name = product_infos.get()
      description = product_description.get()
      category = product_category.get()
      size= product_size.get()
      price = product_price.get()
      quantity = product_quantity.get()

      # THIS SQL QUERY WILL UPDATE AN EXSISTING PRODUCT IN THE DATABASE
      if query.execute(f"""UPDATE Product SET Name = (?), Description = (?), Category = (?), Size = (?), Price = (?), Quantity = (?) WHERE ID = (?)""", (name,description,category,size,price,quantity,product_id)):
        database.commit()
        messagebox.showinfo(title="Database Confirmation" , message="The product details have been successfully updated in the database")
        reset_all_entries()
        for each_record in query.execute(f'SELECT * FROM {PRODUCT_TABLENAME} WHERE ID=(?)' ,(product_id,)):
          if edit_counter %2 ==0:
            tree.insert("" ,"end",tags=('evenrow'), values=(each_record[1],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))
          else:  
            tree.insert("" ,"end",tags=('evenodd'), values=(each_record[1],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))
      else:
        messagebox.showerror(title="Database Error" , message="Database Update Error.")
      edit_counter+=1
    
    def delete_product():
      product_information = str(product_chosed.get())
      if len(product_information) == 0:
        messagebox.showerror(title="Delete Error", message="Please Choose a product from the Combobox and then click on Delete")
      else:
        product_name = str(product_information.split('/')[1].strip())
        product_id = product_information.split('/')[0].strip()
        if messagebox.askokcancel(title="Delete confirmation", message=f'Are you sure you want to delete {product_name}'):
          if query.execute(f'DELETE FROM {PRODUCT_TABLENAME} WHERE ID=(?)' , (int(product_id),)):
            database.commit()
            product_chosed.set('')
            messagebox.showinfo(title="Database message", message=f"{product_information} has been deleted successfully from the database.")



    try:
      frame_area.destroy()
      table_frame.destroy()
      customsearch_frame.destroy()
      ord_full_frame.destroy()    
    except Exception:
      pass
      
    # creating a new frame;
    global edit_frame
    edit_frame = Frame(bg="white",highlightthickness=0,background="white")
    edit_frame.place(x=300,y=0,width=1000,height=590)

    Label(edit_frame,text="Edit Product", font=TITLE , bg="white" , fg="#06283D").place(x=400,y=10)

    Label(edit_frame, text="Product ID", font=font_applied,bg="white" , fg="#06283D").place(x=10, y=90)

    # Create a Combobox
    product_chosed = StringVar()
    p_values = [f'{str(each_p[0]) + "/" + each_p[1]}' for each_p in  query.execute("SELECT * FROM Product").fetchall()]
    p_combo =ttk.Combobox(edit_frame , textvariable=product_chosed ,values=p_values)
    p_combo.place(x=210,y=92.5,width=250, height=25)

    # # Label
    Label(edit_frame,text="Product Name",font=font_applied,bg="white",fg="#06283D").place(x=10,y=152)
    Label(edit_frame,text="Product Description",font=font_applied,bg="white",fg="#06283D").place(x=10,y=200)
    Label(edit_frame,text="Product Category",font=font_applied,bg="white",fg="#06283D").place(x=10,y=250)
    Label(edit_frame,text="Product Size ",font=font_applied,bg="white",fg="#06283D").place(x=525,y=250)
    Label(edit_frame,text="Product Price",font=font_applied,bg="white",fg="#06283D").place(x=10,y=300)
    Label(edit_frame,text="Quantity",font=font_applied,bg="white",fg="#06283D").place(x=525,y=300)



    # # Entries:
    product_infos = customtkinter.CTkEntry(master=edit_frame, width=600,fg_color="white", height=35, 
    text_color="Black")
    product_infos.place(x=210, y=150)
    product_description = customtkinter.CTkEntry(master=edit_frame, width=600,fg_color="white", height=35,
    text_color="Black")
    product_description.place(x=210, y=200)
    product_category = customtkinter.CTkEntry(master=edit_frame, width=300,fg_color="white", height=35, 
    text_color="Black")
    product_category.place(x=210, y=250)
    product_size = customtkinter.CTkEntry(master=edit_frame, width=300,fg_color="white", height=35, text_color="Black")
    product_size.place(x=670, y=250)
    product_price = customtkinter.CTkEntry(master=edit_frame, width=300,fg_color="white", height=35, text_color="Black")
    product_price.place(x=210, y=300)
    product_quantity = customtkinter.CTkEntry(master=edit_frame, width=300,fg_color="white", height=35, text_color="Black")
    product_quantity.place(x=670, y=300)


    # TABLEVIEW

    # Create the scrollbar
    tree_frame = Frame(edit_frame)
    tree_frame.place(x=0,y=425,width=980, height=160)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT , fill=Y)

    tree =ttk.Treeview(tree_frame,  columns = ("Name" , "Description" , "Category" , "Size" ,"Price" ,"Quantity"))
    tree_scroll.config(command=tree.yview)
    tree.place(x=0,y=0,width=965, height=160)
    style_tree(tree)
    tree.column ( "#0", width = 0,minwidth=0,stretch=False) 
    tree.column ( "#1", width = 50 , anchor = "center"  )
    tree.column ( "#2" , width = 200 , anchor = "center" )
    tree.column ( "#3" , width = 50 , anchor = "center" )
    tree.column ( "#4" , width = 50 , anchor = "center" )
    tree.column ( "#5" , width = 50 , anchor = "center" )
    tree.column ( "#6" , width = 50 , anchor = "center" )

    tree.heading ( "#1" , text = "Nom" , anchor = "center" )
    tree.heading ( "#2" , text = "Description" , anchor = "center" )
    tree.heading ( "#3" , text = "Category" , anchor = "center" )
    tree.heading ( "#4" , text = "Size" , anchor = "center" )
    tree.heading ( "#5" , text = "Price" , anchor = "center" )
    tree.heading ( "#6" , text = "Quantity" , anchor = "center" )

    # Buttons:
    search = customtkinter.CTkButton(edit_frame,text="Search Product", text_color="White", width=150,height=40,font=btn_font, command=search_for_product)
    search.place(x=520, y=85)
    
    edit = customtkinter.CTkButton(edit_frame,text="Edit Product", text_color="White", width=150,height=40,font=btn_font, command=editing_process)
    edit.place(x=10, y=355)
    
    delete = customtkinter.CTkButton(edit_frame,text="Delete Product", text_color="White", width=150,height=40,font=btn_font, command=delete_product)
    delete.place(x=175, y=355)


  def quit():
    if messagebox.askokcancel(title="Quitter" , message="Are you sure you want to quit the App"):
      database.close()
      dashbord.destroy()


  def all_products():
    
    try:
      edit_frame.destroy()
      frame_area.destroy()
      customsearch_frame.destroy()
      ord_full_frame.destroy()    
    except Exception:
      pass
    
    global table_frame

    # CREATING A FRAME WHERE ALL THE LABELS, ENTRIES, TABLEVIEW Will be.
    table_frame = Frame(bg="white",highlightthickness=0,background="#DFF6FF")
    table_frame.place(x=300,y=35,width=1000,height=590)

    # CREATING A  SCROLLBAR.
    tree_scroll = Scrollbar(table_frame)
    tree_scroll.pack(side=RIGHT , fill=Y)

    tree =ttk.Treeview(table_frame,  columns = ("Name" , "Description" , "Category" , "Size" ,"Price" ,"Quantity"))
    tree_scroll.config(command=tree.yview)
    tree.place(x=0,y=0,width=980, height=590)

    # THIS FUNCTION WILL STYLE THIS TABLEVIEW
    style_tree(tree)

    tree.column ( "#0", width = 0,minwidth=0,stretch=False) 
    tree.column ( "#1", width = 50 , anchor = "center"  )
    tree.column ( "#2" , width = 200 , anchor = "center" )
    tree.column ( "#3" , width = 50 , anchor = "center" )
    tree.column ( "#4" , width = 50 , anchor = "center" )
    tree.column ( "#5" , width = 50 , anchor = "center" )
    tree.column ( "#6" , width = 50 , anchor = "center" )

    tree.heading ( "#1" , text = "Nom" , anchor = "center" )
    tree.heading ( "#2" , text = "Description" , anchor = "center" )
    tree.heading ( "#3" , text = "Category" , anchor = "center" )
    tree.heading ( "#4" , text = "Size" , anchor = "center" )
    tree.heading ( "#5" , text = "Price" , anchor = "center" )
    tree.heading ( "#6" , text = "Quantity" , anchor = "center" )


    # THIS LOOP WILL DISPLAY ALL THE PRODUCTS IN THE TABLEVIEW
    counter = 0
    for each_record in query.execute(f'SELECT * FROM {PRODUCT_TABLENAME}').fetchall():
        if counter %2 ==0:
            tree.insert("" ,"end",tags=('evenrow'), values=(each_record[1],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))
        else:  
            tree.insert("" ,"end",tags=('evenodd'), values=(each_record[1],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))
    counter+=1


  def custom_search():

    def retrieve():
      
      # Deleting all the rows in the TableView
      for each_r in tree.get_children():
        tree.delete(each_r)

      # Grabbing both the values.
      option= filter_option.get()
      value = value_entry.get()


      if option == "ID":
          # This SQL QUERY will return all the Product details about an ID given in the Entrie
          # If the provided ID is not found in the database, the list of emails will be empty. This is why an if statement is used to check the length of the list.
          retrieve_by_id = query.execute(f'SELECT * FROM {PRODUCT_TABLENAME} WHERE ID=(?)' , (value,)).fetchall()
          if len(retrieve_by_id) == 0:
              messagebox.showerror(title="Database Error", message="ID not found in the database")
              value_entry.delete(0,END)
          else:
            for each_record in retrieve_by_id :
              tree.insert("" ,"end",tags=('evenrow'), values=(each_record[0],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))
      
      elif option == "Quantity":
          # This SQL QUERY will return all the Product details about a Quantity given given in the Entrie
          # If the provided ID is not found in the database, the list of emails will be empty. This is why an if statement is used to check the length of the list.
          retrieve_by_quantity = query.execute(f'SELECT * FROM {PRODUCT_TABLENAME} WHERE Quantity=(?)' , (value,)).fetchall() 
          if len(retrieve_by_quantity) == 0:
              messagebox.showerror(title="Database Error", message="Category value not found in the database")
              value_entry.delete(0,END)
          else:
            for each_record in query.execute(f'SELECT * FROM {PRODUCT_TABLENAME} WHERE Quantity=(?)' , (value,)).fetchall():
                tree.insert("" ,"end",tags=('evenrow'), values=(each_record[0],each_record[2], each_record[3], each_record[4], each_record[5],each_record[6]))

    try: 
      frame_area.destroy()
      table_frame.destroy()
      edit_frame.destroy()
      ord_full_frame.destroy()
    except Exception:
      pass


    # Frame
    global customsearch_frame
    customsearch_frame =  Frame(bg="white",highlightthickness=0,background="white")
    customsearch_frame.place(x=300,y=35,width=1000,height=590)

    # Creating the Labels.
    Label(customsearch_frame,text="Filter By", font=INPUT , bg="white" , fg="#06283D").place(x=100,y=12)

    # Creating a Combobox that contains the retrieving options (ID, Category)
    filter_option = StringVar()
    filter_option.set('Choose your filter option')
    p_values = ["ID", "Quantity"]
    p_combo =ttk.Combobox(customsearch_frame,textvariable=filter_option ,values=p_values)
    p_combo.place(x=215,y=16,width=250, height=25)

    # ENTRIES.
    value_entry = customtkinter.CTkEntry(customsearch_frame, width=150, placeholder_text="Enter the Value",fg_color="white", height=30, 
    text_color="Black")
    value_entry.place(x=500,y=13.5)

    # BUTTONS:
    search= customtkinter.CTkButton(customsearch_frame,text="Search", text_color="White", width=150,height=32,font=btn_font, command=retrieve)
    search.place(x=675, y=13.5)



    # TABLEVIEW.
    tree_scroll = Scrollbar(customsearch_frame)
    tree_scroll.pack(side=RIGHT , fill=Y)

    tree =ttk.Treeview(customsearch_frame,  columns = ("Name" , "Description" , "Category" , "Size" ,"Price" ,"Quantity"))
    tree_scroll.config(command=tree.yview)
    tree.place(x=0,y=100,width=980, height=490)
    style_tree(tree)
    tree.column ( "#0", width = 0,minwidth=0,stretch=False) 
    tree.column ( "#1", width = 50 , anchor = "center"  )
    tree.column ( "#2" , width = 200 , anchor = "center" )
    tree.column ( "#3" , width = 50 , anchor = "center" )
    tree.column ( "#4" , width = 50 , anchor = "center" )
    tree.column ( "#5" , width = 50 , anchor = "center" )
    tree.column ( "#6" , width = 50 , anchor = "center" )

    tree.heading ( "#1" , text = "Nom" , anchor = "center" )
    tree.heading ( "#2" , text = "Description" , anchor = "center" )
    tree.heading ( "#3" , text = "Category" , anchor = "center" )
    tree.heading ( "#4" , text = "Size" , anchor = "center" )
    tree.heading ( "#5" , text = "Price" , anchor = "center" )
    tree.heading ( "#6" , text = "Quantity" , anchor = "center" )
    
  def ord_full():
    
    def edit_fullfilement():
      # Grabing the product here
      product_fulfilled=int(str(products_not_fulfiled.get().split('/')[0]))
      
      # This SQL QUERY will change the False to True value once the user choose an order fullfiled and click on the button
      if query.execute(f"UPDATE {ORDERTABLE} SET Fullfiled = (?) WHERE Order_ID = (?)", ("True",product_fulfilled,)):
        database.commit()
        messagebox.showinfo(title="Order Notification", message="The Order has been Fullfiled successfully")
        query_all_orders()
      else:
        messagebox.showinfo(title="Order Notification", message="Database Update Error Please try Again.")
      

    def query_all_orders():
      # All Orders 
      for each_record in tree.get_children():
        tree.delete(each_record)

      global All_orders
      All_orders = [each_order for each_order in query.execute(f'SELECT * FROM {ORDERTABLE}').fetchall()]
      for each_ord in All_orders:
        tree.insert("" ,"end",tags=('evenrow'), values=(each_ord[0],each_ord[1], each_ord[2], each_ord[3], each_ord[4], each_ord[5]))
    
    try:
      frame_area.destroy()
      table_frame.destroy()
      edit_frame.destroy()
      customsearch_frame.destroy()
    except Exception:
      pass


    # Creating a Frame.
    global ord_full_frame
    ord_full_frame = Frame(bg="white",highlightthickness=0,background="white")
    ord_full_frame.place(x=300,y=35,width=1000,height=590)

    # Labels:
    order_label = customtkinter.CTkLabel(ord_full_frame, text="Order Fullfiled", text_color="Black", bg_color="White", font=INPUT)
    order_label.place(x=100, y=20)

    # Combobox
    products_not_fulfiled = StringVar()
    products_not_fulfiled.set('Choose the order Id')
    p_values = [f"{str(each_ord[0])}/{each_ord[4]}" for each_ord in query.execute(f'SELECT * FROM {ORDERTABLE}').fetchall()]
    p_combo =ttk.Combobox(ord_full_frame,textvariable=products_not_fulfiled ,values=p_values)
    p_combo.place(x=290,y=19,width=250, height=25)


    # Buttons
    fullfil_buttons= customtkinter.CTkButton(ord_full_frame, text="Fulfilled", font=NEW_FONT, fg_color="Black", command=edit_fullfilement)
    fullfil_buttons.place(x=580,y=14.5,width=150,height=35)

    # TABLEVIEW.

    tab_frame= Frame(ord_full_frame, highlightthickness=0, background="White")
    tab_frame.place(x=10,y=75,width=980,height=490)

    tree_scroll = Scrollbar(tab_frame)
    tree_scroll.pack(side=RIGHT , fill=Y)

    tree =ttk.Treeview(tab_frame,  columns = ("Order Id" , "Product" , "Price charged" , "Quantity","Customer_details" ,"Fulfilled"))
    # tree_scroll.config(command=tree.yview)
    tree.place(x=0,y=0,width=965, height=490)
    style_tree(tree)
    tree.column ( "#0", width = 0,minwidth=0,stretch=False) 
    tree.column ( "#1", width = 50 , anchor = "center"  )
    tree.column ( "#2" , width = 150 , anchor = "center" )
    tree.column ( "#3" , width = 50 , anchor = "center" )
    tree.column ( "#4" , width = 50 , anchor = "center" )
    tree.column ( "#5" , width = 150 , anchor = "center" )
    tree.column ( "#6" , width = 50 , anchor = "center" )

    tree.heading ( "#1" , text = "Order Id" , anchor = "center" )
    tree.heading ( "#2" , text = "Product" , anchor = "center" )
    tree.heading ( "#3" , text = "Price charged" , anchor = "center" )
    tree.heading ( "#4" , text = "Quantity" , anchor = "center" )
    tree.heading ( "#5" , text = "Customer Details" , anchor = "center" )
    tree.heading ( "#6" , text = "Fulfilled" , anchor = "center" )

    query_all_orders()


  def Dashboard():
    
    # The reason why the dahsboard variable is global is because we will destroy it when the user clicks on QUIT function
    global dashbord 
    
    dashbord=Tk()
    dashbord.title('DASHBOARD')
    dashbord.config(bg="white")
    dashbord.minsize(1300,635)
    dashbord.maxsize(1300,635)
    dashbord.iconbitmap(f"{LOCATION}admin.ico")

    # FRAME that contains all the Buttons (Add , Edit ,Delete, Search)
    all_actions = Frame(dashbord,width=280,height=650,bg="#efbbff")
    all_actions.place(x=0,y=0)


    # LABEL
    Label(all_actions,text="ADMIN DASHBOARD", font=INPUT , bg="#efbbff" , fg="Black").place(x=45,y=10)
    
    
    # Buttons :

    add_button = customtkinter.CTkButton(all_actions,text="Add Product",text_color="Black" ,font=NEW_FONT,command=add_product,fg_color="White")
    add_button.place(x=15,y=70 , width=250 , height=50)
    edit_del_button = customtkinter.CTkButton(all_actions,text="Edit/Delete Product",text_color="Black",font=NEW_FONT, fg_color="white", command=edit_product)
    edit_del_button.place(x=15,y=130,width=250 , height=50)
    all_product_button = customtkinter.CTkButton(all_actions,text="All Products",font=NEW_FONT,text_color="Black", fg_color="white", command=all_products)
    all_product_button.place(x=15,y=190,width=250 , height=50)
    custom_search_button= customtkinter.CTkButton(all_actions,text="Custom Search",text_color="Black",font=NEW_FONT, fg_color="white", command=custom_search)
    custom_search_button.place(x=15,y=250,width=250 , height=50)
    or_fullfilement = customtkinter.CTkButton(all_actions,text="Order Fullfilement",text_color="Black",font=NEW_FONT, fg_color="white", command=ord_full)
    or_fullfilement.place(x=15,y=310,width=250 , height=50)
    quit_button = customtkinter.CTkButton(all_actions,text="Quit",text_color="Black",font=NEW_FONT, fg_color="white", command=quit)
    quit_button.place(x=15,y=370,width=250 , height=50)

    dashbord.mainloop()

  def log_in():
    
    # Retrieving the user's Gmail and password
    email = email_label.get()
    # Grabbing the user email and encrypting the password using SHA1.
    password = hashlib.sha1(str(password_label.get()).encode()).hexdigest()

    if email == ADMINEMAIL:  
      return_window = "ADMINAREA"
    else:
      return_window = "USERAREA"
    
    # Checking the database for a list of emails and determining whether the input email is present in this list
    all_emails = [each_r[2] for each_r in query.execute(f'SELECT * FROM {SQL_TABLENAME}').fetchall()]
    
    if email in all_emails:
        # Retrieving the user password and compare it with the user input 
        user_details = [user_data for user_data in query.execute(f'SELECT * FROM {SQL_TABLENAME} WHERE Email= (?)', (email,))]
        
        # If the passwords are the same
        if password == user_details[0][3].strip():
          
          # GENERATE A RANDOM NUMBER AND DO A SECURITY CHECK
          NUMBERS = "0123456789"
          random_number = "".join(random.sample(NUMBERS,5)) 
          # I have printed the random code just in case The Verification code didn't sent to the user email
          print(f"{BLUE} -> Number sent to this email {email} is {random_number}")
          message_sent = f"""
            Dear {user_details[0][1]},

            Thank you for signing up for our service. In order to complete your registration, we need to verify your email address. Please enter the following verification code when prompted:

            {random_number}

            If you have any trouble entering the code, please don't hesitate to contact us for assistance.

            Thank you for choosing our service.

            Best regards,
          """

          # This function will test if the email is valid and send a verification code
          if sendemail(email, message_sent, "Account Verification"):

           # this will ask the user for the code that has been sent to him  
           user_number_input = simpledialog.askstring(title="Email Verification",prompt=f"We ha Sent a verification code to {email}", parent=window)
           if user_number_input == random_number:
              email_label.delete(0,END)
              password_label.delete(0,END)
              window.destroy()
              # This is what separate the ADMIN ACCOUNT FROM THE USERACCOUNT
              if return_window == "ADMINAREA":
                Dashboard()
              elif return_window == "USERAREA":
                user_dahsboard(email, user_details[0][1])
           else:
              messagebox.showerror(title="Code Error" , message="The verification error you've entered is invalid")
    else:
            messagebox.showerror(title="Log In Error" , message="There is no account created using this email. Please create an account") 
            email_label.delete(0,END)
            password_label.delete(0,END)

  # ----------------------------------------------- CREATE ACCOUNT FUNCTION --------------------------------
  def create_account():


    def cancel_account():
      create.destroy()

    # getting all the data from the user and saving the date in the database.
    def save_account():
      user_fullname = full_name.get().lower()
      user_email = email.get()
      user_password = hashlib.sha1(str(password.get()).encode()).hexdigest()
      user_year = year.get()
      user_month = month.get()
      user_day = date.get()
      date_of_birth=f"{user_day}/{user_month}/{user_year}"
      user_phone_number = phone_number.get()
      # Here we will pop an error message if there is a field empty
      if len(user_fullname)==0 or len(user_email)==0 or len(user_password)==0 or user_year==0 or len(user_month)==0 or user_day==0 or user_phone_number=="":
        messagebox.showerror(title="Error !",message="Please Fill out All The Fields")
      else:
        emails = [each_record[2] for each_record in query.execute(f'SELECT * FROM {SQL_TABLENAME}')]
        if user_email in emails:
          messagebox.showerror(title="Technical Problem",message='Account already created using this Email. Please try to Log in')
        else:
          data = [
            (user_fullname,user_email,user_password,date_of_birth,user_phone_number)
          ]
          query.executemany(f"INSERT INTO {SQL_TABLENAME} ('FullName','Email','Password','DateOfBirth','PhoneNumber')  Values(?,?,?,?,?)",data)
          database.commit()
          create.destroy()
          user_auth(user_fullname , user_email , date_of_birth, LOCATION)

    






    create = Toplevel()
    create.title("Inventory Management System")
    create.minsize(500,520)
    create.maxsize(500,520)
    create.iconbitmap(VECTOR)
    create.config(bg="white")
    

    # TITLE
    Label(create, text="REGISTER", bg="white",fg="#57a1f8",font=TITLE).pack() 

    # Label Create New Account
    Label(create,text="Full Name",font=btn_font, bg="white").place(x=60,y=80)
    Label(create,text="Email",font=btn_font,bg="white").place(x=60,y=150)
    Label(create,text="Password",font=btn_font,bg="white").place(x=60,y=220)
    Label(create,text="Date Of Birth",font=btn_font,bg="white").place(x=60,y=290)
    Label(create,text="Phone Number",font=btn_font,bg="white").place(x=60,y=360)


    # Entries:

    full_name = customtkinter.CTkEntry(create,width=500,fg_color="White", text_color="Black")
    full_name.place(x=60,y=115,width=335)
    email = customtkinter.CTkEntry(create,width=500,fg_color="White", text_color="Black")
    email.place(x=60,y=185,width=335)
    password = customtkinter.CTkEntry(create,width=500,fg_color="White", text_color="Black")
    password.place(x=60,y=255,width=335)
    phone_number = customtkinter.CTkEntry(create,width=500,fg_color="White", text_color="Black")
    phone_number.place(x=60,y=395,width=335)

    # Combobox:
    # 1-date
    date = IntVar()
    date_values= [i for i in range(1,32)]
    date_numbers = ttk.Combobox(create, width = 10, textvariable = date, values=date_values)
    date_numbers.place(x=60,y=325)
    # 2-Month
    month = StringVar()
    month_values= ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month_numbers = ttk.Combobox(create, width = 10, textvariable = month, values=month_values)
    month_numbers.place(x=180,y=325)
    # 3-Year:
    year = IntVar()
    year_values= [i for i in range(2002,1905,-1)]
    year_numbers = ttk.Combobox(create, width = 10, textvariable = year , values=year_values)
    year_numbers.place(x=300,y=325)
  

    # BUTTONS
    save_account= customtkinter.CTkButton(create, text="Sign Up",text_color="White", width=150,height=40,font=btn_font, command=save_account)
    save_account.place(x=60,y=445,width=165)
    cancel_account= customtkinter.CTkButton(create, text="Cancel",text_color="White", width=150,height=40,font=btn_font, command=cancel_account)
    cancel_account.place(x=250,y=445,width=165)

  
  # Those functions are used to delete both "Enter your email" and "Eneter your password" when the user click on those entries
  def on_enter1(e):
    email_label.delete(0,'end')

  def on_leave1(e):
    login = email_label.get()
    if login == "":
      email_label.insert(0,"Enter your Email")
    
  # this for the password
  def on_enter2(e):
    password_label.delete(0,'end')
    password_label.config(show="*")

  def on_leave2(e):
    password = password_label.get()
    if password == "":
      password_label.insert(0,"Enter your password")
      password_label.config(show="")



  window = Tk()
  window.title("Inventory Management System")
  window.config(bg="white")
  window.minsize(1280,705)
  window.maxsize(1280,705)
  window.iconbitmap(VECTOR)

  # 1-> CREATING THE FRAME AND THE CANVAS SO WE CAN PUT THE DESIGN
  design = Image.open(GUI_DESIGN)

  gui_background = Canvas(window,width=1280,height=705)
  gui_background.image = ImageTk.PhotoImage(design)
  gui_background.create_image(0,0,image=gui_background.image, anchor=NW)
  gui_background.place(x=0,y=0)


  # LABELS
  Label(gui_background,text="Inventory Management System",fg="#57a1f8",bg="white",font=TITLE).place(x=80,y=150)

  # Entries
  email_label = Entry(gui_background,font=("Microsoft YaHei UI Light",14),bg="white",border=0,fg="black")
  email_label.place(x=100,y=240,width=335,height=32.5)
  email_label.insert(0,"Enter your Email")
  email_label.bind('<FocusIn>',on_enter1)
  email_label.bind('<FocusOut>',on_leave1)

  # Creating a black line that will be under the Entry
  Frame(gui_background,width=350,height=1,bg="black").place(x=100,y=285)

  password_label = Entry(gui_background,font=("Microsoft YaHei UI Light",14),bg="white",border=0,fg="black")
  password_label.place(x=100,y=320,width=335,height=32.5)
  password_label.insert(0,"Enter your password")
  password_label.bind('<FocusIn>',on_enter2)
  email_label.bind('<FocusOut>',on_leave2)
 
  Frame(gui_background,width=350,height=1,bg="black").place(x=100,y=365)


  # Label:
  Label(gui_background,text="Don't Have an Account ?",fg="black",bg="white",font=("Microsoft YaHei UI Light",14)).place(x=100,y=465)

  # Buttons:
  login = customtkinter.CTkButton(gui_background, text="Log in", font=NEW_FONT, command=log_in)
  login.place(x=115,y=400,width=300,height=35)
  Button(gui_background,text="Create One",font=("Microsoft YaHei UI Light",14),cursor="hand2",bg="white",fg="#57a1f8",border=0,width=9,   
  command=create_account).place(x=320,y=460)


  window.mainloop()


if __name__ == "__main__":
  try:
    GUI()
  except KeyboardInterrupt:
    sys.exit() 
