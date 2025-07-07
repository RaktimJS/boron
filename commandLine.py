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




"""
Checking cache if "path" already exists for data and schema integrity
and ease of usage
"""

def cacheFileCheck():
        filePathList = []
        filePath = jsonValidity()


        """
        Checking existence of 'cache.json' and loading the data of the same file in
        variable 'data' if the file exists. Otherwise, an error message is prompted
        """

        try:
                with open("cache.json", "r") as file:
                        data = json.load(file)
        except FileNotFoundError:
                print("'cache.json' not found. Please create it with a valid JSON array structure.")
                return
        except json.JSONDecodeError:
                print("'cache.json' seems to have some issue")
                return
        except Exception as e:
                print("Unexpected error occured:", e)
                return

        for i in data:
                try:
                        filePathList.append(os.path.normpath(i["path"]))
                except KeyError:
                        print("Invalid cache format: 'path' key missing in one of the entries.")



        """
        Checking if entered JSON path is already cached. If it is cached, then
        it is assumed that the JSON is already following a schema, considering
        there have been no changes made in 'cache.json' file externally.
        """

if __name__ == "__main__":
        cacheFileCheck()
