# This file contains the code for the application.

from LLL import AvailableRooms
from table import Tree23

def main():
    schedule = Tree23()
    rooms = AvailableRooms()
    rooms.display_all()
    print("Welcome to Spring 2023 Term Scheduler!\n")
    print ("What would you like to do?")

    done = False
    while (not done):
        selected = menu()
        # Scheduling a room
        if selected == 1:
            schedule_room(rooms, schedule)
        # Display current schedule for all classes
        elif selected == 2:
            try:
                schedule.display_all()
            except Exception as e:
                print(e)
        # Retrieve a class schedule
        elif selected == 3:
            retrieve_class(schedule)
        # Quit program
        elif selected == 4:
            break
        
        if (not again()):
            done = True
    
    print("Thank you for using the program!")

'''
This function displays the main menu options
Argument: none
Return: int of selected option
'''
def menu():
    # Main menu options
    print("1) Schedule a room for a class\n" +
          "2) Display room/s for all classes\n" +
          "3) Retrieve room/s for a class\n" +
          "4) Quit\n")
    
    done = False
    while (not done):
        num = input(f"Please enter the number of the action you would like to take: ")
        try:
            num = int(num)
            if (num <= 0 or num > 4):
                print("Please enter a number between 1 and 4, inclusive.")
            else:
                done = True
        except ValueError:
                print("Please enter an integer value.")
    print()
    return num

'''
This function prompts to the user if they would like to take another action
Argument: none
Return: True if answered yes, False if answered no
'''
def again():
    done = False
    while (not done):
        answer = input("Would you like to take another action? (y/n): ")
        if (answer == 'y' or answer == 'Y'):
            print()
            return True
        elif (answer == 'n' or answer == 'N'):
            print()
            return False
        else:
            print("Please only enter 'y' or 'n'.")

'''
This is the function to retrieve and display the schedule for a class
Argument: a Tree23 object
Return: none
'''
def retrieve_class(schedule):
    # Get info from user
    courseName = input("Enter course name: ")
    print()
    try:
        result = schedule.retrieve_class(courseName)
        if (result):
            print(f"The rooms for {courseName} are:\n")
            result[1].display_all()
        else:
            print(f"Error finding {courseName}, please try again.")
    except Exception as e:
        print(e)

'''
This is the function to schedule a room for a class
Argument: a AvailableRooms object and a Tree23 object
Return: none
'''
def schedule_room(rooms, schedule):
    # Get info from user
    courseName = input("Enter course name: ")
    print()
    type = get_room_type(courseName)
    occupancy = get_occupancy()
    print("Please provide information about the class you would like to schedule.")
    days = get_days(courseName)
    dayTime = get_times(days, courseName)
    desiredSpec = get_base_specifications(courseName)
    additional = get_unique_specification(type)

    # Finding matches for the specifications
    try:
        matches = rooms.find_matches(type, desiredSpec, dayTime, occupancy, additional)
        roomNum, roomObj = select_match(matches, courseName) #returns room number and room object

        # Add the selected roomObj to schedule table
        schedule.insert(courseName, roomObj)

        # Remove selected room
        if (rooms.remove_room(type, roomNum)):
            print(f"Successfully scheduled {courseName} in {roomNum}.\n")
        else:
            print(f"Error scheduling room, please try again.\n")
    except Exception as e:
        print(e)

'''
This function display the matching results and prompt the user to select the room they would like to schedule
Argument: array of matched rooms, string of courseName
Return: string of roomNumber that's selected and the selected roomObj
'''
def select_match(matches, courseName):
    if (len(matches) == 0):
        raise Exception("No good matches found for your specifications, please try again.\n")
    
    print("Rooms matching your search...\n")
    for match in matches:
        print(match)
        print()
    
    roomNum = input(f"Please enter the room number you would like to schedule for {courseName} (ex. FAB1): ")

    roomObj = None
    for match in matches:
        if (match == roomNum):
            roomObj = match

    return roomNum, roomObj

'''
This is the function to get the unique specification to each room type
Argument: string of room type
Return: int for the additional feature selected
'''
def get_unique_specification(type):
    if type == "lab":
        return get_computer_num()
    elif type == "lecture":
        return get_acoustic_rating()
    elif type == "seminar":
        return get_round_table()
    
'''
This function prompts the user for the desired computer number in the lab
Argument: none
Return: int for the desired number
'''
def get_computer_num():
    done = False
    while (not done):
        num = input(f"Please enter the number of computers you would like in the lab: ")
        try:
            num = int(num)
            done = True
        except ValueError:
                print("Please enter an integer value.")
    print()
    return num

'''
This function prompts the user for the desired acoustic rating in the lecture hall
Argument: none
Return: int for the rating
'''
def get_acoustic_rating():
    done = False
    while (not done):
        num = input(f"Please enter acoustic rating you would like the lecture hall to have (from 0 to 5, inclusive): ")
        try:
            num = int(num)
            if (num <= 0 or num > 5):
                print("Please enter a number between 0 and 5, inclusive.")
            else:
                done = True
        except ValueError:
                print("Please enter an integer value.")
    print()
    return num

'''
This function prompts the user if they would like a round table in the seminar room
Argument: none
Return: int 0 for False and 1 for True
'''
def get_round_table():
    done = False
    while (not done):
        answer = input("Would you like a round table in the seminar room? (y/n): ")
        if (answer == 'y' or answer == 'Y'):
            answer = 1
            print()
            return answer
        elif (answer == 'n' or answer == 'N'):
            answer = 0
            print()
            return answer
        else:
            print("Please only enter 'y' or 'n'.")

'''
This function prompts the user to select the base features they would like the room to have
Argument: string of course name
Return: a dictonary of specifications (ex. {"movableFurniture":False, "zoomEnabled":False, "hasProjector":True, "hasWhiteboard":False})
'''
def get_base_specifications(courseName):
    print(f"Room features:")
    print("1) Movable furniture\n" +
          "2) Zoom enabled\n" +
          "3) Has projector\n" +
          "4) Has whiteboards\n")
    
    chosenSpecs = []
    chosenSpecsDict = {}
    done = False
    while (not done):
        chosenSpecs = input(f"Please select the features you would like a room for {courseName} to have (ex. 1, 2, 3, 4 for all features): ")
        chosenSpecs = [spec.strip() for spec in chosenSpecs.split(',')] #clean up empty spaces

        try:
            chosenSpecs = [int(spec) for spec in chosenSpecs]
            outOfBound = False
            for spec in chosenSpecs:
                if spec < 0 or spec > 4:
                    outOfBound = True
                    break #only need one errorneous value
            if (not outOfBound):
                done = True
            else:
                print("Please enter numbers between 1 and 4, inclusive.")
        except ValueError:
            print("Please enter an integer value.")

    # Parse selected options into chosenSpecsDict 
    if (1 in chosenSpecs):
        chosenSpecsDict["movableFurniture"] = True
    else:
        chosenSpecsDict["movableFurniture"] = False
    
    if (2 in chosenSpecs):
        chosenSpecsDict["zoomEnabled"] = True
    else:
        chosenSpecsDict["zoomEnabled"] = False
    
    if (3 in chosenSpecs):
        chosenSpecsDict["hasProjector"] = True
    else:
        chosenSpecsDict["hasProjector"] = False
    
    if (4 in chosenSpecs):
        chosenSpecsDict["hasWhiteboard"] = True
    else:
        chosenSpecsDict["hasWhiteboard"] = False
    print()
    return chosenSpecsDict

'''
This function prompts the user for the time/s at the day/s they want to schedule their class
Argument: the array of days from get_days() and string of course name
Return: a dictionary of days and times (ex. {'M': ["10PM", "8AM"], 'T': ["11AM"]})
'''
def get_times(days, courseName):
    print(f"What time/s would like to schedule {courseName} on the days you selected? (ex. 10AM, 4PM)")
    dayTimes = {}
    for day in days:
        times = input(f"{day}: ")
        times = [time.strip() for time in times.split(',')] #clean up empty spaces
        dayTimes[day] = list(set(times)) #remove duplicated values
    print()
    return dayTimes

'''
This function prompts the user for the day/s they want to schedule their class
Argument: string of course name
Return: an array of days (ex. ['M', 'W', 'TH'])
'''
def get_days(courseName):
    days = input(f"What days are you hoping to schedule {courseName} (ex. M, W, TH): ")
    days = [day.strip() for day in days.split(',')] #clean up empty spaces
    print()
    return list(set(days)) #remove duplicated values

'''
This function prompts the user to enter the occupancy they would like for the room
Argument: none
Return: an int for occupancy
'''
def get_occupancy():
    done = False
    while (not done):
        num = input(f"Please enter the occupancy of the room you would like: ")
        try:
            num = int(num)
            if (num <= 0):
                print("Please enter a number greater than 0.")
            else:
                done = True
        except ValueError:
                print("Please enter an integer value.")
    print()
    return num

'''
This function prompts the user to enter a room type they want to schedule
Argument: string of course name
Return: a string matching their selected option
'''
def get_room_type(courseName):
    print("The room types we offer are:\n" +
          "1) Computer lab\n" +
          "2) Lecture hall\n" +
          "3) Seminar room\n")
   
    done = False
    while (not done):
        type = input(f"Please enter the number of room type you would like to schedule for {courseName}: ")

        try:
            type = int(type)
            if (type <= 0 or type > 3):
                print("Please enter a number between 1 and 3, inclusive.")
            else:
                done = True
        except ValueError:
            print("Please enter an integer value.")
    print()
    # Convert to a string of the type selected
    if type == 1:
        return "lab"
    elif type == 2:
        return "lecture"
    elif type == 3:
        return "seminar"

if __name__ == "__main__":
    main()
