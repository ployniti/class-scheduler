# This file contains the code for the LNode and LLL classes.

import classroom
import numpy as np
import random

### LNODE ###
class LNode:
    '''
    Default constructor with arguments
    Argument: a class object to set as the LNode's data
    Return: none
    '''
    def __init__(self, classObj=None):
        self._class = classObj
        self._next = None
    
    '''
    Destructor
    Argument: none
    Return: none
    '''
    def __del__(self):
        self._class = None
        self._next = None
    
    '''
    Overloaded display operator to display the class data of a LNode
    Argument: none
    Return: a string object
    '''
    def __str__(self):
        return self._class.__str__() #or self.get_class().__str__()
    
    '''
    This is the function to set the next node
    Argument: node object to set next to
    Return: none
    '''
    def set_next(self, toSet):
        self._next = toSet
    
    '''
    This is the function to get the next node
    Argument: none
    Return: none
    '''
    def get_next(self):
        return self._next
    
    '''
    This is the function to get the class object
    Argument: none
    Return: none
    '''
    def get_class(self):
        return self._class
    
    '''
    This is the function to pass the required specification from the user to find matches in the LLL
    Arguments: dicts of desired specification and day/time and occupancy int
    Return: an int of the overall match, greater is better
    '''
    def match_requirements(self, desiredSpec, dayTime, occupancy):
        try:
            return self._class.match_requirements(desiredSpec, dayTime, occupancy)
        except Exception as e:
            print(e)

### LLL ###
class LLL:
    '''
    Default constructor
    Argument: none
    Return: none
    '''
    def __init__(self):
        self._head = None
    
    '''
    This is the function to get the head of the LLL
    Argument: none
    Return: head LNode object
    '''
    def get_head(self):
        return self._head
    
    '''
    This is the wrapper function to display all nodes' class object in the list
    Argument: none
    Return: 1 for success, 0 for failure
    '''
    def display_all(self):
        # If head is None, raise an exception
        if not self._head:
            raise Exception("List is empty.\n")
        return self._display_all(self._head)
    
    '''
    This is the recursive function to display all nodes' class object in the list
    Argument: none
    Return: 1 for success, 0 for failure
    '''
    def _display_all(self, head):
        if not head:
            return 1
        print(head)
        print()
        return self._display_all(head.get_next())

    '''
    This is the function to insert a new node at the beginning of the LLL
    Argument: a class object to set as the LNode's data
    Return: 1 for success, 0 for failure
    '''
    def insert(self, classObj):
        if not classObj:
            raise Exception("Empty class object passed.\n")
        
        if (not self._head):
            self._head = LNode(classObj)
            return 1
        
        newFirst = LNode(classObj)
        newFirst.set_next(self._head)
        self._head = newFirst
        return 1
    
    '''
    This is a wrapper function to find matches from the available classes
    Arguments: dicts of desired specification and day/time and occupancy int
    Return: an array of matched classes
    '''
    def find_matches(self, type, desiredSpec, dayTime, occupancy, additional):
        if not self._head:
            raise Exception("List is empty.\n")
        
        if not desiredSpec or not dayTime or occupancy <= 0 :
            raise Exception("No specification, day/time, or occupancy provided for matching.\n")
        
        return self._find_matches(self._head, type, desiredSpec, dayTime, occupancy, additional)
    
    '''
    This is a recursive function to find matches from the available classes
    Arguments: head LNode object, dicts of desired specification and day/time and occupancy int
    Return: an array of matched classes
    '''
    def _find_matches(self, head, type, desiredSpec, dayTime, occupancy, additional):
        matches = []
        if not head:
            return matches
        
        # Base specification
        result = head.match_requirements(desiredSpec, dayTime, occupancy)

        # Unique specification
        if (type.lower() == "lab"):
            result += head.get_class().computer_num_check(additional)
        elif (type.lower() == "lecture"):
            result += head.get_class().acoustic_check(additional)
        elif (type.lower() == "seminar"):
            result += head.get_class().table_check(additional)
        
        if result >= 5:
            matches.append(head.get_class()) #add the class object to the list of matches

        matches += self._find_matches(head.get_next(), type, desiredSpec, dayTime, occupancy, additional)   
        return matches
    
    '''
    This is the wrapper function to remove a node with a matching room number
    Argument: string of room number
    Return: True for if a node is removed, False if not
    '''
    def remove_match(self, roomNum):
        if not self._head:
            raise Exception("List is empty.\n")
        elif not roomNum:
            raise Exception("Empty string object passed.\n")
        
        self._head, flag = self._remove_match(self._head, roomNum)
        return flag
    
    '''
    This is the wrapper function to remove a node with a matching room number
    Argument: string of room number
    Return: head node for reconnecting and True for if a node is removed, False if not
    '''
    def _remove_match(self, head, roomNum):
        if not head: #no match, nothing is removed
            return head, False
        if (head.get_class() == roomNum):
            return head.get_next(), True
        next, flag = self._remove_match(head.get_next(), roomNum)
        head.set_next(next)
        return head, flag

### AVAILABLEROOMS ###
class AvailableRooms:
    '''
    Default constructor
    Argument: none
    Return: none
    '''
    def __init__(self, labNum=5, lectureNum=5, seminarNum=5):
        # Generate LLL of different room types
        labs = self._generate_LLL('lab', labNum)
        lectureHalls = self._generate_LLL('lecture', lectureNum)
        seminars = self._generate_LLL('seminar', seminarNum)
        self._rooms = np.array([labs, lectureHalls, seminars]) #array of LLL of available rooms

    '''
    This is the function to display all rooms in the AvailableRooms object
    Argument: none
    Return: none
    '''
    def display_all(self):
        # Empty LLLs in the array
        if (not self._rooms[0].get_head() and not self._rooms[1].get_head() and not self._rooms[2].get_head()):
            raise Exception("No available rooms.\n")
        
        for i in range(len(self._rooms)):
            try:
                self._rooms[i].display_all()
            except Exception as e: #empty LLL
                print(e)
    
    '''
    This is a function to find room matches based on the user's specification
    Argument: string of room type, dicts of desired specification and day/time and occupancy int
    Return: an array of matched classes
    '''
    def find_matches(self, type, desiredSpec, dayTime, occupancy, additional):
        # Empty LLLs in the array
        if (not self._rooms[0].get_head() and not self._rooms[1].get_head() and not self._rooms[2].get_head()):
            raise Exception("No available rooms.\n")
    
        # Empty string supplied
        elif (not type):
            raise Exception("Empty string object passed.\n")
        
        if (type.lower() == "lab"):
            try:
                matches = self._rooms[0].find_matches(type, desiredSpec, dayTime, occupancy, additional)
                return matches
            except Exception as e:
                print(e)
        elif (type.lower() == "lecture"):
            try:
                matches = self._rooms[1].find_matches(type, desiredSpec, dayTime, occupancy, additional)
                return matches
            except Exception as e:
                print(e)
        elif (type.lower() == "seminar"):
            try:
                matches = self._rooms[2].find_matches(type, desiredSpec, dayTime, occupancy, additional)
                return matches
            except Exception as e:
                print(e)

    '''
    This is a function to remove room that has been selected and assigned from the AvailableRooms
    Arguments: strings of room type and room number
    Return: True for a successful removal, False for an unsuccessful removal
    '''
    def remove_room(self, type, roomNum):
        # Empty LLLs in the array
        if (not self._rooms[0].get_head() and not self._rooms[1].get_head() and not self._rooms[2].get_head()):
            raise Exception("No available rooms.\n")
        
        # Empty string supplied
        elif (not roomNum or not type):
            raise Exception("Empty string object passed.\n")
        
        if (type.lower() == "lab"):
            try:
                return self._rooms[0].remove_match(roomNum)
            except Exception as e:
                print(e)
        elif (type.lower() == "lecture"):
            try:
                return self._rooms[1].remove_match(roomNum)
            except Exception as e:
                print(e)
        elif (type.lower() == "seminar"):
            try:
                return self._rooms[2].remove_match(roomNum)
            except Exception as e:
                print(e)

    '''
    This is a private function to generate a random availability dict to build a database of available rooms
    Argument: none
    Return: a dict of availability for the room
    '''
    def _generate_availability_dict(self):
        DAYLIST = ['M', 'T', 'W', 'TH', 'F', 'S', 'SU']
        TIMELIST = [str(i)+"AM" for i in range(1,13)] + [str(i)+"PM" for i in range(1,13)]
        
        resultDict = {}

        # Select 1 to 5 days for the dict
        chosenDays = random.sample(DAYLIST, k=random.randint(1,5)) #sample doesn't include duplicate

        # For each chosenDays, generate a random list of chosenTimes
        for day in chosenDays:
            chosenTimes = []
            for i in range(random.randint(1,5)): #each day will have 1 to 5 available times
                chosenTimes.append(TIMELIST[random.randint(0, len(TIMELIST)-1)]) #len(TIMELIST)-1 to stay within range of TIMELIST
            chosenTimes = list(set(chosenTimes)) #remove duplicates
            resultDict[day] = chosenTimes

        return resultDict

    '''
    This is a private function to generate a LLL of different room types
    Argument: string type of room and int for the number of that type of room
    Return: a LLL object
    '''
    def _generate_LLL(self, type, num):
        list = LLL()

        for i in range(num):
            roomNum = f"FAB{random.randint(1,50)}"
            occupancy = random.randint(10,80)
            availability = self._generate_availability_dict()

            if type.lower() == "lab":
                computerNum = random.randint(15,40)
                lab = classroom.Lab(roomNum, occupancy, availability, computerNum)
                list.insert(lab)
            
            elif type.lower() == "lecture":
                rating = random.randint(0,5)
                lectureHall = classroom.LectureHall(roomNum, occupancy, availability, rating)
                list.insert(lectureHall)
            
            elif type.lower() == "seminar":
                table = random.choice([True, False])
                seminar = classroom.Seminar(roomNum, occupancy, availability, table)
                list.insert(seminar)

        return list

# def main():
#     lab = classroom.Lab("FAB2", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)
#     lecturehall = classroom.LectureHall("FAB3", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 5)
#     seminar = classroom.Seminar("FAB4", 15, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, True)

#     list = LLL()
#     list.insert(lab)
#     list.insert(lecturehall)
#     list.insert(seminar)

#     desiredSpec = {"movableFurniture":True, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}
#     dayTime = {'M': ["8AM"], 'T': ["9AM"]}

#     print(seminar.match_requirements(desiredSpec, dayTime, 20))

#     rooms = AvailableRooms()
#     rooms.display_all()
#     print('\n\n\n')

#     matches = rooms.find_matches("seminar", desiredSpec, dayTime, 20, 0)
#     for match in matches:
#         print(match)
#     print(len(matches))

# if __name__ == "__main__":
#     main()


