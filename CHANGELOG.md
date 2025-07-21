# 1.1.0 (July 21, 2025)

### Additions:
- Automatic removal of duplicate scalar or array fields within the same hierarchy
- Interactive confirmation prompt for duplicate object fields to prevent accidental deletion of nested objects
  - Requires "y" (YES) confirmation to remove the entire nested object

Previously, users had to rewrite the entire schema from scratch when making typos, which significantly impacted the user experience. This limitation has now been addressed.

### Removals:
- Replaced redundant duplicate field messages with more intuitive handling systems

# 1.0.1 (July 21, 2025)

### Fixes:
- Restricted entry of two or more fields with the same name in a schema object. A message is prompted saying that the entered field already exists if a field wit the same name already exists

- Fetches the absolute path if a relative path is entered

# 1.0.0 (July 19, 2025)

Version 1.0.0 out as open source
