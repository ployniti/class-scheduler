# This is the file containing pytests for the LNode and LLL classes

import LLL
import pytest

### LNODE ###
'''
Test the creation of a LNode object
'''
def test_LNode_creation(LNodeFixture, labFixture):
    assert LNodeFixture._class == labFixture
    assert LNodeFixture._next == None

'''
Test set_next and get_next
'''
def test_set_get_next(LNodeFixture, lectureHallFixture):
    # Initial _next is None
    assert LNodeFixture.get_next() == None
    
    # Set _next to a new LNode object
    nextNode = LLL.LNode(lectureHallFixture)
    LNodeFixture.set_next(nextNode)

    # _next should now be the new LNode object
    assert LNodeFixture.get_next() == nextNode

'''
Test get_class
'''
def test_get_class(LNodeFixture, labFixture):
    assert LNodeFixture.get_class() == labFixture

'''
Test match_requirements
'''
def test_match_requirements(LNodeFixture):
    assert type(LNodeFixture.match_requirements({"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}, {'M': ["8AM"], 'T': ["9AM"]}, 20)) == int

### LLL ###
'''
Test the creation of a LLL object
'''
def test_LLL_creation():
    list = LLL.LLL()
    assert list._head == None

'''
Test get_head
'''
def test_get_head(lectureHallFixture):
    list = LLL.LLL()
    assert list.get_head() == None #empty LLL

    list.insert(lectureHallFixture)
    assert list.get_head() != None

'''
Test the display_all function of a LLL for raising exception when the object is empty
'''
def test_display_all_exception():
    list = LLL.LLL()
    with pytest.raises(Exception, match="List is empty.\n"): 
        list.display_all()

'''
Test the insert function of a LLL for raising exception when an empty object is passed
'''
def test_insert_exception():
    list = LLL.LLL()
    with pytest.raises(Exception, match="Empty class object passed.\n"): 
        list.insert(None)

'''
Test the insert function of a LLL
'''
def test_insert(labFixture):
    list = LLL.LLL()
    list.insert(labFixture)
    assert list._head != None

'''
Test find_matches function of a LLL for raising exceptions
'''
def test_find_matches_exception(labFixture):
    list = LLL.LLL()

    # List is empty
    with pytest.raises(Exception, match="List is empty.\n"): 
        list.find_matches({"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}, {'M': ["8AM"], 'T': ["9AM"]}, 20, 10)
    
    list.insert(labFixture)
    # Empty dicts
    with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
        list.find_matches({}, {'M': ["8AM"], 'T': ["9AM"]}, 20, 10)
    
    with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
        list.find_matches({"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}, {}, 20, 10)
    
    # Zero occupancy
    with pytest.raises(Exception, match="No specification, day/time, or occupancy provided for matching.\n"): 
        list.find_matches({"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}, {'M': ["8AM"], 'T': ["9AM"]}, 0, 10)

'''
Test find_matches function of a LLL
'''
def test_find_matches_exception(labFixture):
    llist = LLL.LLL()
    llist.insert(labFixture)
    
    # Check that a list is returned when valid arguments are provided
    assert isinstance(llist.find_matches({"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":True}, 
                                         {'M': ["8AM"], 'T': ["9AM"]}, 20, 10), list)

'''
Test the remove_match function of a LLL for raising exceptions
'''
def test_remove_match_exception(seminarFixture):
    list = LLL.LLL()

    # List is empty
    with pytest.raises(Exception, match="List is empty.\n"): 
        list.remove_match("FAB2")
    
    # Empty string passed in
    list.insert(seminarFixture)
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        list.remove_match("")

'''
Test the remove_match function of a LLL
'''
def test_remove_match(seminarFixture, labFixture, lectureHallFixture):
    list = LLL.LLL()

    # Remove one and only node
    list.insert(seminarFixture)
    assert list.remove_match("WRONG") == False #no match
    assert list.remove_match("FAB4") == True
    assert list._head == None

    # Remove middle node
    list.insert(seminarFixture)
    list.insert(labFixture)
    list.insert(lectureHallFixture)
    assert list.remove_match("FAB2") == True
    assert list._head != None

    # Remove last node
    assert list.remove_match("FAB4") == True
    assert list._head != None

### AVAILABLEROOMS ###
'''
Test the creation of a AvailableRooms object
'''
def test_AvailableRooms_creation():
    rooms = LLL.AvailableRooms()
    assert len(rooms._rooms) == 3 #an np.array of len 3 for the 3 types of rooms

'''
Test the display_all function of a AvailableRooms for raising exception when the LLLs are empty
'''
def test_display_all_exception():
    rooms = LLL.AvailableRooms(0,0,0)

    # Empty array of LLL
    with pytest.raises(Exception, match="No available rooms.\n"): 
        rooms.display_all()

'''
Test the find_matches function of a AvailableRooms for raising exception
'''
def test_find_matches_exception():
    rooms = LLL.AvailableRooms(0,0,0)

    # Empty array of LLL
    with pytest.raises(Exception, match="No available rooms.\n"): 
        rooms.find_matches("lab", {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":False}, {'M': ["8AM"], 'T': ["9AM"]}, 20, 10)
    
    rooms = LLL.AvailableRooms()
    # Empty string supplied
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        rooms.find_matches("", {"movableFurniture":False, "zoomEnabled":True, "hasProjector":True, "hasWhiteboard":False}, {'M': ["8AM"], 'T': ["9AM"]}, 20, 10)

'''
Test the remove_room function of a AvailableRooms for raising exception
'''
def test_remove_room_exception():
    rooms = LLL.AvailableRooms(0,0,0)

    # Empty array of LLL
    with pytest.raises(Exception, match="No available rooms.\n"): 
        rooms.remove_room("lab", "FAB1")
    
    rooms = LLL.AvailableRooms()
    # Empty string supplied
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        rooms.remove_room("", "FAB1")
    
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        rooms.remove_room("lab", "")
    
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        rooms.remove_room("", "")
