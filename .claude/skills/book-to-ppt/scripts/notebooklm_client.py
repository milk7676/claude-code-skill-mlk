"""
NotebookLM Client - Generate PPT outlines using real NotebookLM
Integrates with the notebooklm skill
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict

# Path to notebooklm skill
NOTEBOOKLM_SKILL_PATH = Path.home() / ".claude" / "skills" / "notebooklm"


class NotebookLMClient:
    """Client for interacting with NotebookLM"""

    def __init__(self, notebook_url: Optional[str] = None):
        """
        Initialize NotebookLM client

        Args:
            notebook_url: URL of the NotebookLM notebook
        """
        self.notebook_url = notebook_url
        self.skill_path = NOTEBOOKLM_SKILL_PATH

    def ask_notebooklm(self, question: str, notebook_url: Optional[str] = None) -> Optional[str]:
        """
        Ask NotebookLM a question

        Args:
            question: Question to ask
            notebook_url: Optional override notebook URL

        Returns:
            Answer from NotebookLM or None if failed
        """
        url = notebook_url or self.notebook_url

        if not url:
            print("Error: No notebook URL provided")
            return None

        # Build command
        script_path = self.skill_path / "scripts" / "ask_question.py"
        run_wrapper = self.skill_path / "scripts" / "run.py"

        cmd = [
            sys.executable,
            str(run_wrapper),
            "ask_question.py",
            "--question", question,
            "--notebook-url", url
        ]

        # Execute command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=180  # 3 minutes timeout
            )

            if result.returncode == 0:
                # Extract answer from output
                output = result.stdout

                # Remove follow-up reminder if present
                if "EXTREMELY IMPORTANT:" in output:
                    output = output.split("EXTREMELY IMPORTANT:")[0].strip()

                return output
            else:
                print(f"Error running NotebookLM: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("Error: NotebookLM query timed out")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate_outline_prompt(self, chapter_content: str, chapter_title: str = "") -> str:
        """
        Generate prompt for PPT outline creation

        Args:
            chapter_content: Content of the chapter
            chapter_title: Title of the chapter

        Returns:
            Formatted prompt for NotebookLM
        """

        prompt = f"""Based on the following chapter content, generate a PowerPoint presentation outline in JSON format.

Chapter Title: {chapter_title}

Requirements:
1. Create 3-5 slides for the main content
2. Include 1 introduction slide
3. Include 1 conclusion/summary slide
4. Each slide should have a clear title and 3-5 bullet points
5. Output MUST be valid JSON with this exact structure:
{{
  "title": "Presentation Title",
  "subtitle": "Chapter Subtitle",
  "slides": [
    {{
      "title": "Slide Title",
      "content": ["bullet point 1", "bullet point 2", "bullet point 3"],
      "notes": "Optional speaker notes"
    }}
  ]
}}

Chapter Content:
{chapter_content[:8000]}

Please generate the JSON outline now. Ensure the output is valid JSON only, no additional text."""

        return prompt

    def generate_outline(self, chapter_content: str, chapter_title: str = "") -> Optional[Dict]:
        """
        Generate outline using NotebookLM

        Args:
            chapter_content: Content of the chapter
            chapter_title: Title of the chapter

        Returns:
            Parsed outline dictionary or None if failed
        """
        # Generate prompt
        prompt = self.generate_outline_prompt(chapter_content, chapter_title)

        print(f"Generating outline for: {chapter_title}")

        # Ask NotebookLM
        response = self.ask_notebooklm(prompt)

        if not response:
            return None

        # Try to extract JSON from response
        outline = self.extract_json_from_response(response)

        return outline

    def extract_json_from_response(self, response: str) -> Optional[Dict]:
        """
        Extract JSON from NotebookLM response

        Args:
            response: Raw response from NotebookLM

        Returns:
            Parsed JSON dictionary or None
        """
        # Try to find JSON in response
        import re

        # Look for JSON blocks
        json_pattern = r'\{[\s\S]*\}'
        matches = re.findall(json_pattern, response)

        for match in matches:
            try:
                outline = json.loads(match)

                # Validate structure
                if "slides" in outline and "title" in outline:
                    return outline

            except json.JSONDecodeError:
                continue

        # If no valid JSON found, try parsing entire response
        try:
            outline = json.loads(response.strip())

            if "slides" in outline and "title" in outline:
                return outline

        except json.JSONDecodeError:
            print("Warning: Could not extract valid JSON from response")
            print(f"Response preview: {response[:500]}...")

            # Return a basic outline structure
            return {
                "title": "Presentation",
                "slides": [
                    {
                        "title": "Content",
                        "content": ["Please see the source material"],
                        "notes": response[:500]
                    }
                ]
            }

        return None

    def load_markdown_content(self, md_path: Path) -> str:
        """Load markdown content from file"""
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()

    def save_outline(self, outline: dict, output_path: Path):
        """Save outline to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)

        print(f"Saved outline: {output_path}")


def batch_generate_outlines(
    markdown_files: List[Path],
    output_dir: Path,
    notebook_url: str
):
    """
    Generate outlines for multiple markdown files

    Args:
        markdown_files: List of markdown file paths
        output_dir: Output directory for outlines
        notebook_url: URL of NotebookLM notebook
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = NotebookLMClient(notebook_url=notebook_url)

    success_count = 0

    for i, md_file in enumerate(markdown_files, 1):
        print(f"\n[{i}/{len(markdown_files)}] Processing: {md_file.name}")

        # Load content
        content = client.load_markdown_content(md_file)

        # Generate outline
        outline = client.generate_outline(content, md_file.stem)

        if outline:
            # Save outline
            output_path = output_dir / f"{md_file.stem}_outline.json"
            client.save_outline(outline, output_path)
            success_count += 1
        else:
            print(f"Failed to generate outline for {md_file.name}")

    print(f"\nGenerated {success_count}/{len(markdown_files)} outlines")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate PPT outlines using NotebookLM'
    )
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Markdown files to process'
    )
    parser.add_argument(
        '--output-dir',
        default='./outlines',
        help='Output directory for outlines'
    )
    parser.add_argument(
        '--notebook-url',
        required=True,
        help='NotebookLM notebook URL'
    )

    args = parser.parse_args()

    markdown_files = [Path(f) for f in args.input_files]

    batch_generate_outlines(
        markdown_files,
        Path(args.output_dir),
        args.notebook_url
    )


if __name__ == '__main__':
    main()
