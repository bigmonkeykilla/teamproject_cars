# Car Dealership V3 Group Project
# This program lets the user list, add, modify, and delete cars.

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

try:
    import pyttsx3
    voice_available = True
except ImportError:
    voice_available = False

# Use a CSV file in the same folder as this program.
file_name = os.path.join(os.path.dirname(__file__), "cars_info.csv")
cars = []
selected_car = None

# Read the cars from the CSV file when the program starts.
if os.path.exists(file_name):
    with open(file_name, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for car in reader:
            if len(car) == 3:
                cars.append(car)


# Save the car list to the CSV file.
def save_cars():
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(cars)


# Read a message aloud if voice is turned on.
def speak(message):
    if voice_available and voice_on.get():
        try:
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()
        except Exception:
            pass


# Show a message at the bottom of the window.
def show_status(message):
    status_label.config(text=message)
    speak(message)


# Update the table with all cars.
def list_cars():
    for item in car_table.get_children():
        car_table.delete(item)

    for car in cars:
        car_table.insert("", tk.END, values=car)

    show_status("We currently have " + str(len(cars)) + " cars.")


# Clear the input fields.
def clear_fields():
    global selected_car
    model_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)
    selected_car = None


# Check the information entered by the user.
def get_car_info():
    model = model_entry.get().strip()
    year = year_entry.get().strip()
    condition = condition_entry.get().strip()

    if model == "" or year == "" or condition == "":
        messagebox.showwarning("Missing Information", "Please fill in all three fields.")
        return None

    if not year.isdigit() or len(year) != 4:
        messagebox.showwarning("Invalid Year", "Please enter a four-digit year.")
        return None

    return [model, year, condition]


# Add a new car to the list.
def add_car():
    car = get_car_info()
    if car is None:
        return

    cars.append(car)
    save_cars()
    clear_fields()
    list_cars()
    show_status(car[0] + " was added successfully.")


# Put the selected car's information in the input fields.
def select_car(event):
    global selected_car
    selection = car_table.selection()
    if not selection:
        return

    selected_car = car_table.index(selection[0])
    car = cars[selected_car]

    model_entry.delete(0, tk.END)
    model_entry.insert(0, car[0])
    year_entry.delete(0, tk.END)
    year_entry.insert(0, car[1])
    condition_entry.delete(0, tk.END)
    condition_entry.insert(0, car[2])
    status_label.config(text="Selected " + car[0] + ".")


# Modify the selected car.
def modify_car():
    if selected_car is None:
        messagebox.showinfo("Select a Car", "Please select a car first.")
        return

    car = get_car_info()
    if car is None:
        return

    cars[selected_car] = car
    save_cars()
    clear_fields()
    list_cars()
    show_status(car[0] + " was modified successfully.")


# Delete the selected car.
def delete_car():
    if selected_car is None:
        messagebox.showinfo("Select a Car", "Please select a car first.")
        return

    car = cars[selected_car]
    answer = messagebox.askyesno("Delete Car", "Delete " + car[0] + "?")
    if answer:
        cars.pop(selected_car)
        save_cars()
        clear_fields()
        list_cars()
        show_status(car[0] + " was deleted.")


# Create the main window.
window = tk.Tk()
window.title("Car Dealership")
window.geometry("750x550")
window.configure(bg="lightblue")

# Create the title frame.
title_frame = tk.Frame(window, bg="lightblue")
title_frame.pack(pady=15)

title_label = tk.Label(
    title_frame,
    text="Car Dealership",
    font=("Arial", 18, "bold"),
    fg="darkblue",
    bg="lightblue"
)
title_label.pack()

# Create the input frame.
input_frame = tk.LabelFrame(window, text="Car Details", bg="lightblue")
input_frame.pack(fill="x", padx=20, pady=10)

# Car model
model_label = tk.Label(input_frame, text="Car Model:", font=("Arial", 12), bg="lightblue")
model_label.grid(row=0, column=0, padx=10, pady=8, sticky="e")
model_entry = tk.Entry(input_frame, width=35, font=("Arial", 12))
model_entry.grid(row=0, column=1, padx=10, pady=8)

# Car year
year_label = tk.Label(input_frame, text="Year:", font=("Arial", 12), bg="lightblue")
year_label.grid(row=1, column=0, padx=10, pady=8, sticky="e")
year_entry = tk.Entry(input_frame, width=35, font=("Arial", 12))
year_entry.grid(row=1, column=1, padx=10, pady=8)

# Car condition
condition_label = tk.Label(input_frame, text="Condition:", font=("Arial", 12), bg="lightblue")
condition_label.grid(row=2, column=0, padx=10, pady=8, sticky="e")
condition_entry = tk.Entry(input_frame, width=35, font=("Arial", 12))
condition_entry.grid(row=2, column=1, padx=10, pady=8)

# Create the button frame.
button_frame = tk.Frame(window, bg="lightblue")
button_frame.pack(pady=10)

list_button = tk.Button(button_frame, text="List Cars", command=list_cars, width=12)
list_button.grid(row=0, column=0, padx=5)

add_button = tk.Button(button_frame, text="Add Car", command=add_car, width=12)
add_button.grid(row=0, column=1, padx=5)

modify_button = tk.Button(button_frame, text="Modify Car", command=modify_car, width=12)
modify_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(button_frame, text="Delete Car", command=delete_car, width=12)
delete_button.grid(row=0, column=3, padx=5)

exit_button = tk.Button(button_frame, text="Exit", command=window.destroy, width=10)
exit_button.grid(row=0, column=4, padx=5)

# Create the frame that displays all cars.
list_frame = tk.LabelFrame(window, text="Available Cars", bg="lightblue")
list_frame.pack(fill="both", expand=True, padx=20, pady=10)

car_table = ttk.Treeview(list_frame, columns=("model", "year", "condition"), show="headings")
car_table.heading("model", text="Car Model")
car_table.heading("year", text="Year")
car_table.heading("condition", text="Condition")
car_table.column("model", width=260)
car_table.column("year", width=100)
car_table.column("condition", width=170)
car_table.pack(fill="both", expand=True, padx=10, pady=10)
car_table.bind("<<TreeviewSelect>>", select_car)

# Create the status and voice controls.
bottom_frame = tk.Frame(window, bg="lightblue")
bottom_frame.pack(fill="x", padx=20, pady=10)

status_label = tk.Label(bottom_frame, text="Enter car details or select a car.", bg="lightblue")
status_label.pack(side="left")

voice_on = tk.BooleanVar(value=voice_available)
voice_checkbox = tk.Checkbutton(
    bottom_frame, text="Voice", variable=voice_on,
    bg="lightblue", state="normal" if voice_available else "disabled"
)
voice_checkbox.pack(side="right")

# Show the cars when the program starts.
list_cars()
window.mainloop()
