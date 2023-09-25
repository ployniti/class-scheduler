# This file contains the code for the TNode and BT classes.

import LLL

### TNODE ###
class TNode:
    '''
    Default constructor with arguments
    Arguments: a string of course name, a class object, or a LLLObj, and an optional parent TNode
    Return: none
    '''
    def __init__(self, courseName, classObj, LLLObj, parent=None):
        self._childList = [] #size 3, list of nodes
        self._parent = parent
        # If no LLLObj is passed, we use the create a new LLLObj and insert the classObj
        if (not LLLObj):
            self._rooms = LLL.LLL()
            try:
                self._rooms.insert(classObj)
            except Exception as e:
                print(e)
        else:
            self._rooms = LLLObj
        self._dataList = [tuple([courseName, self._rooms])] #size 2, list of tuples with course name and rooms LLL object

    '''
    This is the function to display the node's data in order
    Arguments: boolean value for whether the node is a leaf and the index of data to display if it's not a leaf
    Return: none
    '''
    def display(self, leaf, index=0):

        if (leaf):
            for data in self._dataList:
                print(data[0])
                try:
                    data[1].display_all()
                except Exception as e:
                    print(e)
        else:
            print(self._dataList[index][0])
            try:
                self._dataList[index][1].display_all()
            except Exception as e:
                print(e)

### TREE23 ###
class Tree23:
    '''
    Default constructor with arguments
    Arguments: none
    Return: none
    '''
    def __init__(self):
        self._root = None #a TNode
    
    '''
    This is the wrapper function to insert a course and classObj into the tree
    Arguments: string of course name and a class object
    Return: 1 for success, 0 for failure
    '''
    def insert(self, courseName, classObj):
        if not classObj:
            raise Exception("Empty class object passed.\n")
        elif courseName == " ":
            raise Exception("Empty string object passed.\n")

        # Tree is empty
        if (not self._root):
            self._root = TNode(courseName, classObj, None)
        else:
            self._root = self._insert(self._root, courseName, classObj)
        return 1
    
    '''
    This is the recursive function to insert a course and classObj into the tree
    Arguments: root TNode, string of course name and a class object
    Return: root TNode
    '''
    def _insert(self, root, courseName, classObj):
        # Check if the course already exists in the node's dataList
        # If so, insert into the exisiting LLL rooms object
        for i in range(len(root._dataList)):
            if (courseName == root._dataList[i][0]):
                try:
                    root._dataList[i][1].insert(classObj)
                    return root #for reconnecting
                except Exception as e:
                    print(e)

        # Check if it's a leaf, add data
        if len(root._childList) == 0:
            rooms = LLL.LLL()
            try:
                rooms.insert(classObj)
            except Exception as e:
                print(e)
            root._dataList.append(tuple([courseName, rooms]))
            root._dataList.sort()
            
            # Check if we need to split the node
            if (len(root._dataList) == 3):
                # Split the node
                leftChild = TNode(root._dataList[0][0], None, root._dataList[0][1])
                rightChild = TNode(root._dataList[2][0], None, root._dataList[2][1])
                
                if (root._parent):
                    root._parent._dataList.append(root._dataList[1])
                    root._parent._dataList.sort()
                    leftChild._parent = root._parent
                    root._parent._childList.append(leftChild)
                    rightChild._parent = root._parent
                    root._parent._childList.append(rightChild)
                    root._parent._childList.sort(key=lambda x: x._dataList[-1][0])
                    return None
                else:
                    root._dataList = [root._dataList[1]]
                    leftChild._parent = root
                    rightChild._parent = root
                    root._childList = [leftChild, rightChild]
            return root
        
        # If node is not a leaf, find the child that is a leaf
        # If courseName is bigger than the largest courseName in the data list, insert at the last child in the list
        elif courseName > root._dataList[-1][0]: #[0] index is for the courseName key in the tuple
            hold = root._childList[-1]
            temp = self._insert(root._childList[-1], courseName, classObj) #indexing might not be consistent...
            for i in range(len(root._childList)):
                if root._childList[i] == hold:
                    root._childList[i] = temp
        # If not, find the smaller node to add to
        else:
            for i in range(len(root._dataList)):
                if courseName < root._dataList[i][0]:
                    hold = root._childList[i]
                    temp = self._insert(root._childList[i], courseName, classObj)
                    for i in range(len(root._childList)):
                        if root._childList[i] == hold:
                            root._childList[i] = temp
                    break

        # Remove child that is marked None because it has been split from the childList
        root._childList = [child for child in root._childList if child != None]

        # Check if we need clean up parent on the way out
        if (len(root._dataList) == 3):
            # Split the node
            leftChild = TNode(root._dataList[0][0], None, root._dataList[0][1])
            rightChild = TNode(root._dataList[2][0], None, root._dataList[2][1])
            
            leftChild._childList = [root._childList[0], root._childList[1]]
            rightChild._childList = [root._childList[2], root._childList[3]]
            
            if (root._parent):
                root._parent._dataList.append(root._dataList[1])
                leftChild._parent = root._parent
                root._parent._childList.append(leftChild)
                rightChild._parent = root._parent
                root._parent._childList.append(rightChild)
                root._parent._childList.sort(key=lambda x: x._dataList[-1][0])
            else:
                root._dataList = [root._dataList[1]]
                leftChild._parent = root
                rightChild._parent = root
                root._childList = [leftChild, rightChild]
        return root
    
    '''
    This wrapper function to display all nodes in the Tree23 object
    Argument: none
    Return: 1 for success, 0 for failure
    '''
    def display_all(self):
        if (not self._root):
            raise Exception("Tree is empty.\n")
        
        # In order traversal to display
        return self._display_all(self._root)
    
    '''
    This recursive function to display all nodes in the Tree23 object
    Argument: none
    Return: 1 for success, 0 for failure
    '''
    def _display_all(self, root):
        val = 0
        # Base case is at the leaf, no children
        if (len(root._childList) == 0):
            root.display(True)
            return 1
        
        val += self._display_all(root._childList[0]) #smallest child

        root.display(False, 0) #display first data of parent, if with 3 children

        val += self._display_all(root._childList[1]) #middle child

        if (len(root._childList) == 3):
            root.display(False, 1) #display second data of parent, if with 3 children
            val += self._display_all(root._childList[2]) #largest child
        return val
    
    '''
    This wrapper function to find a match in the course name
    Argument: string of courseName to find
    Return: the tuple of the matching data
    '''
    def retrieve_class(self, courseName):
        if (not self._root):
            raise Exception("Tree is empty.\n")
        elif courseName == " ":
            raise Exception("Empty string object passed.\n")
        
        return self._retrieve_class(self._root, courseName)
    
    '''
    This recursive function to find a match in the course name
    Argument: string of courseName to find
    Return: the tuple of the matching data
    '''
    def _retrieve_class(self, root, courseName):
        
        for i in range(len(root._dataList)):
            if (courseName == root._dataList[i][0]):
                return root._dataList[i]
        
        if (len(root._childList) == 0): #no match found
            return None
        
        if courseName > root._dataList[-1][0]:
            return self._retrieve_class(root._childList[-1], courseName)

        else:
            for i in range(len(root._dataList)):
                if courseName < root._dataList[i][0]:
                    return self._retrieve_class(root._childList[i], courseName)
    
    '''
    This function returns the root of the Tree23 object (mainly for testing)
    Argument: none
    Return: root TNode of the Tree23 object
    '''
    def get_root(self):
        return self._root

# def main():
#     lab1 = classroom.Lab("FAB2", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)
#     lab2 = classroom.Lab("FAB99", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)
#     lab3 = classroom.Lab("FAB1", 20, {'M': ["10PM", "8AM"], 'T': ["11AM"], 'W': ["5PM"]}, 40)
#     tree = Tree23()
#     tree.insert("CS302", lab1)
#     tree.insert("CS302", lab2)
#     tree.insert("CS486", lab2)
#     tree.insert("CS580", lab3)
#     tree.insert("CS333", lab2) #Lose the root when inserting this, don't need to return?
#     tree.insert("CS323", lab1)
#     tree.insert("CS312", lab2)
#     tree.insert("CS308", lab2)
#     tree.insert("CS308", lab2)
#     tree.get_root()._childList[1]._dataList[0][1].display_all()
#     classResult = tree.retrieve_class("CS302")
#     print(classResult[1].display_all())
#     tree.display_all()
#     print(tree.get_root()._childList[1]._dataList)
#     node = TNode("CS302", lab1)
#     node.display()
#     node.insert("CS486", lab2)
#     node.display()
#     node.insert("CS580", lab3)
#     node.display()

# if __name__ == "__main__":
#     main()
