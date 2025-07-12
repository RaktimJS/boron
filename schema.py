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
