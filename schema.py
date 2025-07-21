"""
This module contains all functions for schema handling.
"""

"""
The schema definition for that particular JSON is stored with the JSON file's path
as an object, and the JSON storing the cache is an array-type JSON at the topmost
level. Meaning, cache.json is an array that stores multiple JSON objects, each one
containing 2 attributes, "path" and "schema", where "path" stores the file path of
the JSON and "schema" stores the schema definition of the "JSON".
"""




import json, os



def fetcher(filePath:str):
        """
        This function fetches the schema of the JSON (i.e, filePath) if it has been cached in 'cache.json'.

        NOTE: This function is not a validator or a definer.
        """

        try:
                with open("cache.json", "r") as cache:
                        cacheData = json.load(cache)
        except json.JSONDecodeError:
                print("'cache.json' is corrupted")
                return None
        except Exception as e:
                print("Unexpected error")
                return None


        for i in cacheData:
                if filePath in os.path.normpath(i["path"]):
                        schema = i["schema"]
                        return schema




# Variable for indenting nesting
indent = 4

def schemadef():
        """
        This function lets user define schema for a JSON file that has not been recorded in
        'cache.json'.
        
        When entering the name of a key, the user may end the key name with a pair of curly
        braces ("{}") or square bracket ("[]") to define non scalar data type — dictionary
        and list respectively.

        If the value if a dictionary, the function will recurse. And at the end it returns 
        a variable named "schemaDefinition"
        """

        global indent

        schemaDefinition = {}
        arg = f'{" " * indent}'

        while True:
                key = input(arg)
                key = key.strip()

                if "__end__" not in key:
                        if "__end__" not in key:
                                # Strip any type indicators before checking for duplicates
                                base_key = key.removesuffix("[]").removesuffix("{}")
                                if base_key not in schemaDefinition:
                                        if key.endswith("[]"):          # When the value of a key is a list
                                                schemaDefinition[key[:len(key) - 2]] = []
                                        elif key.endswith("{}"):        # When the value of a key is a dictionary
                                                indent += 4
                                                schemaDefinition[key[:len(key) - 2]] = schemadef()
                                                indent -= 4
                                        else:
                                                schemaDefinition[key] = None
                                else:
                                        print(f"{arg}\033[A\033[KField \"{base_key}\" already exists")
                else:
                        break

        return schemaDefinition
