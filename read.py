"""
This module contains functions for data query.

NOTE: v1 doesn't support data query
"""




import json

def loadJson(filePath):
        """
        Load a JSON file and return its full dict content.
        Returns (dataDict, None) on success, or (None, errorMessage) on failure.
        """
        try:
                with open(filePath, 'r') as fileHandle:
                        parsedJson = json.load(fileHandle)
        except FileNotFoundError:
                return None, f"File not found: '{filePath}'"
        except json.JSONDecodeError as decodeError:
                return None, f"Invalid JSON: {decodeError.msg} at line {decodeError.lineno}, column {decodeError.colno}"

        if not isinstance(parsedJson, dict):
                return None, "Root JSON must be an object (dictionary of instances)."

        return parsedJson, None

def validateSchemaPath(schemaDefinition, keyPathList):
        """
        Walk the schemaDefinition following keyPathList to ensure every key exists.
        Returns None on success, or errorMessage on failure.
        """
        current = schemaDefinition
        fullPathList = []
        for key in keyPathList:
                fullPathList.append(key)
                pathStr = '.'.join(fullPathList[:-1])
                if not isinstance(current, dict):
                        return f"Schema error: '{pathStr}' should be an object."
                if key not in current:
                        if pathStr.strip() == "":
                                return f"Schema error: key '{key}' not defined under '{pathStr}'."
                        else:
                                return f"Schema error: key '{key}' not defined under root."
                current = current[key]
        return


def extractValue(dataInstance, keyPathList, fullPathList=None):
        """
        Recursively walk down dataInstance following keyPathList.
        Returns (value, None) on success, or (None, errorMessage) on failure.
        """
        if fullPathList is None:
                fullPathList = []

        if not keyPathList:
                return dataInstance, None

        currentKey = keyPathList[0]
        newFullPath = fullPathList + [currentKey]
        pathStr = '.'.join(fullPathList)

        if not isinstance(dataInstance, dict):
                return None, f"Data error: expected object at '{pathStr}', found {type(dataInstance).__name__}."
        if currentKey not in dataInstance:
                return None, f"Data error: key '{currentKey}' not found under '{pathStr}'."

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
        queryParts = queryString.strip().split()
        if len(queryParts) != 2:
                print("Usage: show KEY1.KEY2... or show *")
                return None

        commandWord, pathExpression = queryParts
        if commandWord.lower() != 'show':
                print("Only 'show' command is supported.")
                return None

        # Load all data instances
        allDataDict, loadError = loadJson(jsonFilePath)
        if loadError:
                print(f"Error: {loadError}")
                return None

        # Wildcard: return the entire dictionary of instances
        if pathExpression == '*':
                return allDataDict

        # Split path and validate schema once
        keyPathList = pathExpression.split('.')
        schemaError = validateSchemaPath(jsonSchema, keyPathList)
        if schemaError:
                print(f"{schemaError}")
                return None

        # Extract data for each instance
        outputDict = {}
        for instanceId, instanceData in allDataDict.items():
                value, dataError = extractValue(instanceData, keyPathList)
                if dataError:
                        outputDict[instanceId] = {"error": dataError}
                else:
                        # Build nested dictionary for this instance
                        nestedResult = {}
                        currentLevel = nestedResult
                        for keyPart in keyPathList[:-1]:
                                currentLevel[keyPart] = {}
                                currentLevel = currentLevel[keyPart]
                        currentLevel[keyPathList[-1]] = value
                        outputDict[instanceId] = nestedResult

        return outputDict
