"""Car dealership GUI with optional offline text-to-speech.
Place cars_info.csv in the same folder as this file.
Install voice support with: python -m pip install pyttsx3
"""
import csv
import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cars_info.csv")


def read_cars():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, newline="", encoding="utf-8-sig") as file:
        return [row for row in csv.reader(file) if len(row) == 3]


def write_cars(cars):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(cars)


class CarDealership:
    def __init__(self, window):
        self.window = window
        self.window.title("Car Dealership - Tkinter")
        self.window.geometry("810x570")
        self.window.minsize(690, 520)
        self.cars = read_cars()
        self.speech_queue = queue.Queue()
        self.voice_on = tk.BooleanVar(value=True)
        self.name = tk.StringVar()
        self.year = tk.StringVar()
        self.condition = tk.StringVar()
        self.status = tk.StringVar(value="Select a car or enter details to get started.")
        self.editing_index = None

        try:
            import pyttsx3  # noqa: F401
            self.voice_available = True
            threading.Thread(target=self.speech_worker, daemon=True).start()
        except ImportError:
            self.voice_available = False
            self.voice_on.set(False)
            self.status.set("Voice disabled. Install it using: python -m pip install pyttsx3")

        header = tk.Frame(window, bg="#1d3557", padx=18, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="CAR DEALERSHIP", font=("Arial", 20, "bold"),
                 fg="white", bg="#1d3557").pack(anchor="w")
        tk.Label(header, text="Manage cars and hear prompts aloud", font=("Arial", 10),
                 fg="#dce8f8", bg="#1d3557").pack(anchor="w")

        actions = tk.Frame(window, padx=15, pady=10)
        actions.pack(fill="x")
        for text, command in [
            ("List Cars", self.list_cars), ("Add Car", self.add_car),
            ("Modify Car", self.modify_car), ("Delete Car", self.delete_car),
            ("Exit", self.window.destroy)
        ]:
            ttk.Button(actions, text=text, command=command).pack(side="left", padx=4)
        ttk.Checkbutton(actions, text="Voice", variable=self.voice_on,
                        state="normal" if self.voice_available else "disabled").pack(side="right")

        form = ttk.LabelFrame(window, text="Car Details", padding=12)
        form.pack(fill="x", padx=18, pady=(2, 10))
        for row, (title, variable, prompt) in enumerate([
            ("Car Model", self.name, "Enter the car model."),
            ("Year", self.year, "Enter the car year."),
            ("Condition", self.condition, "Enter the car condition.")
        ]):
            ttk.Label(form, text=title + ":").grid(row=row, column=0, sticky="w", pady=5)
            ttk.Entry(form, textvariable=variable, width=47).grid(row=row, column=1, sticky="ew", padx=10, pady=5)
            ttk.Button(form, text="🔊 Speak", command=lambda p=prompt: self.speak(p)).grid(row=row, column=2, pady=5)
        form.columnconfigure(1, weight=1)
        ttk.Label(form, text="Select a row to edit or delete it. Add Car uses the fields above.",
                  foreground="#555555").grid(row=3, column=0, columnspan=3, sticky="w", pady=(6, 0))

        listing = ttk.LabelFrame(window, text="Available Cars", padding=10)
        listing.pack(fill="both", expand=True, padx=18, pady=(0, 10))
        self.table = ttk.Treeview(listing, columns=("model", "year", "condition"), show="headings", selectmode="browse")
        for col, title, width in [("model", "Car Model", 290), ("year", "Year", 100), ("condition", "Condition", 170)]:
            self.table.heading(col, text=title)
            self.table.column(col, width=width)
        scroll = ttk.Scrollbar(listing, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.on_select)

        bottom = tk.Frame(window, padx=18, pady=10)
        bottom.pack(fill="x")
        ttk.Label(bottom, textvariable=self.status, wraplength=620).pack(side="left", anchor="w")
        ttk.Button(bottom, text="🔊 Read Status", command=lambda: self.speak(self.status.get())).pack(side="right")
        self.refresh()

    def speech_worker(self):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            while True:
                phrase = self.speech_queue.get()
                try:
                    engine.say(phrase)
                    engine.runAndWait()
                except Exception:
                    pass
                finally:
                    self.speech_queue.task_done()
        except Exception:
            
            pass

    def speak(self, words):
        if self.voice_available and self.voice_on.get():
            self.speech_queue.put(str(words))

    def announce(self, words):
        self.status.set(words)
        self.speak(words)

    def refresh(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for index, car in enumerate(self.cars):
            self.table.insert("", "end", iid=str(index), values=car)

    def on_select(self, _event=None):
        selection = self.table.selection()
        if not selection:
            return
        self.editing_index = int(selection[0])
        car = self.cars[self.editing_index]
        self.name.set(car[0])
        self.year.set(car[1])
        self.condition.set(car[2])
        self.status.set(f"Selected {car[0]}. You can modify or delete this car.")

    def clear_fields(self):
        self.name.set("")
        self.year.set("")
        self.condition.set("")
        self.editing_index = None
        self.table.selection_remove(self.table.selection())

    def get_fields(self):
        car = [self.name.get().strip(), self.year.get().strip(), self.condition.get().strip()]
        if not all(car):
            self.announce("Please enter the car model, year, and condition.")
            messagebox.showwarning("Missing information", "Please fill in all three fields.")
            return None
        if not (car[1].isdigit() and len(car[1]) == 4):
            self.announce("Please enter a valid four digit year.")
            messagebox.showwarning("Invalid year", "Enter a four-digit year, such as 2024.")
            return None
        return car

    def list_cars(self):
        self.refresh()
        if not self.cars:
            self.announce("There are no cars in the dealership.")
        else:
            self.announce(f"Showing {len(self.cars)} cars. " +
                          " ".join(f"{c[1]} {c[0]}, condition {c[2]}." for c in self.cars))

    def add_car(self):
        car = self.get_fields()
        if car is None:
            return
        self.cars.append(car)
        write_cars(self.cars)
        self.refresh()
        self.clear_fields()
        self.announce(f"{car[0]} was added successfully.")

    def modify_car(self):
        if self.editing_index is None:
            self.announce("Select a car from the list to modify.")
            messagebox.showinfo("Select a car", "Click a car in the list first.")
            return
        car = self.get_fields()
        if car is None:
            return
        self.cars[self.editing_index] = car
        write_cars(self.cars)
        self.refresh()
        self.clear_fields()
        self.announce(f"{car[0]} was modified successfully.")

    def delete_car(self):
        if self.editing_index is None:
            self.announce("Select a car from the list to delete.")
            messagebox.showinfo("Select a car", "Click a car in the list first.")
            return
        car = self.cars[self.editing_index]
        if messagebox.askyesno("Delete car", f"Delete {car[0]}?"):
            self.cars.pop(self.editing_index)
            write_cars(self.cars)
            self.refresh()
            self.clear_fields()
            self.announce(f"{car[0]} was deleted.")


if __name__ == "__main__":
    root = tk.Tk()
    CarDealership(root)
    root.mainloop()
