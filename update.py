"""
This module conains function for updating values of an instance
"""

import json, copy




def stringType(string: str):
        try:
                int(string)
                return int
        except ValueError:
                try:
                        float(string)
                        return float
                except ValueError:
                        return str




indent = 4

def inputTaker(Dict: dict):
        global indent

        for i in Dict:
                arg = f'{" " * indent}{i}'

                if type(Dict[i]) == list:
                        newList = []

                        while True:
                                item = input(f"{arg} : {Dict[i]} → ")

                                if item != "__end__":
                                        item = item.strip()
                                        if not item:  # Check for empty input
                                                newList.append(None)
                                        elif stringType(item) == int:
                                                newList.append(int(item))
                                        elif stringType(item) == float:
                                                newList.append(float(item))
                                        else:
                                                newList.append(item)
                                else:
                                        break

                        Dict[i] = newList
                elif type(Dict[i]) == dict:
                        indent += 4
                        print(arg)
                        Dict[i] = inputTaker(Dict[i])
                        indent -= 4
                else:
                        item = input(f"{arg} : {Dict[i]} → ")

                        if item != "__end__":
                                item = item.strip()
                                if not item:  # Check for empty input
                                        item = None
                                elif stringType(item) == int:
                                        item = int(item)
                                elif stringType(item) == float:
                                        item = float(item)
                        
                        Dict[i] = item

        return Dict

def update(filePath: str, id: str):
        with open(filePath, "r") as file:
                data = json.load(file)

        if len(data) == 0:
                print("Empty file. No instances to update")
                return
        else:
                if id in data:
                        instance = copy.deepcopy(data[id])
                        instance = inputTaker(instance)

                        data[id] = instance

                        print(f"Instance related to ID \"{id}\" updated successfully")
                else:
                        print(f"No instance is linked to ID \"{id}\". Try again")

        with open(filePath, "w") as file:
                json.dump(data, file, indent=8)

        return
