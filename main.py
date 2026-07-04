import os
from pathlib import Path

def createfile():
    try:
        name = input("Enter the name of file you want create:- ")
        path = Path(name)
        if not path.exists():
            with open(name,"w") as fs:
                data = input("Enter what you want to write in the file:- ")
                fs.write(data)
                print(data)
                print("File is created Successfully")
        else:
            print("ERROR, File already exists")
    except Exception as err:
        print(f"Error occured as {err}")

def readfile():
    try:
        name = input("Enter the name of the file you want to read:- ")
        path = Path(name)
        if path.exists():
            with open(name,"r") as fs:
             content = fs.read()
            print(content)
            print("File is successfully read")
        else:
            print("ERROR, File does not exists")
    except Exception as err:
        print(f"Error occured as {err}")

def updatefile():
    name = input("Enter the name of the file you want to update:- ")
    path = Path(name)
    if path.exists():
        print("3 OPTIONS TO UPDATE THE FILE:- ")
        print("ENTER 1 TO RENAME THE FILE")
        print("ENTER 2 TO OVERWRITE THE FILE")
        print("ENTER 3 TO APPEND THE FILE")
    input2 = int(input("ENTER YOUR CHOICE:- "))

    if input2 == 1 :
        try:
            path = Path(name)
            data = input("Enter to rename your file:- ")
            rename = path.rename(data)
            print(rename)
            print("File is renamed successfully")
        except Exception as err:
            print(f"Error occured as {err}")
    elif input2 == 2:
        try:
            with open(name,"w") as fs:
                data = input("Enter what you want to overwrite in the file:- ")
                fs.write(data)
                print(data)
                print("File is overwritten successfully")
        except Exception as err:
            print(f"Error occured as {err}")
    elif input2 == 3:
        try:
            with open(name,"a") as fs:
                data = input("Enter what you want to append in the file:- ")
                fs.write(data)
                print("  \n" + data)
                print("File is appended successfully")
        except Exception as err:
            print(f"Error occured as {err}")

def deletefile():
    try:
        name = input("Enter your file name:- ")
        path = Path(name)
        if path.exists():
            path.unlink()
            print("File is deleted successfully")
        else :
            print("The file does not exists")
    except Exception as err:
        print(f"Error occured as {err}")

print("ENTER 1 FOR CREATING A FILE")
print("ENTER 2 FOR READING A FILE")
print("ENTER 3 FOR UPDATING A FILE")
print("ENTER 4 FOR DELETING A FILE")

input1 = int(input("Enter your choice:- "))

if input1 == 1:
    createfile()

elif input1 == 2:
    readfile()

elif input1 == 3:
    updatefile()

elif input1 == 4:
    deletefile()