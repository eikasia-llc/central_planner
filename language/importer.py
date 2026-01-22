import sys
import os
import subprocess
import shutil

# Try importing optional libraries
try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

def convert_docx_to_md(file_path):
    """
    Converts DOCX to Markdown. 
    1. Tries python-docx for structure preservation.
    2. Fallback to MacOS textutil if available (converts to text/html then we clean up).
    """
    if HAS_DOCX:
        doc = docx.Document(file_path)
        md_lines = []
        for para in doc.paragraphs:
            style = para.style.name
            text = para.text.strip()
            if not text:
                continue
                
            if 'Heading 1' in style:
                md_lines.append(f"# {text}")
            elif 'Heading 2' in style:
                md_lines.append(f"## {text}")
            elif 'Heading 3' in style:
                md_lines.append(f"### {text}")
            else:
                md_lines.append(text)
            
            md_lines.append("") # space after paragraphs
            
        return "\n".join(md_lines)
        
    # MacOS Fallback: textutil
    if sys.platform == 'darwin' and shutil.which('textutil'):
        print(f"python-docx not found. Using MacOS textutil for {file_path}. Structure might be lost.")
        try:
            cmd = ['textutil', '-convert', 'txt', '-stdout', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Add a root header since textutil flattens it
            filename = os.path.basename(file_path)
            return f"# Imported {filename}\n\n" + result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error using textutil: {e}")
            return None

    print("Error: Library 'python-docx' not installed and 'textutil' unavailable.")
    print("Install it via: pip install python-docx")
    return None

def convert_pdf_to_md(file_path):
    """
    Converts PDF to Markdown (Text Extraction).
    """
    if HAS_PYPDF:
        try:
            reader = pypdf.PdfReader(file_path)
            text = []
            filename = os.path.basename(file_path)
            text.append(f"# Imported {filename}")
            
            for page in reader.pages:
                text.append(page.extract_text())
                
            return "\n\n".join(text)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None
            
    # Fallback? Maybe `pdftotext` CLI
    if shutil.which('pdftotext'):
         print(f"pypdf not found. Using pdftotext CLI for {file_path}.")
         try:
            cmd = ['pdftotext', '-layout', file_path, '-']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            filename = os.path.basename(file_path)
            return f"# Imported {filename}\n\n" + result.stdout
         except subprocess.CalledProcessError as e:
             print(f"Error using pdftotext: {e}")
             return None

    print("Error: Library 'pypdf' not installed and 'pdftotext' unavailable.")
    print("Install it via: pip install pypdf")
    return None

def import_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    md_content = None
    if ext == '.docx':
        md_content = convert_docx_to_md(file_path)
    elif ext == '.doc':
        # textutil handles .doc too
        if sys.platform == 'darwin' and shutil.which('textutil'):
             try:
                cmd = ['textutil', '-convert', 'txt', '-stdout', file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                filename = os.path.basename(file_path)
                md_content = f"# Imported {filename}\n\n" + result.stdout
             except Exception as e:
                 print(f"Error converting .doc: {e}")
        else:
            print("Cannot convert .doc files without MacOS textutil or external tools.")
    elif ext == '.pdf':
        md_content = convert_pdf_to_md(file_path)
    else:
        print(f"Unsupported format: {ext}")
        return

    if md_content:
        # Save as .md
        new_path = os.path.splitext(file_path)[0] + ".md"
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Converted to {new_path}")
        
        # Run migration to add metadata
        # We need to import migrate entry point
        # Assuming migrate.py is in the same folder
        import migrate
        print("Running migration on new file...")
        migrate.migrate_file(new_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python importer.py <files>")
        sys.exit(1)
        
    for f in sys.argv[1:]:
        import_file(f)
