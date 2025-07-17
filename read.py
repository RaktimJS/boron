"""
This module contains functions for data query.

NOTE: v1 doesn't support data query
"""




import json  # Import the built-in JSON module for reading and parsing JSON files


def loadJson(filePath):
        """
        Load a JSON file and return its full dict content.
        Returns (dataDict, None) on success, or (None, errorMessage) on failure.
        """
        try:
                # Try to open the file at the given path in read mode
                with open(filePath, 'r') as fileHandle:
                        # Parse the file content as JSON
                        parsedJson = json.load(fileHandle)
        except FileNotFoundError:
                # If the file does not exist, return an error message
                return None, f"File not found: '{filePath}'"
        except json.JSONDecodeError as decodeError:
                # If the file is not valid JSON, return an error message with details
                return None, f"Invalid JSON: {decodeError.msg} at line {decodeError.lineno}, column {decodeError.colno}"

        # Check if the parsed JSON is a dictionary (object)
        if not isinstance(parsedJson, dict):
                # If not, return an error message
                return None, "Root JSON must be an object (dictionary of instances)."

        # If everything is fine, return the parsed dictionary and None for error
        return parsedJson, None


def validateSchemaPath(schemaDefinition, keyPathList):
        """
        Walk the schemaDefinition following keyPathList to ensure every key exists.
        Returns None on success, or errorMessage on failure.
        """
        current = schemaDefinition  # Start from the root of the schema
        fullPathList = []  # Keep track of the path as we go deeper
        for key in keyPathList:
                fullPathList.append(key)  # Add the current key to the path
                pathStr = '.'.join(fullPathList[:-1])  # Create a string of the path up to the parent
                if not isinstance(current, dict):
                        # If the current level is not a dictionary, it's an error
                        return f"Schema error: '{pathStr}' should be an object."
                if key not in current:
                        # If the key is not found at this level, return an error
                        if pathStr.strip() == "":
                                return f"Schema error: key '{key}' not defined under '{pathStr}'."
                        else:
                                return f"Schema error: key '{key}' not defined under root."
                current = current[key]  # Move to the next level in the schema
        return  # If all keys are found, return None (success)


def extractValue(dataInstance, keyPathList, fullPathList=None):
        """
        Recursively walk down dataInstance following keyPathList.
        Returns (value, None) on success, or (None, errorMessage) on failure.
        """
        if fullPathList is None:
                fullPathList = []  # Initialize the path if not provided

        if not keyPathList:
                # If there are no more keys to follow, return the current value
                return dataInstance, None

        currentKey = keyPathList[0]  # Get the next key to look for
        newFullPath = fullPathList + [currentKey]  # Update the path
        pathStr = '.'.join(fullPathList)  # Create a string of the current path

        if not isinstance(dataInstance, dict):
                # If the current data is not a dictionary, return an error
                return None, f"Data error: expected object at '{pathStr}', found {type(dataInstance).__name__}."
        if currentKey not in dataInstance:
                # If the key is not found, return an error
                return None, f"Data error: key '{currentKey}' not found under '{pathStr}'."

        # Recursively call extractValue for the next key in the path
        return extractValue(
                dataInstance[currentKey],
                keyPathList[1:],
                newFullPath
        )


def read(queryString, jsonSchema, jsonFilePath):
        """
        Parse "show KEY1.KEY2..." or "show *", load JSON, validate schema once,
        and extract nested values across all instances.
        Prints a user-friendly error or returns the result dictionary.
        """
        queryParts = queryString.strip().split()  # Split the query into parts
        if len(queryParts) != 2:
                # If the query does not have exactly two parts, print usage info
                print("Usage: show KEY1.KEY2... or show *")
                return None

        commandWord, pathExpression = queryParts  # Unpack the command and path
        if commandWord.lower() != 'show':
                # Only the 'show' command is supported
                print("Only 'show' command is supported.")
                return None

        # Load all data instances from the JSON file
        allDataDict, loadError = loadJson(jsonFilePath)
        if loadError:
                # If there was an error loading the file, print it
                print(f"Error: {loadError}")
                return None

        # Wildcard: if the path is '*', return the entire dictionary
        if pathExpression == '*':
                return allDataDict

        # Split the path into keys and validate the schema once
        keyPathList = pathExpression.split('.')
        schemaError = validateSchemaPath(jsonSchema, keyPathList)
        if schemaError:
                # If the schema is invalid, print the error
                print(f"{schemaError}")
                return None

        # Extract data for each instance in the loaded data
        outputDict = {}  # This will store the results for each instance
        for instanceId, instanceData in allDataDict.items():
                # For each instance, try to extract the value at the given path
                value, dataError = extractValue(instanceData, keyPathList)
                if dataError:
                        # If there was an error, store the error message
                        outputDict[instanceId] = {"error": dataError}
                else:
                        # Build a nested dictionary to represent the path and value
                        nestedResult = {}
                        currentLevel = nestedResult
                        for keyPart in keyPathList[:-1]:
                                currentLevel[keyPart] = {}
                                currentLevel = currentLevel[keyPart]
                        currentLevel[keyPathList[-1]] = value
                        outputDict[instanceId] = nestedResult

        # Return the dictionary containing results for all instances
        return outputDict
