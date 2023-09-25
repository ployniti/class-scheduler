# This is the file containing pytests for the TNode and Tree23 classes

import pytest

### TNODE ###
'''
Test the creation of a TNode object with classObj
'''
def test_TNode_creation(TNodeFixtureClassObj):
    assert len(TNodeFixtureClassObj._dataList) == 1
    assert type(TNodeFixtureClassObj._dataList[0]) == tuple
    assert TNodeFixtureClassObj._dataList[0][0] == "CS302"

'''
Test the creation of a TNode object with LLLObj
'''
def test_TNode_creation(TNodeFixtureLLLObj):
    assert len(TNodeFixtureLLLObj._dataList) == 1
    assert type(TNodeFixtureLLLObj._dataList[0]) == tuple
    assert TNodeFixtureLLLObj._dataList[0][0] == "CS302"

### TREE23 ###
'''
Test the creation of a Tree23 object
'''
def test_Tree23_creation(Tree23Fixture):
    assert Tree23Fixture._root == None

'''
Test insert function of a Tree23 object for raising exception when invalid arguments are passed
'''
def test_insert_exception(Tree23Fixture, seminarFixture):
    with pytest.raises(Exception, match="Empty class object passed.\n"):
        Tree23Fixture.insert("CS302", None)
    
    with pytest.raises(Exception, match="Empty string object passed.\n"):
        Tree23Fixture.insert(" ", seminarFixture)

'''
Test insert function of a Tree23 object
'''
def test_insert(Tree23Fixture, seminarFixture):
    assert Tree23Fixture.insert("CS302", seminarFixture) == 1

'''
Test the display_all function of a Tree23 for raising exception when the object is empty
'''
def test_display_all_exception(Tree23Fixture):
    with pytest.raises(Exception, match="Tree is empty.\n"): 
        Tree23Fixture.display_all()

'''
Test the display_all function of a Tree23
'''
def test_display_all(Tree23Fixture, seminarFixture):
    Tree23Fixture.insert("CS302", seminarFixture)
    assert Tree23Fixture.display_all() == 1

'''
Test the retrieve_class function of a Tree23 for raising exceptions
'''
def test_retrieve_class_exception(Tree23Fixture, seminarFixture):
    with pytest.raises(Exception, match="Tree is empty.\n"): 
        Tree23Fixture.retrieve_class("CS302")

    Tree23Fixture.insert("CS302", seminarFixture)
    with pytest.raises(Exception, match="Empty string object passed.\n"): 
        Tree23Fixture.retrieve_class(" ")

'''
Test the retrieve_class function of a Tree23
'''
def test_retrieve_class(Tree23Fixture, seminarFixture):
    Tree23Fixture.insert("CS302", seminarFixture)
    assert type(Tree23Fixture.retrieve_class("CS302")) == tuple #returns a tuple
    assert Tree23Fixture.retrieve_class("CS302")[0] == "CS302"
    assert Tree23Fixture.retrieve_class("CS999") == None #no match returns None
