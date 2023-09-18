from tkinter import *
from tkinter import messagebox
import time
import json

FONT = ("Arial", 12, "bold")
BEIGE = "#FAF1E4"
SOFT_GREEN = "#CEDEBD"
MID_GREEN = "#9EB384"
DARK_GREEN = "#435334"
BRIGHT_GREEN = "#A2FF86"
logged_in = False
ID = None

total_users_file = "data\\total_users.txt"
json_file = "data\\data.json"

with open(total_users_file, "r") as data_file:
    data = data_file.read()
    total_users = int(data)

#--------------------------UI------------------------------#
def login_screen():

    def signup():
        global total_users
        new_user = username_entry.get()
        new_pass = password_entry.get()
        valid_user = False

        new_user_data = {
                    "Username": new_user,
                    "ID": total_users,
                    "Name": "",
                    "Password": new_pass,
                }

        #try:
            #Checks for space in username
        for i in new_user:
            if i == " ":
                messagebox.showerror(title="Name Error", message=f"The username: {new_user} cannot contain spaces.")
                space_in_name = True
                break
            else: space_in_name = False

        #Checks for space in password
        for i in new_pass:
            if i == " ":
                messagebox.showerror(title="Password Error", message=f"The password: {new_pass} cannot contain spaces.")
                space_in_pass = True
                break
            else: space_in_pass = False

        #Reads Data file
        with open(json_file, "r") as data:
            read_data = json.load(data)

        #Username Checking
        if space_in_name == False and space_in_pass == False:
            for user in read_data:
                valid_user = False
                if user["Username"].lower() == new_user.lower():
                    messagebox.showerror(title="Name Error", message=f"The username: {new_user} is already in use.\n Please enter another username.")
                    break
                elif len(new_user) < 4:
                    messagebox.showerror(title="Name Error", message=f"The username: {new_user} is too short.\n Please enter another username.")
                else: 
                    valid_user = True
        
        #If Valid Username
        if valid_user == True and len(new_pass) >= 4:
            is_ok = messagebox.askyesno(title="User Info", message=f"Username: {new_user}\nPassword: {new_pass}\n\nDoes this look correct?")

            if is_ok == True:
                #Reads and loads data into list
                with open(json_file, "r") as data:
                    read_data = json.load(data)
                    read_data.append(new_user_data)
                #Appends data to file
                with open(json_file, "w") as data:
                    json.dump(read_data, data, indent=4)
                #Gets the total users and tracks index
                with open(total_users_file, "w") as data_file:
                    data_file.write(str(len(read_data)))
                    print(len(read_data))
                
                username_entry.delete(0, END)
                password_entry.delete(0, END)
        elif len(new_pass) < 4 and new_user != "":
            messagebox.showerror(title="Password Error", message="Please make sure password is atleast 4 characters long.")
        else:
            pass
        #except:
            #messagebox.showerror(title="Login Info", message="Please Enter Valid Username and Password.")

        
    def login():
        global logged_in
        global ID
        username = username_entry.get()
        password = password_entry.get()
        valid_user = False
        valid_pass = False
        index = 0

        with open(json_file, "r") as data:
            read_data = json.load(data)
            for user in read_data:
                if user["Username"].title() == username.title() or user["Username"] == username.lower() and user["Password"] == password:
                    valid_user = True
                    break
                else:
                    #Returns ID
                    index += 1

        if valid_user == True:
            #Assigns ID
            ID = index
            print("Logged In")
            logged_in = True
            window.destroy()
        else:
            messagebox.showerror(title="Wrong Info", message="Please Enter Valid Username and Password.")


    def hide_view_password():
        check = check_state.get()

        if check == 0:
            password_entry.config(show="*")
        else:
            password_entry.config(show="")

    def exit_app():
        global is_on

        is_on = False
        window.destroy()

    def on_closing():
        global is_on

        if messagebox.askyesno("Quit", "Do you want to quit?"):
            is_on = False
            window.destroy()

    #Window
    window = Tk()
    window.title("Expense Tracker")
    window.minsize(width=417, height=375)
    window.maxsize(width=450, height=400)
    window.config(bg=DARK_GREEN, padx=20, pady=10)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.eval('tk::PlaceWindow . center')

    #Labels
    username_label = Label(text="Username: ", font=("Arial", 16), bg=DARK_GREEN)
    username_label.grid(column=1, row=2)
    password_label = Label(text="Password:", font=("Arial", 16), bg=DARK_GREEN)
    password_label.grid(column=1, row=3)
    empty_label = Label(text="",bg=DARK_GREEN)
    empty_label.grid(column=1, row=1)
    empty_label = Label(text="",bg=DARK_GREEN)
    empty_label.grid(column=1, row=4)

    #Buttons
    login_button = Button(text="Login", width=15, command=login, bg=BRIGHT_GREEN, font=FONT)
    login_button.config(pady=5)
    login_button.grid(column=1, row=5)
    signup_button = Button(text="Sign Up", width=15, command=signup, font=FONT, bg=BEIGE)
    signup_button.config(pady=5)
    signup_button.grid(column=2, row=5)
    exit_button = Button(text="Exit", width=15, command=exit_app, font=FONT, bg="red")
    exit_button.config(pady=5)
    exit_button.grid(column=3, row=5)

    #Entries
    username_entry = Entry(width=40)
    username_entry.grid(column=2, row=2)
    username_entry.focus()
    password_entry = Entry(show="*", width=40)
    password_entry.grid(column=2, row=3)

    #Radio Button
    check_state = IntVar()
    view_password = Checkbutton(text="Show Password",variable=check_state,onvalue=1, offvalue=0, command=hide_view_password)
    view_password.config(bg=DARK_GREEN)
    view_password.grid(column=3, row=3)

    #Canvas
    canvas = Canvas(width=400, height=150, bg=BEIGE, highlightbackground=SOFT_GREEN, highlightthickness=10)
    #bg_image = PhotoImage(file="C:\\Users\\Yungstaz\\Documents\\Projects\\Expense Tracker\\img\\login_screen.png")
    #canvas.create_image(208, 212, image=bg_image)
    canvas.create_text(208,75, text="Expense Tracker", fill=DARK_GREEN, font=("Impact", 40))
    canvas.grid(column=0, row=0, columnspan=4)

    window.mainloop()

def profile_screen():
    global ID

    with open(json_file, "r") as data:
        read_data = json.load(data)

        #Returns the users info
        current_user = read_data[ID]["Username"]

    def delete_account():
        global logged_in

        delete = messagebox.askyesno(title="Delete Account", message="Are you sure you want to delete your account?")

        if delete == True:
            with open(json_file, "r") as data:
                read_data = json.load(data)
                read_data.pop(ID)
            #Appends data to file
            with open(json_file, "w") as data:
                json.dump(read_data, data, indent=4)
            #Gets the total users and tracks index
            with open(total_users_file, "w") as data_file:
                data_file.write(str(len(read_data)))
                print(len(read_data))
            logged_in = False
            window.destroy()
        else:
            pass

    def log_out():
        global logged_in
        logged_in = False
        window.destroy()

    def on_closing():
        global is_on
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            is_on = False
            window.destroy()


    window = Tk()
    window.title("Expense Tracker")
    window.minsize(width=600, height=500)
    window.config(bg=BEIGE, padx=20, pady=10)
    window.geometry("600x250")
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.eval('tk::PlaceWindow . center')

    #Canvas
    canvas = Canvas(width=550, height=50, bg=BEIGE, highlightbackground=SOFT_GREEN, highlightthickness=5)
    #bg_image = PhotoImage(file="C:\\Users\\Yungstaz\\Documents\\Projects\\Expense Tracker\\img\\login_screen.png")
    #canvas.create_image(208, 212, image=bg_image)
    canvas.create_text(275,25, text=f"{current_user}".title(), fill=DARK_GREEN, font=("Impact", 20))
    canvas.grid(column=0, row=0, columnspan=4)

    #Buttons
    delete_button = Button(text="Delete Account", command=delete_account)
    delete_button.grid(column=0,row=1)

    log_out_button = Button(text="Log Out", command=log_out)
    log_out_button.grid(column=0,row=2)


    window.mainloop()

if __name__ == "__main__":
    is_on = True

    while is_on == True:
        if logged_in == False:
            login_screen()
        else:
            profile_screen()

