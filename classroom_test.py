# This is the file containing pytests for the classroom and its derived classes

import classroom
import pytest

### CLASSROOM ###
'''
Test the creation of a Classroom object
'''
def test_classroom_creation(classroomFixture):
    assert classroomFixture._specification == {"movableFurniture":False, "zoomEnabled":False, "hasProjector":True, "hasWhiteboard":False}
    assert classroomFixture._roomNum == "FAB1"
    assert classroomFixture._occupancy == 20
    assert classroomFixture._type == "Classroom"
    assert classroomFixture._availability == {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}

'''
Test the __eq__ operator with class objects
'''
def test_eq_obj_operator(seminarFixture, lectureHallFixture, labFixture):
    fixtures = [seminarFixture, lectureHallFixture, labFixture]

    # Same object type
    for i in range(len(fixtures)):
        assert (fixtures[i] == fixtures[i]) == True

    # Different object type
    assert (seminarFixture == lectureHallFixture) == False
    assert (seminarFixture == labFixture) == False

    assert (lectureHallFixture == seminarFixture) == False
    assert (lectureHallFixture == labFixture) == False

    assert (labFixture == lectureHallFixture) == False
    assert (labFixture == seminarFixture) == False

'''
Test the __eq__ operator with string
'''
def test_eq_str_operator(seminarFixture, lectureHallFixture, labFixture):
    fixtures = [labFixture, lectureHallFixture, seminarFixture]
    roomNums = ["FAB2", "FAB3", "FAB4"]

    # Correct roomNum strings
    for i in range(len(fixtures)):
        assert (fixtures[i] == roomNums[i]) == True

    # Incorrect roomNum strings
    assert (seminarFixture == "FAB2") == False
    assert (seminarFixture == "FAB3") == False

    assert (lectureHallFixture == "FAB2") == False
    assert (lectureHallFixture == "FAB4") == False

    assert (labFixture == "FAB3") == False
    assert (labFixture == "FAB4") == False

'''
Test the __ne__ operator with class objects
'''
def test_ne_obj_operator(seminarFixture, lectureHallFixture, labFixture):
    fixtures = [seminarFixture, lectureHallFixture, labFixture]

    # Same object type
    for i in range(len(fixtures)):
        assert (fixtures[i] != fixtures[i]) == False

    # Different object type
    assert (seminarFixture != lectureHallFixture) == True
    assert (seminarFixture != labFixture) == True

    assert (lectureHallFixture != seminarFixture) == True
    assert (lectureHallFixture != labFixture) == True

    assert (labFixture != lectureHallFixture) == True
    assert (labFixture != seminarFixture) == True

'''
Test the __ne__ operator with string
'''
def test_ne_str_operator(seminarFixture, lectureHallFixture, labFixture):
    fixtures = [labFixture, lectureHallFixture, seminarFixture]
    roomNums = ["FAB2", "FAB3", "FAB4"]

    # Correct roomNum strings
    for i in range(len(fixtures)):
        assert (fixtures[i] != roomNums[i]) == False

    # Incorrect roomNum strings
    assert (seminarFixture != "FAB2") == True
    assert (seminarFixture != "FAB3") == True

    assert (lectureHallFixture != "FAB2") == True
    assert (lectureHallFixture != "FAB4") == True

    assert (labFixture != "FAB3") == True
    assert (labFixture != "FAB4") == True

'''
Test the match_requirements function for raising exception when invalid arguments are passed
'''
def test_match_requirements_exception(classroomFixture):
    errorOccupancyList = [0, -1]
    validOccupancy = 50
    validDayTimeDict = {'M': ["8AM"], 'T': ["9AM"]}
    validSpecDict = {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}
    errorDict = {}

    # Testing 0 or negative occupancy argument
    for val in errorOccupancyList:
        with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
            classroomFixture.match_requirements(validSpecDict, validDayTimeDict, val)
    
    # Testing errorDict for desiredSpec argument
    with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
            classroomFixture.match_requirements(errorDict, validDayTimeDict, validOccupancy)
    
    # Testing errorDict for dayTime argument
    with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
            classroomFixture.match_requirements(validSpecDict, errorDict, validOccupancy)
    
    # Testing all invalid arguments
    for val in errorOccupancyList:
        with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
            classroomFixture.match_requirements(errorDict, errorDict, val)

'''
Test the match_requirements function for the correct return value with valid arguments
'''
def test_match_requirements(classroomFixture):
    validOccupancy = 50
    validDayTimeDict = {'M': ["8AM"], 'T': ["9AM"]}
    validSpecDict = {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}

    assert type(classroomFixture.match_requirements(validSpecDict, validDayTimeDict, validOccupancy)) == int

### LAB ###
'''
Test the creation of a Lab object
'''
def test_lab_creation(labFixture):
    assert labFixture._specification == {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True} #the default spec for lab
    assert labFixture._roomNum == "FAB2"
    assert labFixture._occupancy == 20
    assert labFixture._type == "Computer lab"
    assert labFixture._availability == {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}
    assert labFixture._computerNum == 40

'''
Test the computer_num_check function for raising exception when invalid arguments are passed
'''
def test_computer_num_check_exception(labFixture):
    errorNumList = [0, -1]

    # Testing 0 or negative num argument
    for val in errorNumList:
        with pytest.raises(Exception, match="Please specify a number of computers greater than 0.\n"): 
            labFixture.computer_num_check(val)

'''
Test the computer_num_check function for the correct return value with valid arguments
'''
def test_computer_num_check(labFixture):
    assert labFixture.computer_num_check(5) == 1 #required num is less than _computerNum
    assert labFixture.computer_num_check(45) == 0 #required num is greater than _computerNum

### LECTUREHALL ###
'''
Test the creation of a LectureHall object
'''
def test_lecturehall_creation(lectureHallFixture):
    assert lectureHallFixture._specification == {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":False} #the default spec for lecture hall
    assert lectureHallFixture._roomNum == "FAB3"
    assert lectureHallFixture._occupancy == 20
    assert lectureHallFixture._type == "Lecture hall"
    assert lectureHallFixture._availability == {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}
    assert lectureHallFixture._acousticRating == 3

'''
Test raising exception with the creation of a LectureHall object with rating > 5 and rating < 0
'''
def test_lecturehall_creation_exception():
    with pytest.raises(Exception, match="Please specify a number between 0 and 5.\n"):
        _errorCreation = classroom.LectureHall("FAB3", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, -1)
    
    with pytest.raises(Exception, match="Please specify a number between 0 and 5.\n"):
        _errorCreation = classroom.LectureHall("FAB3", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 6)

'''
Test the acoustic_check function for raising exception when invalid arguments are passed
'''
def test_acoustic_check_exception(lectureHallFixture):
    errorNumList = [-1, 6]

    # Testing negative and greater than 5 rating argument
    for val in errorNumList:
        with pytest.raises(Exception, match="Please specify a number between 0 and 5.\n"): 
            lectureHallFixture.acoustic_check(val)

'''
Test the acoustic_check function for the correct return value with valid arguments
'''
def test_acoustic_check(lectureHallFixture):
    assert lectureHallFixture.acoustic_check(2) == 1 #required rating is less than _acousticRating
    assert lectureHallFixture.acoustic_check(5) == 0 #required rating is greater than _acousticRating

### SEMINAR ###
'''
Test the creation of a Seminar object
'''
def test_seminar_creation(seminarFixture):
    assert seminarFixture._specification == {"movableFurniture":True, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True} #the default spec for lecture hall
    assert seminarFixture._roomNum == "FAB4"
    assert seminarFixture._occupancy == 10
    assert seminarFixture._type == "Seminar room"
    assert seminarFixture._availability == {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}
    assert seminarFixture._roundTable == True

'''
Test the table_check function for raising exception when invalid arguments are passed
'''
def test_table_check(seminarFixture):
    assert seminarFixture.table_check(True) == 1 #required spec is a match
    assert seminarFixture.table_check(False) == 0 #rrequired spec is NOT a match
