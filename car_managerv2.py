import csv

FILE_NAME = "cars_info.csv"

def display_menu():
    print("COMMAND MENU")
    print("list - List all movies")
    print("add  - Add a movie")
    print("del  - Delete a movie")
    print("exit - Exit program\n")  

    def write_cars(my_cars):
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(my_cars)  

    def read_cars():
        my_cars = []

        with open(file_name, newline="") as file:
            reader = csv.reader(file)
            for line in reader:
                my_cars.append(line)

        return my_cars
    
    def list_cars(my_car_2d_list):
        if len(my_car_2d_list) == 0:
            print("There are no cars in the list.\n")
        else:
            i = 1
            for my_car in my_car_2d_list:
                print(i, my_car[0] + " (" + str(my_car[1]) + ")")
                i = i + 1
            print()

    def add_car(my_car_2dlist):
        name = input("Name: ")
        year = input("Year: ")

        my_car = [name, year]
        my_car_2dlist.append(my_car)

        write_cars(my_car_2dlist)

        print(f"{my_car[0]} was added.\n")

    def delete_car(my_car_2dlist):
        car_number = int(input("Enter the Number of the Car to Delete: "))

        if car_number < 1 or car_number > len(my_car_2dlist):
            print("Invalid car number.\n")

    def main():
        my_cars = read_cars()

        display_menu()

        while True:
            command = input("Command: ")
            if command == "list":
                list_cars(my_cars)
            elif command == "add":
                add_car(my_cars)
            elif command == "del":
                delete_car(my_cars)
            elif command == "exit":
                break
            else:
                print("Not a valid command. Please try again.\n")

        print("Bye!")