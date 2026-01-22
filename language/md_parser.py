import re
import sys
import json

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
                        value = meta_match.group(2).strip()
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
    if len(sys.argv) < 2:
        print("Usage: python md_parser.py <file.md>")
        sys.exit(1)

    parser = MarkdownParser()
    file_path = sys.argv[1]
    
    try:
        root_node = parser.parse_file(file_path)
        errors = parser.validate(root_node)
        
        if errors:
            print("Validation Errors:")
            for err in errors:
                print(f"- {err}")
            sys.exit(1)
        else:
            # Print JSON representation to stdout
            print(json.dumps(root_node.to_dict(), indent=2))
            # print("\nValidation Successful.", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
