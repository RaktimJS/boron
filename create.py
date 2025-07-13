"""
This module contains function for inserting new instances of data in the
JSON file. 
"""



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

indent = 0

def create(schema: dict) -> list:
        global indent
        shape = []

        for key in schema:
                arg = f'{" " * indent}{key}: '

                if type(schema[key]) == dict:
                        indent += 4
                        print(arg)
                        shape.append(create(schema[key]))
                        indent -= 4
                elif type(schema[key]) == list:
                        itemList = []

                        while True:
                                item = input(arg)

                                if item.lower() != "end":
                                        if stringType(item) == int:
                                                item = int(item)
                                        elif stringType(item) == float:
                                                item = float(item)
                                        else:
                                                pass

                                        itemList.append(item)
                                else:
                                        break
                        
                        shape.append(itemList)
                else:
                        item = input(arg)

                        if item.lower() != "end":
                                if stringType(item) == int:
                                        item = int(item)
                                elif stringType(item) == float:
                                        item = float(item)
                                else:
                                        pass

                        shape.append(item)

        return shape




__import__('os').system('cls')

Dict = {
        "Name": None,
        "Class": None,
        "Subjects": {
                "Math": {
                        "FA 1": None,
                        "FA 2": None,
                        "SA 1": None,
                        "FA 3": None,
                        "FA 4": None,
                        "SA 2": None
                },
                "Science": {
                        "FA 1": None,
                        "FA 2": None,
                        "SA 1": None,
                        "FA 3": None,
                        "FA 4": None,
                        "SA 2": None
                },
                "Computer Science": {
                        "FA 1": None,
                        "FA 2": None,
                        "SA 1": None,
                        "FA 3": None,
                        "FA 4": None,
                        "SA 2": None
                },
                "Music": {
                        "FA 1": None,
                        "FA 2": None,
                        "SA 1": None,
                        "FA 3": None,
                        "FA 4": None,
                        "SA 2": None
                }
        }
}

print(create(Dict))
