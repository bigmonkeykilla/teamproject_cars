import os
import csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, 'cars_info.csv')

def display_menu():
    print("The Car Dealership program V2")
    print("COMMAND MENU")
    print("list - List all cars")
    print("add  - Add a car")
    print("del  - Delete a car")
    print("mod  - Modify a car")
    print("exit - Exit program\n")
    print()

def write_cars(my_cars):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(my_cars)

def read_cars():
    my_cars = []

    with open(FILE_NAME, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0 and len(row) == 3:
                my_cars.append(row)

    return my_cars

def list_cars(my_car_2d_list):
    if len(my_car_2d_list) == 0:
        print("There are no more cars in the dealership avaliable.\n")
    else:
        my_cars_number = 1
        for car in my_car_2d_list:
            print(my_cars_number, "Car Model:", car[0], "|", "Year:", car[1], "|", "Condition:", car[2])
            my_cars_number = my_cars_number + 1

        print()


def add_car(my_car_2d_list):
    name = input("Name: ")
    year = input("Year: ")
    condition = input("Condition: ")

    my_car = [name, year, condition]
    my_car_2d_list.append(my_car)
    write_cars(my_car_2d_list)
    print(f"{my_car[0]} was added.\n")


def delete_car(my_car_2d_list):
    my_cars_number = int(input("Enter the Number of the Car to Delete: "))
    if my_cars_number < 1 or my_cars_number > len(my_car_2d_list):
        print("Invalid car number.\n")
    else:
        my_cars = my_car_2d_list.pop(my_cars_number - 1)
        write_cars(my_car_2d_list)
        print(f"{my_cars[0]} was deleted.\n")

def modify_car(my_car_2d_list):
    my_cars_number = int(input("Enter the Number of the Car to Modify: "))
    if my_cars_number < 1 or my_cars_number > len(my_car_2d_list):
        print("Invalid car number.\n")
    else:
        my_car = my_car_2d_list[my_cars_number - 1]
        print(f"Current Car Model: {my_car[0]}")
        new_name = input("Enter new name (leave blank to keep current): ")
        if new_name:
            my_car[0] = new_name

        print(f"Current Year: {my_car[1]}")
        new_year = input("Enter new year (leave blank to keep current): ")
        if new_year:
            my_car[1] = new_year

        print(f"Current Condition: {my_car[2]}")
        new_condition = input("Enter new condition (leave blank to keep current): ")
        if new_condition:
            my_car[2] = new_condition

        write_cars(my_car_2d_list)
        print(f"{my_car[0]} was modified.\n")

def main():
    display_menu()
    my_cars = read_cars()

    while True:
        command = input("Command: ")

        if command.lower() == "exit":
            break

        if command.lower() == "list":
            list_cars(my_cars)
        elif command.lower() == "add":
            add_car(my_cars)
        elif command.lower() == "del":
            delete_car(my_cars)
        elif command.lower() == "mod":
            modify_car(my_cars)
        else:
            print("Not a valid command. Please try again.\n")

    print("Bye!")


if __name__ == "__main__":
    main()
