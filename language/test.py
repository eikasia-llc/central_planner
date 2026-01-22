import unittest
import os
import sys
import tempfile
import shutil

# Ensure we can import modules from the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from md_parser import MarkdownParser
from operations import merge_trees, extend_tree
# visualization is hard to test programmatically for output, but we can try running it

class TestLanguageTools(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a valid source file
        self.valid_file = os.path.join(self.test_dir, "valid.md")
        with open(self.valid_file, "w") as f:
            f.write("# Root\n- status: active\n- type: recurring\n\n## Child\n- status: todo\n- type: binary\n")

        # Create an invalid file
        self.invalid_file = os.path.join(self.test_dir, "invalid.md")
        with open(self.invalid_file, "w") as f:
            f.write("# Root\n(no status)\n\n## Child\n- status: todo\n- type: invalid_type\n")

        # Create files for operations
        self.target_file = os.path.join(self.test_dir, "target.md")
        with open(self.target_file, "w") as f:
            f.write("# Target Root\n- status: active\n\n## Feature A\n- status: todo\n")
            
        self.source_file = os.path.join(self.test_dir, "source.md")
        with open(self.source_file, "w") as f:
            f.write("# Source Root\n- status: draft\n\n## SubTask\n- status: proposed\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parser_valid(self):
        parser = MarkdownParser()
        root = parser.parse_file(self.valid_file)
        self.assertEqual(root.title, "Root")
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].title, "Child")
        self.assertEqual(root.children[0].metadata['status'], 'todo')
        self.assertEqual(root.children[0].metadata['type'], 'binary')
        
    def test_parser_validation(self):
        parser = MarkdownParser()
        root = parser.parse_file(self.valid_file)
        errors = parser.validate(root)
        self.assertEqual(len(errors), 0)
        
        # Check invalid file
        root_invalid = parser.parse_file(self.invalid_file)
        errors_invalid = parser.validate(root_invalid)
        # Should have error for invalid type
        self.assertTrue(any("Invalid type" in e for e in errors_invalid))

    def test_operations_extend(self):
        output_file = os.path.join(self.test_dir, "extended.md")
        extend_tree(self.target_file, self.source_file, output_file)
        
        parser = MarkdownParser()
        root = parser.parse_file(output_file)
        
        # Target Root should now have Feature A AND SubTask (appended from source)
        # Note: extend_tree appends source's CHILDREN to target's children
        child_titles = [c.title for c in root.children]
        self.assertIn("Feature A", child_titles)
        self.assertIn("SubTask", child_titles)

    def test_operations_merge(self):
        output_file = os.path.join(self.test_dir, "merged.md")
        # Merge source (SubTask) into "Feature A" of target
        merge_trees(self.target_file, self.source_file, "Feature A", output_file)
        
        parser = MarkdownParser()
        root = parser.parse_file(output_file)
        
        # Find feature A
        feature_a = next(c for c in root.children if c.title == "Feature A")
        # It should have SubTask as child
        self.assertEqual(len(feature_a.children), 1)
        self.assertEqual(feature_a.children[0].title, "SubTask")

if __name__ == "__main__":
    unittest.main()
