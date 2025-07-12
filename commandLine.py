# This script serves as the entry point to the program.




import os
import json

import schema

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
                                print("Invalid Path\n")
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
                        data = json.load(f)

                        if isinstance(data, dict):
                                return filePath
                        else:
                                raise ValueError("Array-type JSON not supported")
        except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}\n")
                return
        except Exception as e:
                print(f"Error reading file: {e}\n")
                return




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
                        cacheData = json.load(file)
        except FileNotFoundError:
                print("'cache.json' not found. Please create it with a valid JSON array structure.")
                return
        except json.JSONDecodeError:
                print("'cache.json' seems to have some issue")
                return
        except Exception as e:
                print("Unexpected error:", e)
                return


        for i in cacheData:
                try:
                        filePathList.append(os.path.normpath(i["path"]))
                except KeyError:
                        print("Invalid cache format: 'path' key missing in one of the entries.")



        """
        Checking if entered JSON path is already cached. If it is cached, then
        it is assumed that a schema has been defined and the JSON file is following
        the schema, considering there have been no changes made in 'cache.json'
        file externally.
        """


        if filePath in filePathList:
                try:
                        with open(filePath, "r") as file:
                                data = json.load(file)
                except json.JSONDecodeError as e:
                        print("Error in the JSON file:", e)
                except Exception as e:
                        print("Unexpected error:", e)


                """
                Fetching schema of the JSON when its path is found in cache. For
                fetching the schema, the program looks at the ver first key-value
                pair in the JSON, and fetches the data and converts it into a
                dictionary data type. When a command is passed, the program will
                try to match the syntax with the dictionary. If any mismatch is
                detected, the program will through an error. 
                """

                jsonSchema = schema.fetcher(filePath)        # Fetches schema of the cached JSON
                # Data insertion function to be called here
        elif filePath != None:
                """
                Schema definition when the file is uncached
                """

                print("Schema definition required")
        else:
                print("Garbage")




if __name__ == "__main__":
        cacheFileCheck()
