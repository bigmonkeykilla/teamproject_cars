CAR COLLECTION MANAGER - GROUP PROJECT 1

The required console program manages make, model, year, and price in cars.csv.
Prices are fictional sample data, not current market valuations.

SETUP AND RUN
1. Install Python 3.
2. Extract the ZIP into a folder. Keep car_manager.py and cars.csv together.
3. Open a terminal in that folder.
4. Required console version: python car_manager.py
5. Optional Pygame version:
   python -m pip install -r requirements.txt
   python car_manager.py --gui
On some computers, use py or python3 instead of python.

CONSOLE COMMANDS
list: display all records and their numbers.
add: enter make, model, year, and price.
update: select a record number; blank input keeps an existing field.
delete: select a record and enter yes to confirm.
help: display usage guidance.
exit: close the program.
All successful changes save immediately. A failed save does not change the
in-memory collection. The CSV path is based on the Python file location, so
launching from another working directory still finds cars.csv.

PYGAME CONTROLS
Click a row to select it. Scroll for more records. Click Add or Update, then
click fields or press Tab. Enter validates and saves; Esc cancels.
Delete asks for confirmation: Enter confirms, Esc cancels.
Save explicitly saves the list. Exit or the window close button quits.
The rotating car is a procedural low-poly 3D model projected into Pygame.
It is an illustrative design shared by every record, not an exact model of
each listed vehicle. No external images or model files are required.

PROGRAM ORGANIZATION
read_cars / save_cars: CSV file operations.
validate_car: shared input checks.
display_cars / get_selection / get_car: console display and input.
console_main: required repeating command menu and CRUD operations.
gui_main / draw_car: optional Pygame interface and 3D rendering.
main: chooses the interface and reports startup errors safely.

PRESENTATION OUTLINE
1. Purpose: organize a collection of cars stored in a CSV file.
2. Show the four fields and explain the numbered records.
3. Run list, add a car, update its price, then delete it.
4. Add another car, exit, and restart to show that it remains saved.
5. Try an unknown command and an invalid record number.
6. Explain functions, the main loop, CSV reading, and automatic saving.
7. Optionally demonstrate the Pygame interface and rotating car preview.
Divide these topics among your actual group members so everyone participates.

MANUAL TEST CHECKLIST
[ ] List existing cars.
[ ] Add a valid car and verify its CSV row.
[ ] Update a car; verify blank fields keep their original values.
[ ] Cancel deletion, then confirm deletion.
[ ] Exit and restart; confirm changes persist.
[ ] Try an invalid command, nonnumeric selection, zero, and an oversized number.
[ ] Try blank make/model, invalid year, negative price, and nonnumeric price.
[ ] Start from a different working directory.
[ ] In Pygame, add/update/delete, cancel forms, and scroll a long collection.

SUBMISSION
The assignment requests car_manager.py and cars.csv. The console works with
Python's standard library and needs no Pygame installation. Include the other
files if your instructor wants the optional graphical interface instructions.
