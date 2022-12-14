# designPS11Q1_2022MT12211
# Sourav Patnaik
# Overwriting Dictlist() to store multiple values for same Key
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

class Node:
    def __init__(self, id, name, designation):
        self.id = id
        self.name = name
        self.designation = designation
        self.left = None
        self.right = None

root = None
employees = []
empByID = {}
empByName = Dictlist()
empByDesignation = Dictlist()
inorderTraversal = []
count = 0
inputFile = 'inputPS11Q1.txt'
promptFile = 'promptsPS11Q1.txt'
outputFile = 'outputPS11Q1.txt'

# Insert Employee into BST
def insert(node, obj):
    if node is None:
        # it is the first node in BST
        return Node(obj.id, obj.name, obj.designation)
    if obj.id < node.id:
        node.left = insert(node.left, obj)
    else:
        node.right = insert(node.right, obj)
    return node

# inorder Traversal BST
def inorder(root):
    if root is not None:
        # Traverse left
        inorder(root.left)
        # Traverse root
        #print(root.id, root.name, root.designation + "->\n")
        inorderTraversal.append(root)
        # Traverse right
        inorder(root.right)


def searchEmployeeByID(root, obj):
    if root is not None:
        if obj.id == root.id:
            empByID[obj.id] = root.name
        if obj.id < root.id:
            if root.left == None:
                empByID[obj.id] = "not found"
            return searchEmployeeByID(root.left, obj)
        elif obj.id > root.id:
            if root.right == None:
                empByID[obj.id] = "not found"
            return searchEmployeeByID(root.right, obj)

def searchEmployeeByName(obj):
    namesearch = 0
    for emp in inorderTraversal:
        if obj.name != "" and obj.name.strip().lower() in emp.name.strip().lower():
            empByName[obj.name] = emp
            namesearch = namesearch +1
    if namesearch == 0:
        e1 = Node(0, "not found", "")
        empByName[obj.name] = e1

def searchEmployeeByDesignation(obj):
    dessearch = 0
    for emp in inorderTraversal:
        if obj.designation != "" and obj.designation.lower() in emp.designation.lower():
            empByDesignation[obj.designation] = emp
            dessearch = dessearch +1
    if dessearch == 0:
        e1 = Node(0, "", "not found",)
        empByDesignation[obj.designation] = e1

def clearOutputFile():
    import os
    try:
        os.remove(outputFile)
    except IOError as e:
        print('Could not delete the output file')

def readInputs():
    global count
    with open(inputFile, "r") as file:
        for x in file.readlines():
            parts = x.strip().split(',')
            if (len(parts[0]) == 0 or len(parts[1]) == 0 or len(parts[2]) == 0) or len(parts) != 3:
                print("Formatting error in line: ", count+1)
                exit(1)
            if len(parts) == 3:
                try:
                    new_emp = Node(int(parts[1]), parts[0].strip(), parts[2].strip())
                    employees.append(new_emp)
                    count += 1
                except ValueError:
                    print("Missing employee ID in line: ", count+1)
                    exit(1)
            else:
                print("Formatting error in line: ", count+1)
                exit(1)

def searchResult():
    with open(promptFile, "r") as file:
        count = 0
        for x in file.readlines():
            parts = x.strip().split(':')
            if len(parts) != 2:
                print("Incorrect File format in file: ",
                      file.name,  "line: ", count+1)
                exit(1)
            if parts[0] == "Search ID":
                try:
                    id = int(parts[1])
                    searchById = Node(id, "", "")
                    searchEmployeeByID(root, searchById)
                except ValueError:
                    print("Missing employee ID in file: ",
                          file.name, "line: ", count+1)
                    exit(1)
            elif parts[0] == "Search Name":
                searchByName = Node(0, parts[1].strip(), "")
                searchEmployeeByName(searchByName)
            elif parts[0] == "Search Designation":
                searchByDesignation = Node(0, "", parts[1].strip())
                searchEmployeeByDesignation(searchByDesignation)
            else:
                print("Incorrect File format in file: ",
                      file.name,  "line: ", count+1)
                exit(1)

def writeOutput():
    with open(outputFile, "a+") as f:
        f.write("------------- Search by ID ---------------\n")
        for eid, ename in empByID.items():
            printstr = str(eid) + ' ' + ename + '\n'
            f.write(printstr)
        for key, val in empByName.items():
            s = "----------- Search by Name: " + key + " -------------" + '\n'
            f.write(s)
            for emp in val:
                if emp.name == "not found":
                    f.write("not found\n")
                else:
                    printstr = emp.name + '\n'
                    f.write(printstr)
        for key, val in empByDesignation.items():
            s = "----------- List Employees by Designation: " + key + " -------------" + '\n'
            f.write(s)
            for emp in val:
                if emp.designation == "not found":
                    f.write("not found\n")
                else:
                    printstr = emp.name + ' ' + str(emp.id) + '\n'
                    f.write(printstr)
        f.close()

def start():
    global count
    global root
    global employees
    global empByID
    global empByName
    global empByDesignation
    global inorderTraversal
    # clear output file
    clearOutputFile()
    # read Employee details from PS11Q1.txt file
    readInputs()
    # insert Employee into BST
    for emp in employees:
        #print(emp.id, emp.name, emp.designation)
        root = insert(root,emp)

    # open outputPS11Q1.txt and write the output
    with open(outputFile, "a+") as f:
        f.write(str(count) + " Binary Tree Created with the employee details (from file PS11Q1.txt)" + '\n')
        f.close()

    # inorder will store Employee details in inorder manner into inorderTraversal[] 
    # which will be used by searchEmployeeByNameAndDesignation()
    inorder(root)
    # open promptsPS11Q1.txt and search Employee by ID, Name and Designation
    searchResult()
    # write output to output file
    writeOutput()
    
start()
