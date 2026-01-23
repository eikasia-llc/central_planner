import re
import sys
import os
import json
import argparse
# Add current directory to sys.path to ensure we can import cli_utils if running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import cli_utils
from cli_utils import add_standard_arguments, validate_and_get_pairs

class Node:
    def __init__(self, level, title, metadata=None, content=""):
        self.level = level
        self.title = title
        self.metadata = metadata if metadata else {}
        self.content = content
        self.children = []

    def to_dict(self):
        return {
            "level": self.level,
            "title": self.title,
            "metadata": self.metadata,
            "content": self.content,
            "children": [child.to_dict() for child in self.children]
        }

    def to_markdown(self):
        md_lines = []
        if self.level > 0:
            md_lines.append(f"{'#' * self.level} {self.title}")
            for key, value in self.metadata.items():
                if isinstance(value, list):
                    val_str = f"[{', '.join(str(v) for v in value)}]"
                    md_lines.append(f"- {key}: {val_str}")
                else:
                    md_lines.append(f"- {key}: {value}")
            if self.metadata:
                md_lines.append("") # Empty line after metadata
        
        if self.content:
            md_lines.append(self.content)
            # Ensure proper spacing if content doesn't end with newlines
            if not self.content.endswith('\n'):
                md_lines.append("")
        elif self.level > 0:
             # If no content but valid node, ensure at least one newline separator for clarity
             md_lines.append("")

        for child in self.children:
            md_lines.append(child.to_markdown())
            
        return "\n".join(md_lines)

class MarkdownParser:
    def __init__(self):
        # Regex for headers: # Title
        self.header_pattern = re.compile(r'^(#+)\s+(.*)')
        # Regex for metadata lines: - key: value
        self.metadata_pattern = re.compile(r'^\s*-\s*([a-zA-Z0-9_]+):\s*(.*)')

    def parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        return self.parse_lines(lines)

    def parse_lines(self, lines):
        root = Node(0, "Root")
        node_stack = [root] # Stack to track hierarchy

        i = 0
        while i < len(lines):
            line = lines[i]
            header_match = self.header_pattern.match(line)

            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                new_node = Node(level, title)

                # Look ahead for metadata (immediately following header)
                i += 1
                while i < len(lines):
                    meta_line = lines[i]
                    # Check for metadata line
                    meta_match = self.metadata_pattern.match(meta_line)
                    # Also check if it's just a blank line, we might allow blank lines before metadata? 
                    # Spec says "immediately following", so let's be strict but allow skipping ONE blank line if we want.
                    # Actually spec says "Metadata MUST be placed immediately after the header".
                    # But usually there is a newline after header.
                    
                    if meta_match:
                        key = meta_match.group(1).strip()
                        value_str = meta_match.group(2).strip()
                        
                        # Basic list parsing: [a, b, c]
                        if value_str.startswith('[') and value_str.endswith(']'):
                            inner = value_str[1:-1]
                            if inner.strip():
                                value = [x.strip() for x in inner.split(',')]
                            else:
                                value = []
                        else:
                            value = value_str
                            
                        new_node.metadata[key] = value
                        i += 1
                    elif meta_line.strip() == "":
                        # If we haven't found any metadata yet, a blank line is okay? 
                        # Or if we are inside metadata block, a blank line ends it?
                        # Let's assume blank line ends metadata block or starts content.
                        # If we have finding metadata, blank line ends it.
                        # If we are strictly looking for metadata immediately, blank line might be allowed between header and list?
                        # Let's assume standard markdown: Header\n\n- key: val
                        i += 1
                        continue 
                    else:
                        # Non-metadata line, stop looking for metadata
                        break
                
                # Capture content until next header
                content_lines = []
                while i < len(lines):
                    if self.header_pattern.match(lines[i]):
                        break # Next header found
                    content_lines.append(lines[i])
                    i += 1
                
                new_node.content = "".join(content_lines).strip()

                # Place node in hierarchy
                # Pop until we find a parent with level < new_node.level
                while node_stack[-1].level >= level:
                    node_stack.pop()
                
                node_stack[-1].children.append(new_node)
                node_stack.append(new_node)
            else:
                # Content before first header?
                # For now just ignore or append to root content if needed
                i += 1
        
        return root

    def validate(self, node):
        errors = []
        # Example validation: check if status is valid enum if present
        if 'status' in node.metadata:
            valid_statuses = ['todo', 'in-progress', 'done', 'blocked', 'proposed', 'active', 'draft', 'pending'] # Expanded list based on usage
            if node.metadata['status'] not in valid_statuses:
                errors.append(f"Invalid status '{node.metadata['status']}' in node '{node.title}' (Allowed: {valid_statuses})")
        
        if 'type' in node.metadata:
            valid_types = ['recurring', 'episodic', 'binary']
            if node.metadata['type'] not in valid_types:
                errors.append(f"Invalid type '{node.metadata['type']}' in node '{node.title}' (Allowed: {valid_types})")

        for child in node.children:
            errors.extend(self.validate(child))
        return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and validate Markdown files with Metadata.")
    add_standard_arguments(parser, multi_file=False)
    # Also add positional args which are handled by validat_and_get_pairs
    parser.add_argument('args', nargs='*', help='Input file (and optional output file)')

    args = parser.parse_args()
    
    try:
        # allow_single_file_stdio=True because md_parser can print to stdout
        pairs = validate_and_get_pairs(args, args.args, tool_name="md_parser.py", allow_single_file_stdio=True)
        
        parser_obj = MarkdownParser()
        
        for input_path, output_path in pairs:
            root_node = parser_obj.parse_file(input_path)
            errors = parser_obj.validate(root_node)
            
            if errors:
                print(f"Validation Errors in {input_path}:", file=sys.stderr)
                for err in errors:
                    print(f"- {err}", file=sys.stderr)
                sys.exit(1)
            else:
                result = json.dumps(root_node.to_dict(), indent=2)
                if output_path:
                    with open(output_path, 'w') as f:
                        f.write(result)
                else:
                    print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
