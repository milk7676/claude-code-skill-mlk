"""
Book to PPT - Complete workflow with real NotebookLM integration
Automates: PDF -> Chapters -> Markdown -> NotebookLM -> PPTs -> Merged PPT
"""

import sys
from pathlib import Path
from typing import Optional

# Import our modules
from pdf_splitter import PDFSplitter
from notebooklm_client import NotebookLMClient, batch_generate_outlines
from ppt_generator import PPTGenerator, batch_generate_ppts
from ppt_merger import PPTMerger


class BookToPPTWorkflow:
    """Complete workflow: PDF Book -> PPT Presentation with NotebookLM"""

    def __init__(
        self,
        pdf_path: str,
        notebook_url: str,
        output_dir: str = "./output",
        use_iSlide: bool = True
    ):
        self.pdf_path = Path(pdf_path)
        self.notebook_url = notebook_url
        self.output_dir = Path(output_dir)

        # Create subdirectories
        self.chapters_dir = self.output_dir / "chapters"
        self.outlines_dir = self.output_dir / "outlines"
        self.ppts_dir = self.output_dir / "presentations"

        self.use_iSlide = use_iSlide

        # Track progress
        self.chapter_files = []
        self.markdown_files = []
        self.outline_files = []
        self.ppt_files = []

    def step1_split_pdf(self):
        """Step 1: Split PDF into chapters"""
        print("\n" + "="*60)
        print("STEP 1: Splitting PDF into chapters")
        print("="*60)

        splitter = PDFSplitter(self.pdf_path, self.chapters_dir)

        # Split PDF by chapters
        self.chapter_files = splitter.split_by_chapters()

        # Extract markdown for each chapter
        self.markdown_files = []
        for chapter_pdf in self.chapter_files:
            md_path = splitter.extract_markdown(chapter_pdf)
            self.markdown_files.append(md_path)

        print(f"\n✓ Created {len(self.chapter_files)} chapter files")
        print(f"✓ Extracted {len(self.markdown_files)} markdown files")

    def step2_upload_to_notebooklm(self):
        """Step 2: Guide user to upload chapters to NotebookLM"""
        print("\n" + "="*60)
        print("STEP 2: Upload Chapters to NotebookLM")
        print("="*60)

        print("\n⚠️ IMPORTANT: You need to upload the chapter files to NotebookLM")
        print(f"\nYour Notebook URL: {self.notebook_url}")
        print(f"\nFiles to upload ({len(self.markdown_files)} files):")

        for i, md_file in enumerate(self.markdown_files, 1):
            print(f"  {i}. {md_file}")

        print("\n" + "-"*60)
        print("ACTIONS REQUIRED:")
        print("1. Open your Notebook in a browser:")
        print(f"   {self.notebook_url}")
        print("\n2. Upload ALL markdown files from:")
        print(f"   {self.chapters_dir.absolute()}")
        print("\n3. Wait for NotebookLM to process all files")
        print("\n4. Press Enter to continue when files are uploaded...")

        input("\n⏎ Press Enter after uploading files to NotebookLM...")

        print("\n✓ Continuing to outline generation...")

    def step3_generate_outlines(self):
        """Step 3: Generate PPT outlines using NotebookLM"""
        print("\n" + "="*60)
        print("STEP 3: Generating PPT outlines with NotebookLM")
        print("="*60)

        print(f"\nNotebook URL: {self.notebook_url}")
        print(f"Processing {len(self.markdown_files)} chapters...")

        batch_generate_outlines(
            self.markdown_files,
            self.outlines_dir,
            self.notebook_url
        )

        # Find generated outline files
        self.outline_files = sorted(self.outlines_dir.glob("*_outline.json"))
        print(f"\n✓ Generated {len(self.outline_files)} outline files")

    def step4_generate_ppts(self):
        """Step 4: Generate PPTs from outlines"""
        print("\n" + "="*60)
        print("STEP 4: Generating PPT presentations")
        print("="*60)

        batch_generate_ppts(
            self.outlines_dir,
            self.ppts_dir,
            use_iSlide=self.use_iSlide
        )

        # Find generated PPT files
        self.ppt_files = sorted(self.ppt_files)
        self.ppt_files = sorted(self.ppts_dir.glob("*.pptx"))
        print(f"\n✓ Generated {len(self.ppt_files)} presentation files")

    def step5_merge_ppts(self, output_name: Optional[str] = None):
        """Step 5: Merge all PPTs into one"""
        print("\n" + "="*60)
        print("STEP 5: Merging all presentations")
        print("="*60)

        if output_name is None:
            output_name = self.pdf_path.stem + "_complete.pptx"

        output_path = self.output_dir / output_name

        merger = PPTMerger()
        merger.merge_presentations(self.ppt_files, output_path)

        print(f"\n✓ Merged presentation saved: {output_path}")

    def run_complete_workflow(self):
        """Run the complete workflow"""
        print("\n" + "="*60)
        print("BOOK TO PPT - COMPLETE WORKFLOW")
        print("WITH REAL NOTEBOOKLM INTEGRATION")
        print("="*60)
        print(f"Input PDF: {self.pdf_path}")
        print(f"Notebook: {self.notebook_url}")
        print(f"Output Directory: {self.output_dir}")

        try:
            # Step 1: Split PDF
            self.step1_split_pdf()

            # Step 2: Upload to NotebookLM (manual)
            self.step2_upload_to_notebooklm()

            # Step 3: Generate outlines with NotebookLM
            self.step3_generate_outlines()

            # Step 4: Generate PPTs
            self.step4_generate_ppts()

            # Step 5: Merge PPTs
            self.step5_merge_ppts()

            print("\n" + "="*60)
            print("✓ WORKFLOW COMPLETE!")
            print("="*60)
            print(f"\nFinal presentation:")
            print(f"  {self.output_dir / (self.pdf_path.stem + '_complete.pptx')}")

            print(f"\nAll outputs saved to: {self.output_dir.absolute()}")
            print("\nOutput structure:")
            print(f"  - Chapters:      {self.chapters_dir}")
            print(f"  - Outlines:      {self.outlines_dir}")
            print(f"  - Presentations: {self.ppts_dir}")

        except KeyboardInterrupt:
            print("\n\n⚠️ Workflow interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error during workflow: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert PDF book to PowerPoint using NotebookLM'
    )
    parser.add_argument('pdf_path', help='Path to PDF book')
    parser.add_argument('--notebook-url', required=True,
                       help='NotebookLM notebook URL')
    parser.add_argument('--output-dir', default='./output',
                       help='Output directory')
    parser.add_argument('--no-islide', action='store_true',
                       help='Disable iSlide integration')

    args = parser.parse_args()

    workflow = BookToPPTWorkflow(
        args.pdf_path,
        notebook_url=args.notebook_url,
        output_dir=args.output_dir,
        use_iSlide=not args.no_islide
    )

    workflow.run_complete_workflow()


if __name__ == '__main__':
    main()
