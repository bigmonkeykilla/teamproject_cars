import csv

FILE_NAME = "cars_info.csv"


def display_menu():
    print("COMMAND MENU")
    print("list - List all cars")
    print("add  - Add a car")
    print("del  - Delete a car")
    print("exit - Exit program\n")


def write_cars(my_cars):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(my_cars)


def read_cars():
    my_cars = []

    try:
        with open(FILE_NAME, newline="") as file:
            reader = csv.reader(file)
            for line in reader:
                my_cars.append(line)
    except FileNotFoundError:
        pass

    return my_cars


def list_cars(my_car_2d_list):
    if len(my_car_2d_list) == 0:
        print("There are no cars in the list.\n")
    else:
        i = 1
        for my_car in my_car_2d_list:
            print(i, my_car[0] + " (" + str(my_car[1]) + ")")
            i += 1

        print()


def add_car(my_car_2d_list):
    name = input("Name: ")
    year = input("Year: ")

    my_car = [name, year]
    my_car_2d_list.append(my_car)

    write_cars(my_car_2d_list)

    print(f"{my_car[0]} was added.\n")


def delete_car(my_car_2d_list):
    car_number = int(input("Enter the Number of the Car to Delete: "))

    if car_number < 1 or car_number > len(my_car_2d_list):
        print("Invalid car number.\n")
    else:
        my_car_2d_list.pop(car_number - 1)
        write_cars(my_car_2d_list)
        print("Car deleted.\n")


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


if __name__ == "__main__":
    main()
