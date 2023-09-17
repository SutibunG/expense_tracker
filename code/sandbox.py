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

total_users_file = "data\\total_users.txt"
json_file = "data\\data.json"

with open(total_users_file, "r") as data_file:
    data = data_file.read()
    total_users = int(data)
    print(total_users)

#--------------------------UI------------------------------#
def login_screen():

    def signup():
        global total_users
        new_user = username_entry.get()
        new_pass = password_entry.get()
        valid_user = False

        new_user_data = {
            "User": {
                "Username": new_user,
                "ID": total_users,
                "Name": "",
                "Password": new_pass,
                }
        }

        try:
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
                print(read_data)

            #Username Checking
            if space_in_name == False and space_in_pass == False:
                if read_data["User"]["Username"].lower() == new_user.lower():
                    messagebox.showerror(title="Name Error", message=f"The username: {new_user} is already in use.\n Please enter another username.")
                elif len(new_user) < 4:
                    messagebox.showerror(title="Name Error", message=f"The username: {new_user} is too short.\n Please enter another username.")
                else: valid_user = True
            
            #If Valid Username
            if valid_user == True and len(new_pass) >= 4:
                is_ok = messagebox.askyesno(title="User Info", message=f"Username: {new_user}\nPassword: {new_pass}\n\nDoes this look correct?")

                #Adds +1 user and writes data to file
                if is_ok == True:
                    total_users += 1
                    with open(total_users_file, "w") as data_file:
                        data_file.write(f"{total_users}")
                        print(total_users)

                    with open(json_file, "w") as data:
                        json.dump(new_user_data, data, indent=3)
                    
                    username_entry.delete(0, END)
                    password_entry.delete(0, END)
            elif len(new_pass) < 4 and new_user != "":
                messagebox.showerror(title="Password Error", message="Please make sure password is atleast 4 characters long.")
            else:
                pass
        except:
            messagebox.showerror(title="Login Info", message="Please Enter Valid Username and Password.")

        
    def login():
        global logged_in
        username = username_entry.get()
        password = password_entry.get()
        valid_user = False
        valid_pass = False

        with open(json_file, "r") as data:
            read_data = json.load(data)
            if read_data["User"]["Username"] == username.title() or read_data["User"]["Username"] == username.lower():
                valid_user = True
            if read_data["User"]["Password"] == password:
                valid_pass = True

        if valid_pass == True and valid_user == True:
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


    #Window
    window = Tk()
    window.title("Expense Tracker")
    window.minsize(width=417, height=375)
    window.maxsize(width=450, height=400)
    window.config(bg=DARK_GREEN, padx=20, pady=10)
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
    window = Tk()
    window.title("Expense Tracker")
    window.minsize(width=417, height=525)
    window.config(bg=BEIGE, padx=20, pady=10)
    window.geometry("600x250")
    window.eval('tk::PlaceWindow . center')


    window.mainloop()

if __name__ == "__main__":
    login_screen()
    if logged_in == True:
        print("Loading")
        profile_screen()
