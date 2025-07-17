"""
This module contains functions for data deletion by id
"""




import json


def delete(filePath: str, id: str):
        with open(filePath, "r") as file:
                data = json.load(file)

        if len(data) == 0:
                print("Empty file. No instances to delete")
                return
        else:
                if id in data:
                        del data[id]
                        print(f"Instance related to ID \"{id}\" deleted successfully")
                else:
                        print(f"No instance is linked to ID \"{id}\". Try again")

        with open(filePath, "w") as file:
                json.dump(data, file, indent=8)

        return
