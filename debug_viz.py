
import sys
import os

# Mock the path setup like app.py does
current_dir = os.path.abspath(".")
planner_dir = os.path.join(current_dir, "manager/planner")
sys.path.append(planner_dir)

print(f"Planner dir: {planner_dir}")

try:
    import visualize_html
    print("Imported visualize_html successfully")
except ImportError as e:
    print(f"Failed import: {e}")
    sys.exit(1)

target_file = os.path.join(planner_dir, "MASTER_PLAN.md")
print(f"Target file: {target_file}")

try:
    print("Calling generate_html(embed_d3=True)...")
    html = visualize_html.generate_html(target_file, embed_d3=True)
    print(f"Generated HTML successfully. Length: {len(html)}")
    
    # Check if D3 was actually embedded
    if "/* Embedded D3 */" in html:
        print("D3 marker found.")
    else:
        print("D3 marker NOT found.")
        
except Exception as e:
    print(f"Error during generation: {e}")
    import traceback
    traceback.print_exc()
