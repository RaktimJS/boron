# This script serves as the entry point to the program.




import os, json
import schema
import create, read, update, delete


filePath: str = ""




def boot_loader(input_path: str, cache_file: str = "cache.json") -> dict | None:
        """
        Load and validate a JSON file and manage schema caching.
        On success, assigns the file's normalized path to global filePath.
        """
        global filePath

        # Normalize & existence checks
        normalized = os.path.normpath(input_path)
        if not os.path.isfile(normalized):
                print("Error: File does not exist")
                return None
        if not normalized.lower().endswith(".json"):
                print("Error: File is not a .json")
                return None

        # Load JSON
        try:
                with open(normalized, "r") as f:
                        data = json.load(f)
        except Exception:
                print("Error: JSON is invalid or not an object")
                return None
        if not isinstance(data, dict):
                print("Error: JSON is invalid or not an object")
                return None

        # Load cache
        try:
                with open(cache_file, "r") as f:
                        cache_data = json.load(f)
        except FileNotFoundError:
                print(f"Error: '{cache_file}' not found.")
                return None
        except json.JSONDecodeError:
                print(f"Error: '{cache_file}' is corrupted or malformed")
                return None
        if not isinstance(cache_data, list):
                print(f"Error: '{cache_file}' must be a JSON array.")
                return None

        # Lookup existing schema
        for entry in cache_data:
                if (
                        isinstance(entry, dict)
                        and entry.get("path")
                        and entry.get("schema")
                        and os.path.normpath(entry["path"]) == normalized
                ):
                        filePath = normalized
                        return entry["schema"]

        # Define and optionally save new schema
        while True:
                print("\nPlease define the schema:")
                new_schema = schema.schemadef()
                save = input("Do you want to save the schema? (y/n): ").strip().lower()
                if save == "n":
                        print("Schema discarded. Please define again.")
                        continue

                cache_data.append({"path": normalized, "schema": new_schema})
                try:
                        with open(cache_file, "w") as f:
                                json.dump(cache_data, f, indent=8)
                except Exception:
                        print(f"Error: Failed to write to '{cache_file}'")
                        return None

                filePath = normalized
                return new_schema





os.system("cls" if os.name == "nt" else "clear")

while True:
        path = input("File path: ")
        jsonSchema = boot_loader(path)

        if not jsonSchema:
                input("\nPress Enter to continue\n")

        if jsonSchema and filePath:
                while True:
                        inp = input(">>> ")

                        identifier = inp.strip().split()

                        if identifier[0].lower() == "create":
                                print("")
                                create.create(jsonSchema, filePath)
                                print("")
                        elif identifier[0].lower() == "show":
                                print("")
                                read.read(inp, jsonSchema, filePath)
                                print("")
                        elif identifier[0].lower() == "update":
                                print("")
                                update.update(filePath, identifier[1])
                                print("")
                        elif identifier[0].lower() == "delete":
                                print("")
                                delete.delete(filePath, identifier[1])
                                print("")
                        elif identifier[0].lower() == "cd":
                                break
                        elif identifier[0] == "cls":
                                os.system("cls" if os.name == "nt" else "clear")
                        else:
                                print("Invalid command\n")
