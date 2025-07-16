# This script serves as the entry point to the program.




import os, json
import schema, create

os.system('cls' if os.name == "nt" else "clear")


def boot_loader(file_path: str,
                cache_file: str = "cache.json") -> dict | None:
        """
        Load and validate a JSON file and manage schema caching.

        Steps:
        1. Normalize and verify that file_path exists and ends with '.json'.
        2. Load JSON and enforce that the top-level structure is a dict.
        3. Read cache_file (must be a JSON array) to lookup an existing schema.
           - If found: return the cached schema.
           - If not found: repeatedly prompt the user to define and save a new schema
             via schema.schemadef(), then return it once saved.

        Parameters
        ----------
        file_path : str
            Path to the JSON file to load.
        cache_file : str, optional
            Path to the cache JSON file storing schemas (default 'cache.json').

        Returns
        -------
        dict
            The existing or newly defined schema for the file, or None on error.
        """


        file_path = os.path.normpath(file_path)

        if not os.path.isfile(file_path):
                print("Error: File does not exist")
                return None
        if not file_path.lower().endswith(".json"):
                print("Error: File is not a .json")
                return None

        try:
                with open(file_path, "r") as f:
                        data = json.load(f)
        except Exception:
                print("Error: JSON is invalid or not an object")
                return None
        if not isinstance(data, dict):
                print("Error: JSON is invalid or not an object")
                return None

        normalized = file_path
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

        for entry in cache_data:
                if isinstance(entry, dict) and entry.get("path") and entry.get("schema"):
                        if os.path.normpath(entry["path"]) == normalized:
                                return entry["schema"]

        while True:
                print("\nPlease define the schema:")
                new_schema = schema.schemadef()
                save = input("Do you want to save the schema? (Y/n): ").strip().lower()
                if save == "n":
                        print("Schema discarded. Please define again.")
                        continue
                cache_data.append({"path": normalized, "schema": new_schema})
                try:
                        with open(cache_file, "w") as f:
                                json.dump(cache_data, f, indent=4)
                except Exception:
                        print(f"Error: Failed to write to '{cache_file}'")
                        return None
                return new_schema





if __name__ == "__main__":
        while True:
                inp = input(">>> ")

                jsonSchema = boot_loader(inp)
