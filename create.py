"""
This module contains function for inserting new instances of data in the
JSON file. 
"""


import copy, json




# Function for sensible type conversion
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


# Variable to indenting nesting
indent = 4


def populator(schema: dict, filePath: str):
        """
        'create' function is for creating new instances of data. This is a recursive function
        which recurses when the value of any key of the schema, that is a dictionary, is a
        dictionary.

        Proper indentation system has been implemented while countering nested dictionary for
        a better UI and UX.

        'stringType' function has been used for very sensitive case conversions.
        """

        value = copy.deepcopy(schema)
        global indent
        arg = f'{" " * indent}'


        for key in schema:
                arg = f'{" " * indent}{key}: '   # Variable for variable indentation spaces for nested value taking

                if type(schema[key]) == dict:
                        indent += 4
                        print(arg)
                        value[key] = populator(schema[key], filePath)       # Recurse if the value of the key is a dictionary
                        indent -= 4
                elif type(schema[key]) == list:
                        itemList = []

                        while True:     # Looped input taking if the value of the key is list type
                                item = input(arg)

                                if item.lower() != "__end__":
                                        if stringType(item.strip()) == int:
                                                item = int(item)
                                        elif stringType(item.strip()) == float:
                                                item = float(item)
                                        elif item.strip() == "":
                                                item = None
                                        else:
                                                pass

                                        itemList.append(item)
                                else:
                                        break

                        value[key] = itemList
                else:   # Input taking for scalar value
                        item = input(arg)

                        if item.lower() != "end":
                                if stringType(item.strip()) == int:
                                        item = int(item)
                                elif stringType(item.strip()) == float:
                                        item = float(item)
                                elif item.strip() == "":
                                        item = None
                                else:
                                        pass

                        value[key] = item
        return value



def create(schema: dict, filePath:str):
        global indent
        arg = f'{" " * indent}'


        try:
                with open(filePath, "r") as f:
                        data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
                data = {}


        while True:
                entry_id = input(f"{arg}ID: ")

                if entry_id in list(data.keys()):
                        print(f"ID {entry_id} already exists")
                if " " in entry_id:
                        print("ID can't have blank space")
                else:
                        break

        new_record = populator(schema, filePath)
        data[entry_id] = new_record

        with open(filePath, "w") as f:
                json.dump(data, f, indent=8)
