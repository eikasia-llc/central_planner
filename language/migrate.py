import sys
import os
import re

# Simple migration script
# Logic:
# 1. Read file
# 2. Identify headers
# 3. Check if header has METADATA block immediately after
# 4. If not, insert default METADATA block
# 5. Write back

def has_yaml_block(lines, header_index):
    # check next few lines for METADATA-like content
    if header_index + 1 >= len(lines):
        return False
    
    # Check immediate next line (standard/strict) or allow 1 empty line?
    # Our convention says "immediately following", so let's check index+1
    next_line = lines[header_index + 1].strip()
    
    # If it starts with "- key: value" or just "key: value"
    if re.match(r'^-?\s*\w+:', next_line):
        return True
        
    return False

def migrate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    
    header_pattern = re.compile(r'^(#+)\s+(.*)')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        header_match = header_pattern.match(line)
        
        new_lines.append(line)
        
        if header_match:
            # Check if existing METADATA
            if not has_yaml_block(lines, i):
                # Insert default METADATA
                # Infer status if possible, otherwise default to "active" or "documented"
                # For AGENTS files, "active" seems appropriate.
                default_yaml = "- status: active\n"
                
                # If there's a newline after header, we can insert before it or after it?
                # Usually we want Header\nMETADATA.
                # If the line ends with \n, we just append to new_lines.
                
                # But wait, we just appended 'line' (the header) to new_lines.
                # Now we append the METADATA.
                new_lines.append(default_yaml)
                
                # Also, we might want to add 'owner' or 'updated' if we could guess, but let's keep it simple.
        
        i += 1
    
    # Write back only if changed
    if new_lines != lines:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Migrated {file_path}")
        return True
    else:
        # print(f"No changes needed for {file_path}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate.py <file.md>")
        sys.exit(1)
        
    for f in sys.argv[1:]:
        migrate_file(f)
