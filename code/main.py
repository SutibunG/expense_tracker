from tkinter import *
from tkinter import messagebox
from datetime import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import os
import pandas as pd
import time
import json

FONT = ("Arial", 12, "bold")
BEIGE = "#FAF1E4"
SOFT_GREEN = "#CEDEBD"
MID_GREEN = "#9EB384"
DARK_GREY = "#435334"
BRIGHT_GREEN = "#A2FF86"
BLUE = "#4F709C"
DARK_GREY = "#352F44"
DARK_GRAY = "#7D7C7C"
LIGHT_GREY = "#B4B4B3"
logged_in = False
ID = None
GOAL = None
month_text = datetime.now().strftime("%B")
MONTHS = ["January","February","March","April","May","June", "July","August","September","October","November","December"]

monthly_report = {
    "Date": [],
    "Month": [],
    "Paycheck": []
}

total_users_file = "data\\total_users.txt"
json_file = "data\\data.json"

with open(total_users_file, "r") as data_file:
    data = data_file.read()
    total_users = int(data)

#--------------------------Screens------------------------------#
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
                    "Goal": 0,
                }


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
        try:
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
                else:
                    valid_user = True
        except UnboundLocalError:
            messagebox.showerror(title="Wrong Info", message="Please Enter Valid Username and Password.")

        
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
                if user["Username"].title() == username.title() and user["Password"] == password:
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
            root.destroy()
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
        root.destroy()

    def on_closing():
        global is_on

        if messagebox.askyesno("Quit", "Do you want to quit?"):
            is_on = False
            root.destroy()

    #----------------------UI-------------------------#
    #Window
    root = Tk()
    root.title("Salary Tracker")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.eval('tk::PlaceWindow . center')
    root.minsize(width=450, height=500)
    root.maxsize(width=450, height=500)
    root.config(bg=DARK_GREY, padx=20, pady=10)

    #Labels
    username_label = Label(text="Username", font=("Impact", 16), bg=DARK_GREY, fg="white")
    username_label.grid(column=0, row=2)
    password_label = Label(text="Password", font=("Impact", 16), bg=DARK_GREY, fg="white")
    password_label.grid(column=0, row=5)
    empty_label = Label(text="",bg=DARK_GREY)
    empty_label.grid(column=1, row=1)
    empty_label = Label(text="",bg=DARK_GREY)
    empty_label.grid(column=1, row=8)

    #Buttons
    login_button = Button(text="Login", width=25, command=login, bg=BRIGHT_GREEN, font=FONT)
    login_button.config(pady=5)
    login_button.grid(column=0, row=9, columnspan=4)
    signup_button = Button(text="Sign Up", width=25, command=signup, font=FONT, bg=BEIGE)
    signup_button.config(pady=5)
    signup_button.grid(column=0, row=10, columnspan=4)
    exit_button = Button(text="Exit", width=25, command=exit_app, font=FONT, bg="red")
    exit_button.config(pady=5)

    #Entries
    username_entry = Entry(width=55)
    username_entry.grid(column=0, row=3, columnspan=4)
    username_entry.focus()
    password_entry = Entry(show="*", width=55)
    password_entry.grid(column=0, row=6, columnspan=4)

    #Radio Button
    check_state = IntVar()
    view_password = Checkbutton(text="Show Password",variable=check_state,onvalue=1, offvalue=0,fg="white", command=hide_view_password)
    view_password.config(bg=DARK_GREY)
    view_password.grid(column=0, row=7)

    #Canvas
    canvas = Canvas(width=400, height=150, bg=BEIGE, highlightbackground=BLUE, highlightthickness=10)
    canvas.create_text(208,75, text="Salary Tracker", fill=DARK_GREY, font=("Impact", 40))
    canvas.grid(column=0, row=0, columnspan=4)

    root.mainloop()

def profile_screen():
    global ID
    global GOAL

    with open(json_file, "r") as data:
        read_data = json.load(data)
        #Returns the users info
        current_user = read_data[ID]["Username"]
        user_goal = read_data[ID]["Goal"]


    data = pd.DataFrame(monthly_report)
    #Creates a data file for the User if doesn't have one
    if os.path.isfile(f"data\\{current_user}_data.csv"):
        pass
    else:
        data.to_csv(f"data\\{current_user}_data.csv", mode="a+", index=False)

    def log_out():
        global logged_in

        root.destroy()
        plt.close()
        logged_in = False
        print("Logged out")

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

            os.remove(f"data\\{current_user}_data.csv")
            root.destroy()
            plt.close()
        else:
            pass

    def on_closing():
        global is_on
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            is_on = False
            root.destroy()
            plt.close()

    def refresh_report():
        global current_salary
        global plot_canvas

        with open(json_file, "r") as data:
            read_data = json.load(data)
            #Updates color on bar chart
            user_goal = read_data[ID]["Goal"]

        plt.close()
        x = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sept","Oct","Nov","Dec"]
        y = []

        data = pd.read_csv(f"data\\{current_user}_data.csv")

        january = data[data["Month"] == "January"]
        february = data[data["Month"] == "February"]
        march = data[data["Month"] == "March"]
        april = data[data["Month"] == "April"]
        may = data[data["Month"] == "May"]
        june = data[data["Month"] == "June"]
        july = data[data["Month"] == "July"]
        august = data[data["Month"] == "August"]
        september = data[data["Month"] == "September"]
        october = data[data["Month"] == "October"]
        november = data[data["Month"] == "November"]
        december = data[data["Month"] == "December"]

        check = [january, february, march, april, may, june, july, august, september, october, november, december]

        current_salary = 0
        for i in range(0, 12):
            counter = 0
            for j in check[i].Paycheck:
                counter += float(j)
            y.append(counter)
            current_salary += counter

        colors = ['red' if i < (user_goal / 12) else 'green' for i in y]
        fig, ax = plt.subplots(facecolor=BLUE)
        ax.set_facecolor(BEIGE)
        ax.set_title("Overview", loc="left")
        bar_container = ax.bar(x, y, width=.6, color=colors)
        ax.bar_label(bar_container)

        plot_canvas = FigureCanvasTkAgg(fig)
        plot_canvas.get_tk_widget().grid(column=0, row=6, columnspan=3, rowspan=15, pady=10)

    def reset_data():
        monthly_report = {
            "Date": [],
            "Month": [],
            "Paycheck": []
        }

        ok_reset = messagebox.askyesno(title="Reset?", message=f"Are you sure you want to reset all of your Data?")

        if ok_reset:
            data = pd.DataFrame(monthly_report)
            data.to_csv(f"data\\{current_user}_data.csv", mode="w", index=False)
        else:
            pass

    def update_goal():
        with open(json_file, "r") as data:
            read_data = json.load(data)
            user_goal = read_data[ID]["Goal"]
            read_data[ID]["Goal"] = int(overall_goal.get())
        
        with open(json_file, "w") as data:
            json.dump(read_data, data, indent=4)

    def submit_data():
        monthly_report = {
            "Date": [],
            "Month": [],
            "Paycheck": []
        }

        ok_submit = messagebox.askyesno(title="Submit?", message=f"Does this look correct?\n\nDate: {date_entry.get()}\nMonths: {clicked.get()}\nPaycheck: {payment_entry.get()}")

        if ok_submit:
            monthly_report["Date"].append(date.today())
            monthly_report["Month"].append(clicked.get())
            monthly_report["Paycheck"].append(payment_entry.get())

            data = pd.DataFrame(monthly_report)
            data.to_csv(f"data\\{current_user}_data.csv", mode="a", index=False, header=False)
        else:
            pass
    
    def dark_mode():
        root.config(bg=DARK_GREY)
    def light_mode():
        root.config(bg=BEIGE)

    #-------------------------UI---------------------------#
    root = Tk()
    root.title(f"{current_user}'s Profile")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.eval('tk::PlaceWindow . center')
    root.minsize(width=1000, height=700)
    root.maxsize(width=1000, height=700)
    root.config(bg=DARK_GREY, padx=20, pady=10)

    #------------------Matplot DATA----------------------#
    refresh_report()

    #------------Profile Frame-----------------#
    profile_frame = LabelFrame(root, bg=BLUE, padx=50)
    profile_frame.grid(column=4, row=0, columnspan=2, rowspan=6)

    #Profile Label
    user_label = Label(profile_frame, text=f"{current_user}".title(), font=FONT, bg=BLUE, fg="white")
    user_label.config(pady=21)
    user_label.grid(column=5, row=0)

    #Profile Buttons
    dashboard_button = Button(profile_frame, text="     Dark Mode    ", command=dark_mode)
    dashboard_button.grid(column=5,row=1)
    settings_button = Button(profile_frame, text="    Light Mode    ", command=light_mode)
    settings_button.grid(column=5, row=2)
    reset_button = Button(profile_frame, text="     Reset Data     ", command=reset_data)
    reset_button.grid(column=5, row=3)
    log_out_button = Button(profile_frame, text="       Log Out       ", command=log_out)
    log_out_button.grid(column=5, row=4)
    delete_button = Button(profile_frame, text=" Delete Account ", command=delete_account)
    delete_button.grid(column=5, row=5)

    #-------------------Data Frame-------------------#
    data_frame = LabelFrame(root, text="Data", padx=10, pady=5)
    data_frame.grid(column=4, row=6, rowspan=10, columnspan=3)

    goal_text = Label(data_frame, text="Overall Goal", font=FONT)
    goal_text.grid(column=4, row=6)

    overall_goal = Entry(data_frame)
    overall_goal.insert(0, user_goal)
    overall_goal.grid(column=4, row=7)

    update_button = Button(data_frame, text="Update Goal", command=update_goal)
    update_button.grid(column=4, row=8)

    place_holder = Label(data_frame, text="")
    place_holder.config(pady=10)
    place_holder.grid(column=4, row=9)

    select_month = Label(data_frame, text="Month", font=FONT)
    select_month.grid(column=4, row=10)

    clicked = StringVar()
    clicked.set(f"{month_text}")
    month_list = OptionMenu(data_frame, clicked, *MONTHS)
    month_list.grid(column=4, row=11)

    place_holder1 = Label(data_frame, text="")
    place_holder1.config(pady=10)
    place_holder1.grid(column=4, row=12)

    date_label = Label(data_frame, text="Date Entered", font=FONT)
    date_label.config(padx=20)
    date_label.grid(column=4, row=13)
    date_entry = Entry(data_frame, width=30)
    date_entry.insert(0, date.today())
    date_entry.grid(column=4, row=14)

    place_holder2 = Label(data_frame, text="")
    place_holder2.config(pady=10)
    place_holder2.grid(column=4, row=15)

    payment_label = Label(data_frame, text="Paycheck", font=FONT)
    payment_label.config(padx=40)
    payment_label.grid(column=4, row=16)
    payment_entry = Entry(data_frame, width=30)
    payment_entry.grid(column=4, row=17)

    place_holder3 = Label(data_frame, text="")
    place_holder3.config(pady=10)
    place_holder3.grid(column=4, row=18)

    #Submit
    submit_buttom = Button(data_frame, text="Submit", width=16, command=submit_data)
    submit_buttom.config(padx=20)
    submit_buttom.grid(column=4, row=19)

    place_holder4 = Label(data_frame, text="")
    place_holder4.config(pady=10)
    place_holder4.grid(column=4, row=20)

    refresh_button = Button(data_frame, text="Refresh Report", command=refresh_report)
    refresh_button.grid(column=4, row=21)

    # Dashboard Canvas
    canvas = Canvas(width=750, height=200, bg=BLUE, highlightbackground=SOFT_GREEN, highlightthickness=0)
    canvas.create_text(375,25, text="Dashboard", fill="white", font=("Impact", 20))
    canvas.create_rectangle(30,175,250,80, fill=DARK_GREY)
    canvas.create_rectangle(280,175,480,80, fill=DARK_GREY)
    canvas.create_rectangle(510,175,730,80, fill=DARK_GREY)
    canvas.create_text(130,120, text=f"GOAL\n\n", font=("Impact", 15), fill="white")
    salary_text = canvas.create_text(375,120, text=f"Current Salary\n\n"+"    ${:,.2f}".format(current_salary), font=("Impact", 15), fill="white")
    canvas.create_text(615,120, text="Remaining\n\n", font=("Impact", 15), fill="white")
    canvas.grid(column=0, row=0, columnspan=3, rowspan=6)

    #Goal Text
    update_goal_text = canvas.create_text(130, 140, text="${:,.2f}".format(user_goal), font=("Impact", 15), fill="white")
    remaing_salary = user_goal - int(current_salary)
    remaining_text = canvas.create_text(615,140, text="${:,.2f}".format(remaing_salary), font=("Impact", 15), fill="white")


    def refresh_text():
        global remaing_salary

        with open(json_file, "r") as data:
            read_data = json.load(data)
            user_goal = read_data[ID]["Goal"]

        remaing_salary = user_goal - int(current_salary)

        canvas.itemconfig(salary_text, text=f"Current Salary\n\n"+"    ${:,.2f}".format(current_salary))
        canvas.itemconfig(remaining_text, text="${:,.2f}".format(remaing_salary))
        canvas.itemconfig(update_goal_text, text="${:,.2f}".format(user_goal))

        root.after(5000, refresh_text)


    refresh_text()

    root.mainloop()


if __name__ == "__main__":
    is_on = True

    while is_on == True:
        if logged_in == False:
            login_screen()
        else:
            profile_screen()

