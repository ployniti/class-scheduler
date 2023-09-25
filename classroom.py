# This file contains the code for the hierarchy of different classroom types derived from a base classroom class.

### CLASSROOM ###
class Classroom:
    '''
    Default constructor
    Argument: none
    Return: none
    '''
    def __init__(self):
        self._specification = None #a dictionary or array of specification for the room ex. {"movableFurniture":True, "zoomEnabled":True}
        self._roomNum = None
        self._type = None
        self._occupancy = 0
        self._availability = None #a dictionary of day and time availability ex. {'M': ["10PM", "8AM"], 'T': ["11AM"]}
    
    '''
    Default constructor with arguments
    Argument: specification dictionary, string of room number, string of room type, occupancy int, and availability dictionary
    Return: none
    '''
    def __init__(self, specDict=None, roomNum=None, occupancy=0, type=None, availabilityDict=None):
        self._specification = specDict
        self._roomNum = roomNum
        self._occupancy = occupancy
        self._type = type
        self._availability = availabilityDict
    
    '''
    Overloaded display operator to display the data of a classroom object
    Argument: none
    Return: a string object
    '''
    def __str__(self):
        return ("Room number: " + str(self._roomNum) + 
                "\nRoom type: " + str(self._type) +
                "\nOccupancy: " + str(self._occupancy) +
                "\nSpecifications: " + str(self._specification) +
                "\nAvailability " + str(self._availability))

    '''
    Overloaded == operator to compare the room number of two class objects
    Argument: another class object
    Return: True or False
    '''
    def __eq__(self, classObj):
        if (self._roomNum == classObj._roomNum):
            return True
        return False
    
    '''
    Overloaded == operator to compare the room number
    Argument: string of room number
    Return: True or False
    '''
    def __eq__(self, roomNum):
        if (self._roomNum == roomNum):
            return True
        return False
    
    '''
    Overloaded != operator to compare the room number of two class objects
    Argument: another class object
    Return: True or False
    '''
    def __ne__(self, classObj):
        if (self._roomNum != classObj._roomNum):
            return True
        return False
    
    '''
    Overloaded != operator to compare the room number
    Argument: string of room number
    Return: True or False
    '''
    def __ne__(self, roomNum):
        if (self._roomNum != roomNum):
            return True
        return False

    '''
    This is a function to compare the requirements from the user with the class object to figure out if its a good match
    Argument: dicts of desired specification and day/time and occupancy int
    Return: an int of the overall match, greater is better
    '''
    def match_requirements(self, desiredSpec, dayTime, occupancy):
        # If the dicts are empty or occupancy equals 0, raise an exception
        if not desiredSpec or not dayTime or occupancy <= 0 :
            raise Exception("No specification, day/time, or occupancy provided for matching.\n")
        
        specMatch = self._compare_spec(desiredSpec)

        timeMatch = self._compare_time(dayTime)

        occupancyMatch = self._occupancy_check(occupancy)

        return len(specMatch) + len(timeMatch) + occupancyMatch
    
    '''
    This is a private function to compare the specifications of the room to a desired specification gathered from the user
    Argument: a dictionary of desired specification
    Return: a set object of the intersection between the two dicts
    '''
    def _compare_spec(self, desiredSpec):
        result = set(self._specification.items()) & set(desiredSpec.items())
        
        return result

    '''
    This is a private function to compare the availability of the room to a desired day and time gathered from the user
    Argument: a dictionary of desired availability
    Return: a set object of the intersection between the two dicts
    '''
    def _compare_time(self, dayTime):
        # Find the matching days in the dicts
        matchedDays = set(self._availability.keys()) & set(dayTime.keys())
        matchedDayTime = {} #final resulting dict

        # For every day in the matching days, iterates over the desired time and see if it's available in the class's availability
        for key in matchedDays:
            matchedTime = []
            for time in dayTime[key]:
                if time in self._availability[key]:
                    matchedTime.append(time)
            if matchedTime: #don't add empty list to the final dict
                matchedDayTime[key] = matchedTime

        return matchedDayTime 
    
    '''
    This is a private function to check if the room's occupancy is greater than or equal to the desired occupancy
    Argument: an int for the desired occupancy
    Return: 1 if greater than or equal to and 0 if not
    '''
    def _occupancy_check(self, occupancy):
        if self._occupancy >= occupancy:
            return 1
        else:
            return 0

### LAB ###
class Lab(Classroom):
    '''
    Default constructor with arguments
    Argument: string of room number, occupancy int, availability dictionary, computer number int, and specification dictionary
    Return: none
    '''
    def __init__(self, roomNum=None, occupancy=0, availabilityDict=None, computerNum=0, specDict=None):
        if not specDict: #if no special specification is provided, all labs will have a particular specification
            specDict = {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}
        super().__init__(specDict, roomNum, occupancy, "Computer lab", availabilityDict) #call base class constructor with hardcoded room type
        self._computerNum = computerNum
    
    '''
    Overloaded display operator to display the data of a lab object
    Argument: none
    Return: a string object
    '''
    def __str__(self):
        return super().__str__() + "\nComputer numbers: " + str(self._computerNum)
    
    '''
    This is a function to check if the lab has enough computers for the class
    Argument: an int for the desired computer numbers
    Return: 1 if greater than or equal to and 0 if not
    '''
    def computer_num_check(self, num):
        if num <= 0:
            raise Exception("Please specify a number of computers greater than 0.\n")
        
        if self._computerNum >= num:
            return 1
        else:
            return 0

### LECTUREHALL ###
class LectureHall(Classroom):
    '''
    Default constructor with arguments
    Argument: string of room number, occupancy int, availability dictionary, rating int, and specification dictionary
    Return: none
    '''
    def __init__(self, roomNum=None, occupancy=0, availabilityDict=None, rating=0, specDict=None):
        if not specDict: #if no special specification is provided, all lecture halls will have a particular specification
            specDict = {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":False}
        super().__init__(specDict, roomNum, occupancy, "Lecture hall", availabilityDict) #call base class constructor with hardcoded room type

        if (rating < 0 or rating > 5 ):
            raise Exception("Please specify a number between 0 and 5.\n")
        self._acousticRating = rating
    
    '''
    Overloaded display operator to display the data of a lab object
    Argument: none
    Return: a string object
    '''
    def __str__(self):
        return super().__str__() + "\nAcoustic rating: " + str(self._acousticRating)
    
    '''
    This is a function to check if the acousting rating of the hall is good enough
    Argument: an int for the desired rating
    Return: 1 if greater than or equal to and 0 if not
    '''
    def acoustic_check(self, num):
        if num < 0 or num > 5:
            raise Exception("Please specify a number between 0 and 5.\n")
        
        if self._acousticRating >= num:
            return 1
        else:
            return 0

### SEMINAR ###
class Seminar(Classroom):
    '''
    Default constructor with arguments
    Argument: string of room number, occupancy int, availability dictionary, round table boolean, and specification dictionary
    Return: none
    '''
    def __init__(self, roomNum=None, occupancy=0, availabilityDict=None, roundTable=False, specDict=None):
        if not specDict: #if no special specification is provided, all lecture halls will have a particular specification
            specDict = {"movableFurniture":True, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}
        super().__init__(specDict, roomNum, occupancy, "Seminar room", availabilityDict) #call base class constructor with hardcoded room type

        self._roundTable = roundTable
    
    '''
    Overloaded display operator to display the data of a seminar object
    Argument: none
    Return: a string object
    '''
    def __str__(self):
        if (self._roundTable):
            return super().__str__() + "\nRound table: Yes"
        return super().__str__() + "\nRound table: No"
    
    '''
    This is a function to check if the table style match the desired specification
    Argument: a boolean whether a round table is needed
    Return: 1 if matched, 0 if not matched
    '''
    def table_check(self, table):       
        if self._roundTable == table:
            return 1
        else:
            return 0

# def main():
#     desiredSpec = {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}
#     dayTime = {'M': ["8AM"], 'T': ["9AM"]}
#     dayTimeEmpty = {}
#     classroom = Classroom({"movableFurniture":False, "zoomEnabled":False, "hasProjector":True, "hasWhiteboard":False}, 
#                           "FAB1", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]})
#     lab = Lab("FAB2", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)
#     lecturehall = LectureHall("FAB3", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 5)
#     seminar = Seminar("FAB4", 15, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, True)
#     print(seminar)
#     print(seminar != lecturehall)
#     result = classroom.match_requirements(desiredSpec, dayTimeEmpty, 15)
#     print(result)

# if __name__ == "__main__":
#     main()
