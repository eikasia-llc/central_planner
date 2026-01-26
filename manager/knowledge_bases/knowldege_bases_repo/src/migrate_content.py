import os
import shutil
from pathlib import Path
import json

# Setup paths
repo_root = Path("../../../").resolve() # central_planner root
kb_repo = Path("..").resolve() # knowldege_bases_repo root
content_dir = kb_repo / "content"

# Ensure content dirs exist
categories = {
    "agents": content_dir / "agents",
    "plans": content_dir / "plans",
    "guidelines": content_dir / "guidelines",
    "root": content_dir / "root",
    "logs": content_dir / "logs",
    "misc": content_dir / "misc"
}

for p in categories.values():
    p.mkdir(parents=True, exist_ok=True)

# Define mapping rules (glob -> category)
# Order matters!
rules = [
    ("**/AGENTS.md", "guidelines"),
    ("**/MD_CONVENTIONS.md", "guidelines"),
    ("**/README.md", "root"),
    
    # Specific Agents
    ("**/MANAGER_AGENT.md", "agents"),
    ("**/CLEANER_AGENT.md", "agents"),
    ("AI_AGENTS/**/*.md", "agents"),
    
    # Plans
    ("**/MASTER_PLAN.md", "plans"),
    ("**/subplans/*.md", "plans"),
    ("language/example/*.md", "plans"),
    
    # Logs
    ("**/*LOG*.md", "logs"),
    ("**/MEETING_NOTES.md", "logs"),
    
    # Catch-all
    ("**/*.md", "misc")
]

# Track processed files to avoid duplicates (if multiple globs match)
processed = set()
registry_updates = {}

def get_category(file_path):
    # Try to match rules
    rel_path = file_path.relative_to(repo_root)
    
    for pattern, cat in rules:
        if file_path.match(pattern):
             return cat
    return categories["misc"]

print(f"Scanning {repo_root}...")

for root, dirs, files in os.walk(repo_root):
    # Skip the destination repo itself to avoid infinite loop
    if "knowldege_bases_repo" in root:
        continue
    
    for file in files:
        if not file.endswith(".md"):
            continue
            
        src_path = Path(root) / file
        
        # Skip hidden files/dirs
        if any(p.startswith(".") for p in src_path.parts):
            continue
            
        if src_path in processed:
            continue
            
        category_dir = get_category(src_path)
        
        # Determine dest path
        dest_path = category_dir / file
        
        # Handle duplicate filenames by prepending parent folder name
        if dest_path.exists():
            parent_name = src_path.parent.name
            dest_path = category_dir / f"{parent_name}_{file}"
            
        processed.add(src_path)
        
        # Copy
        shutil.copy2(src_path, dest_path)
        print(f"Copied {file} -> {dest_path.relative_to(kb_repo)}")
        
        # Record for registry
        # We need to scan dependencies again later, but for now we register the existence
        rel_dest = str(dest_path.relative_to(kb_repo))
        registry_updates[rel_dest] = {
            "path": rel_dest,
            "original_path": str(src_path.relative_to(repo_root)),
            "dependencies": {} # Placeholder, will need scanning
        }

# Update Registry
reg_file = kb_repo / "dependency_registry.json"
if reg_file.exists():
    with open(reg_file, 'r') as f:
        data = json.load(f)
else:
    data = {"files": {}}

# Merge
if "files" not in data:
    data["files"] = {}
    
data["files"].update(registry_updates)

with open(reg_file, 'w') as f:
    json.dump(data, f, indent=2)

print("Migration complete. Run 'dependency_manager.py scan' next to fix dependencies.")
