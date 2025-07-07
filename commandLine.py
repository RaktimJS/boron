# This script serves as the entry point to the program.




import os
import json

os.system('cls' if os.name == "nt" else "clear")





"""
Checking existence, and extension, if a file exists in the entered path
"""

def fileTypeExistenceVerify():
        while True:
                filePath = input("Enter the JSON path: ").strip()

                try:
                        if filePath:
                                filePath = os.path.normpath(filePath)
                        else:
                                print("Empty input not supported\n")
                                continue

                        if os.path.isfile(filePath):
                                name, extension = os.path.splitext(filePath)

                                if extension.lower() == ".json":
                                        return filePath
                                else:
                                        print("File isn't JSON\n")
                        else:
                                print("The entered path is invalid\n")
                except EOFError:
                        print("Empty input not supported\n")


"""
Checking validity of a JSON file, i.e, if the JSON is structured
or not
"""

def jsonValidity():
        filePath = fileTypeExistenceVerify()

        try:
                with open(filePath, "r") as f:
                        json.load(f)
                        return filePath
        except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}\n")
                return False
        except Exception as e:
                print(f"Error reading file: {e}\n")
                return False
"""
Checking validity of a JSON file, i.e, if the JSON is structured
or not
"""

def jsonValidity():
        filePath = fileTypeExistenceVerify()

        try:
                with open(filePath, "r") as f:
                        json.load(f)
                        return filePath
        except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}\n")
                return False
        except Exception as e:
                print(f"Error reading file: {e}\n")
                return False
