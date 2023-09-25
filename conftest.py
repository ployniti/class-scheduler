import classroom
import LLL
import table
import pytest

### CLASSROOM ###
@pytest.fixture
def classroomFixture():
    return classroom.Classroom(
        {"movableFurniture":False, "zoomEnabled":False, "hasProjector":True, "hasWhiteboard":False}, 
         "FAB1", 20, "Classroom", {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]})

@pytest.fixture
def labFixture():
    return classroom.Lab("FAB2", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)

@pytest.fixture
def lectureHallFixture():
    return classroom.LectureHall("FAB3", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 3)

@pytest.fixture
def seminarFixture():
    return classroom.Seminar("FAB4", 10, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, True)

### LLL ###
@pytest.fixture
def LNodeFixture(labFixture):
    return LLL.LNode(labFixture)

### TABLE ###
@pytest.fixture
def TNodeFixtureClassObj(labFixture):
    return table.TNode("CS302", labFixture, None)

@pytest.fixture
def TNodeFixtureLLLObj(labFixture):
    rooms = LLL.LLL()
    rooms.insert(labFixture)
    return table.TNode("CS302", None, rooms)

@pytest.fixture
def Tree23Fixture():
    return table.Tree23()
