# **Boron v1.1 → How to use?**

## Installation

#### **NOTE:** *Python 3.x* must be installed in the local machine

**Step 1**: Clone or download this repository
```bash
git clone https://github.com/raktimjs/boron
cd <repository-directory>
```

**Step 2**: Run `commandLine.py`
```shell
python commandLine.py
```

### **NOTE:** `commandLine.py` serves as the entry point to the program

## Important Notes

### File Handling
- When you first run Boron, you'll be prompted for a JSON file path
- If this is a new file or not previously cached:
  - You'll need to define the schema structure
  - This schema will be used for all future data entries
- If the file exists in cache:
  - The saved schema will be loaded automatically

### Data Types
- Fields are flexible and accept multiple data types:
  - Numbers (integers and floats)
  - Strings (text)
  - Null values (empty entries)
- Type conversion happens automatically
- No strict validation is enforced

---

## Commands and queries

### 1. **Schema definition:**

```python
File path: C:\path\to\your\json_file.json        # New file, not in cache
# Schema structure definition starts, if the file is not cached

Please define the schema:
    Name                          # Single value field (no suffix required)
    Class
    Subjects{}                    # Object field - use "{}" suffix
        Math{}                    # Nested object - indented by 4 spaces automatically
            FA1                   # Fields inside Math object
            FA2
            SA1
            FA3
            FA4
            SA2
            __end__               # End of object definition using "__end__" clause
        Science{}                 # Another subject object
            FA1
            FA2
            # More fields...
            __end__
        Computer Science{}        # Third subject object
            # Fields here...
            __end__
        __end__                   # End of Subjects object
    Extracurriculars[]            # Array field - use "[]" suffix
    __end__                       # End of root schema
>>> 
```

#### Key Points:
- No suffix: Single value field (scalar)
- `{}` suffix: Object/dictionary field
- `[]` suffix: Array/list field  
- Use `__end__` to close each object definition
- Automatic indentation of nested objects by 4 spaces
- Enter the same field name again under the same hierarchy to remove it

---

### 2. **Data creation:**

Once the schema is defined or a cached file is loaded, type `create` to create a new instance of data:

```python
>>> create

    ID: 1                            # Enter unique ID for the record
    Name: Hrithik Roshan             # Enter scalar values directly
    Class: 10
    Subjects:                        # Object fields show a new line
        Math:                        # Nested objects are indented
            FA1: 85
            FA2: 92
            SA1: 88
            FA3: 90
            FA4: 87
            SA2: 91
        Science:
            FA1: 88
            FA2: 85
            SA1: 90
            FA3: 86
            FA4: 89
            SA2: 92
        Computer Science:
            FA1: 95
            FA2: 88
            SA1: 92
            FA3: 89
            FA4: 91
            SA2: 94
    Extracurriculars: Acting         # For array fields, enter values one per line
    Extracurriculars: Dancing
    Extracurriculars: Gymming
    Extracurriculars: __end__        # Type '__end__' when done with the array. You may enter any number of scalar values in an array
```

### Key Points:
- Each field prompt shows the field name followed by `:`
- For scalar fields: enter the value directly
- For object fields: values are collected for each nested field
- For array fields: 
  - Enter one value per line
  - Type `__end__` to finish the array
  - Nested arrays are not suppported in **v1.1**
- Press Enter without input to set `null` value
- Numbers are automatically converted to proper types
- IDs must be unique for each record

---

### 3. **Data Path Query**

To query data, use the `show` command followed by a path expression:

```python
>>> show Subjects.Math.FA1        # Query specific nested field
1:                                # Results shown by record ID
    Subjects:
        Math:
            FA1: 85
2:
    Subjects:
        Math:
            FA1: 92

>>> show Name                     # Query top-level field
1:
    Name: Hrithik Roshan
2:
    Name: Jane Doe

>>> show *                        # Show all data
1:
    Name: Hrithik Roshan
    Class: 10
    Subjects:
        Math:
            FA1: 85
            FA2: 92
            SA1: 88
            FA3: 90
            FA4: 87
            SA2: 91
        Science:
            FA1: 88
            FA2: 85
            SA1: 90
            FA3: 86
            FA4: 89
            SA2: 92
        Computer Science:
            FA1: 95
            FA2: 88
            SA1: 92
            FA3: 89
            FA4: 91
            SA2: 94
    Extracurriculars: ["Acting", "Dancing", "Gymming", "Singing"]
2:
    # ...data for ID 2
```

#### Key Points:
- Use dot notation to access nested fields: `Field.Nested.Value`
- Query results are grouped by record ID
- Use `show *` to display all data
- Fields must exist in schema
- Results maintain original data structure
- Indentation shows nesting levels

---

### 4. Data Update

Use the `update` command followed by a record ID to modify existing data:

```python
>>> update 1                                                              # Update record ID 1

Name : Hrithik Roshan → Henry Cavill                                      # Format: current_value → new_value
Class : 10 → 11
Subjects:
    Math:
        FA1 : 85 → 88                                                     # Enter new value to update
        FA2 : 92 →                                                        # Press Enter to keep value unchanged
        SA1 : 88 → 90
        FA3 : 90 → 91
        FA4 : 87 → 100
        SA2 : 91 → 95
    Science:
        FA1 : 88 → 90
        FA2 : 85 → 52
        SA1 : 90 → 
        FA3 : 86 → 
        FA4 : 89 → 
        SA2 : 92 → 90
    Computer Science:
        FA1 : 95 → 100
        FA2 : 88 → 98
        SA1 : 92 → 95
        FA3 : 89 → 
        FA4 : 91 → 
        SA2 : 94 → 
Extracurriculars : ["Acting", "Dancing", "Gymming", "Singing"] → Chess    # Update array values
Extracurriculars : ["Acting", "Dancing", "Gymming", "Singing"] → Debate
Extracurriculars : __end__                                                # End array input
```

#### Key Points:
- Command format: `update <ID>`
- Each field shows: `field : <current value> → <new value>`
- Input options:
  - Enter new value to update
  - Press Enter to keep existing value
  - Empty input preserves current value
- Array updates:
  - Enter values one per line
  - Type `__end__` when finished
- Automatic type conversion for numbers
- Changes are saved immediately

---

### 5. Data Delete

Use the `delete` command followed by a record ID to remove data:

```python
>>> delete 1                     # Delete record with ID 1
Record with ID "1" deleted successfully
```

#### Key Points:
- Command format: `delete <ID>`
- Deletion is permanent and cannot be undone
- All data for the specified ID is removed
- The schema remains unchanged
- File is automatically saved after deletion

## Tips:
- Use `show *` to view all records before deletion
- Double-check the ID to avoid deleting wrong records
- No confirmation prompt in v1.1 - be careful!
- Use `cd` to change active file
