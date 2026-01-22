import sys
import os
import re
import argparse

# Simple migration script
# Logic:
# 1. Read file
# 2. Identify headers
# 3. Check if header has METADATA block immediately after
# 4. If not, insert default METADATA block
# 5. Write back

def has_meta_block(lines, header_index):
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
            if not has_meta_block(lines, i):
                # Insert default METADATA
                # Infer status if possible, otherwise default to "active" or "documented"
                # For AGENTS files, "active" seems appropriate.
                default_meta = "- status: active\n"
                
                # If there's a newline after header, we can insert before it or after it?
                # Usually we want Header\nMETADATA.
                # If the line ends with \n, we just append to new_lines.
                
                # But wait, we just appended 'line' (the header) to new_lines.
                # Now we append the METADATA.
                new_lines.append(default_meta)
                
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

import cli_utils
from cli_utils import add_standard_arguments, validate_and_get_pairs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate markdown files to Protocol format.")
    add_standard_arguments(parser, multi_file=True)
    parser.add_argument('args', nargs='*', help='Input file(s)')
    
    args = parser.parse_args()
    
    try:
        # migrate.py updates files. 
        # allow_single_file_stdio=False because it does not support stdout mode easily (it modifies in place).
        pairs = validate_and_get_pairs(args, args.args, tool_name="migrate.py", allow_single_file_stdio=False)
        
        for input_path, output_path in pairs:
            # If output_path != input_path, we should copy first then migrate? 
            # OR read input, migrate in memory, write to output.
            # migrate_file function currently does read -> check -> write. 
            # It takes file_path. It reads from file_path and writes to file_path.
            # We need to adapt it or copy the file first.
            
            if input_path != output_path:
                import shutil
                shutil.copy2(input_path, output_path)
                target = output_path
            else:
                target = input_path
                
            migrate_file(target)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
