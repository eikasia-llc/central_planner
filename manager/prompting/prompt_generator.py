#!/usr/bin/env python3
"""
Prompt Generator for AI Assistants

This script generates prompt injection text that forces AI coding assistants
to read all dependencies of a markdown file before reading the target file.

Usage:
    python prompt_generator.py CLEANER_AGENT.md
    python prompt_generator.py manager/cleaner/CLEANER_AGENT.md --verbose
    python prompt_generator.py MANAGER_AGENT.md --copy

The output can be directly pasted into an AI assistant conversation.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

# Import the dependency manager
from dependency_manager import DependencyManager, PROJECT_ROOT


class PromptGenerator:
    """Generate AI-friendly prompts with dependency resolution."""

    def __init__(self):
        self.manager = DependencyManager()

    def find_file(self, query: str) -> Optional[str]:
        """
        Find a file in the registry by partial name match.

        Args:
            query: Full or partial file name (e.g., 'CLEANER_AGENT.md' or 'CLEANER_AGENT')

        Returns:
            Full path if found, None otherwise
        """
        # Normalize query
        query = query.strip()
        if not query.endswith('.md'):
            query += '.md'

        # Direct match
        if query in self.manager.registry["files"]:
            return query

        # Search by filename
        query_lower = query.lower()
        matches = []

        for path in self.manager.registry["files"].keys():
            filename = Path(path).name.lower()
            if filename == query_lower:
                matches.append(path)
            elif query_lower in path.lower():
                matches.append(path)

        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print(f"Multiple matches found for '{query}':", file=sys.stderr)
            for m in matches:
                print(f"  - {m}", file=sys.stderr)
            print("Please specify the full path.", file=sys.stderr)
            return None

        # Not in registry - try to find the file on disk
        for md_file in PROJECT_ROOT.glob(f"**/{query}"):
            if any(part.startswith('.') for part in md_file.parts):
                continue
            rel_path = str(md_file.relative_to(PROJECT_ROOT))
            return rel_path

        return None

    def generate(
        self,
        file_query: str,
        style: str = "imperative",
        include_rationale: bool = False,
        verbose: bool = False
    ) -> str:
        """
        Generate a prompt for reading a file with its dependencies.

        Args:
            file_query: File name or path to generate prompt for
            style: Prompt style - 'imperative', 'polite', or 'structured'
            include_rationale: Whether to include explanation of why deps are needed
            verbose: Print additional information

        Returns:
            Generated prompt text
        """
        # Find the file
        file_path = self.find_file(file_query)

        if not file_path:
            return f"Error: Could not find file matching '{file_query}'"

        if verbose:
            print(f"Resolved file: {file_path}", file=sys.stderr)

        # Resolve dependencies
        resolved = self.manager.resolve_dependencies(file_path)

        if verbose:
            print(f"Dependencies: {resolved[:-1]}", file=sys.stderr)
            print("", file=sys.stderr)

        # Generate prompt based on style
        if len(resolved) == 1:
            return self._single_file_prompt(resolved[0], style)

        return self._multi_file_prompt(resolved, style, include_rationale)

    def _single_file_prompt(self, file_path: str, style: str) -> str:
        """Generate prompt for a file with no dependencies."""
        if style == "polite":
            return f"Please read {file_path}"
        elif style == "structured":
            return f"<read_file>{file_path}</read_file>"
        else:  # imperative
            return f"Read {file_path}"

    def _multi_file_prompt(
        self,
        resolved: List[str],
        style: str,
        include_rationale: bool
    ) -> str:
        """Generate prompt for a file with dependencies."""
        deps = resolved[:-1]
        target = resolved[-1]

        if style == "structured":
            lines = [
                "<!-- DEPENDENCY INJECTION: Read these files in order -->",
                "<dependency_chain>"
            ]
            for i, f in enumerate(resolved, 1):
                role = "target" if f == target else "dependency"
                lines.append(f'  <file order="{i}" role="{role}">{f}</file>')
            lines.append("</dependency_chain>")
            if include_rationale:
                lines.append("")
                lines.append("<!-- Rationale: Depth-first resolution ensures context is loaded before the target -->")
            return "\n".join(lines)

        elif style == "polite":
            lines = [f"Please read the following files in order to understand {Path(target).name}:"]
            lines.append("")
            for i, f in enumerate(resolved, 1):
                lines.append(f"{i}. {f}")
            if include_rationale:
                lines.append("")
                lines.append(f"(Dependencies are listed first to provide necessary context for {Path(target).name})")
            return "\n".join(lines)

        else:  # imperative (default)
            lines = [f"Read these files in this exact order:"]
            lines.append("")
            for i, f in enumerate(resolved, 1):
                marker = " (target)" if f == target else ""
                lines.append(f"{i}. {f}{marker}")

            if include_rationale:
                lines.append("")
                lines.append("This order ensures you have all required context before reading the main file.")

            return "\n".join(lines)

    def generate_clipboard_text(self, file_query: str) -> str:
        """Generate clean text suitable for clipboard/pasting."""
        file_path = self.find_file(file_query)

        if not file_path:
            return f"Read {file_query}"

        resolved = self.manager.resolve_dependencies(file_path)

        if len(resolved) == 1:
            return f"Read {resolved[0]}"

        # Simple numbered list - easiest to paste and understand
        lines = ["Read these files in order:"]
        for i, f in enumerate(resolved, 1):
            lines.append(f"{i}. {f}")
        return "\n".join(lines)


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard (macOS/Linux/Windows)."""
    import subprocess
    import platform

    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif system == "Linux":
            subprocess.run(["xclip", "-selection", "clipboard"],
                          input=text.encode(), check=True)
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode(), check=True)
        else:
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate AI assistant prompts with dependency resolution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate prompt for CLEANER_AGENT
  python prompt_generator.py CLEANER_AGENT.md

  # Use polite style with rationale
  python prompt_generator.py MANAGER_AGENT.md --style polite --rationale

  # Copy to clipboard (macOS)
  python prompt_generator.py CLEANER_AGENT --copy

  # Verbose output showing resolution
  python prompt_generator.py CLEANER_AGENT.md --verbose

Styles:
  imperative  - Direct commands: "Read X" (default)
  polite      - Request format: "Please read X"
  structured  - XML-tagged format for parsing
        """
    )

    parser.add_argument("file", help="File name or path (e.g., CLEANER_AGENT.md)")
    parser.add_argument("--style", "-s", choices=["imperative", "polite", "structured"],
                       default="imperative", help="Prompt style (default: imperative)")
    parser.add_argument("--rationale", "-r", action="store_true",
                       help="Include explanation of why dependencies are needed")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Print debug information")
    parser.add_argument("--copy", "-c", action="store_true",
                       help="Copy result to clipboard")

    args = parser.parse_args()

    generator = PromptGenerator()
    prompt = generator.generate(
        args.file,
        style=args.style,
        include_rationale=args.rationale,
        verbose=args.verbose
    )

    print(prompt)

    if args.copy:
        clipboard_text = generator.generate_clipboard_text(args.file)
        if copy_to_clipboard(clipboard_text):
            print("\n[Copied to clipboard]", file=sys.stderr)
        else:
            print("\n[Could not copy to clipboard]", file=sys.stderr)


if __name__ == "__main__":
    main()
