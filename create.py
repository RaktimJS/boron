"""
This module contains function for inserting new instances of data in the
JSON file. 
"""


import copy




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
indent = 8


def create(schema: dict):
        """
        'create' function is for creating new instances of data. This is a recursive function
        which recurses when the value of any key of the schema, that is a dictionary, is a
        dictionary.

        Proper indentation system has been implemented while countering nested dictionary for
        a better UI and UX.

        'stringType' function has been used for very sensitive case conversions.
        """

        instance = copy.deepcopy(schema)
        global indent

        for key in schema:
                arg = f'{" " * indent}{key}: '   # Variable for variable indentation spaces for nested value taking

                if type(schema[key]) == dict:
                        indent += 4
                        print(arg)
                        instance[key] = create(schema[key])       # Recurse if the value of the key is a dictionary
                        indent -= 4
                elif type(schema[key]) == list:
                        itemList = []

                        while True:     # Looped input taking if the value of the key is list type
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

                                        itemList.append(item)
                                else:
                                        break

                        instance[key] = itemList
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

                        instance[key] = item

        return instance
