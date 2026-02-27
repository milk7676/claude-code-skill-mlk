"""
PPT Merger - Merge multiple PowerPoint presentations into one
Maintains iSlide formatting and slide order
"""

from pathlib import Path
from typing import List
import win32com.client
from pythonpptx import Presentation


class PPTMerger:
    """Merge multiple PPT presentations"""

    def __init__(self):
        self.powerpoint = None
        self.merged_presentation = None

    def init_powerpoint(self):
        """Initialize PowerPoint application"""
        try:
            self.powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            self.powerpoint.Visible = True

            # Create new merged presentation
            self.merged_presentation = self.powerpoint.Presentations.Add()

        except Exception as e:
            print(f"Error initializing PowerPoint: {e}")
            raise

    def close_powerpoint(self, save_path: Path):
        """Close and save merged presentation"""
        if self.merged_presentation:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            self.merged_presentation.SaveAs(str(save_path))
            self.merged_presentation.Close()

        if self.powerpoint:
            self.powerpoint.Quit()

    def merge_presentations(self, ppt_files: List[Path], output_path: Path):
        """
        Merge multiple PPT files into one presentation
        Maintains slide order and formatting
        """
        # Initialize PowerPoint
        self.init_powerpoint()

        # Track slide count
        total_slides = 0

        # Process each presentation
        for i, ppt_file in enumerate(ppt_files):
            print(f"Processing: {ppt_file.name}")

            try:
                # Open source presentation
                source_presentation = self.powerpoint.Presentations.Open(str(ppt_file))

                # Copy each slide from source to merged presentation
                for source_slide in source_presentation.Slides:
                    source_slide.Copy()
                    self.merged_presentation.Slides.Paste()
                    total_slides += 1

                # Close source presentation
                source_presentation.Close()

            except Exception as e:
                print(f"Error processing {ppt_file.name}: {e}")
                continue

        # Add title slide at the beginning
        self._add_title_slide(output_path.stem, len(ppt_files))

        # Save merged presentation
        print(f"\nMerged {total_slides} slides from {len(ppt_files)} presentations")
        self.close_powerpoint(output_path)

    def _add_title_slide(self, book_title: str, chapter_count: int):
        """Add title slide at the beginning"""
        try:
            # Insert at position 1
            layout = self.merged_presentation.Slides(1).CustomLayouts[1]
            title_slide = self.merged_presentation.Slides.Add(1, layout)

            # Set title
            title_slide.Shapes.Title.TextFrame.TextRange.Text = book_title.replace('_', ' ').title()

            # Set subtitle
            subtitle = f"Complete Book Presentation\n{chapter_count} Chapters"
            subtitle_shape = title_slide.Shapes.AddTextbox(
                1,  # msoTextOrientationHorizontal
                100, 100, 600, 100  # Left, Top, Width, Height (points)
            )
            subtitle_shape.TextFrame.TextRange.Text = subtitle

        except Exception as e:
            print(f"Warning: Could not add title slide: {e}")

    def merge_with_python_pptx(self, ppt_files: List[Path], output_path: Path):
        """
        Alternative method using python-pptx (slower but more compatible)
        Use this if win32com has issues
        """
        merged_presentation = Presentation()

        for ppt_file in ppt_files:
            print(f"Processing: {ppt_file.name}")

            try:
                # Load source presentation
                source_presentation = Presentation(ppt_file)

                # Copy each slide
                for source_slide in source_presentation.slides:
                    # Create new slide with same layout
                    slide_layout = merged_presentation.slide_layouts[source_slide.slide_layout.index]
                    new_slide = merged_presentation.slides.add_slide(source_slide.slide_layout.index)

                    # Copy shapes (simplified - may not preserve all formatting)
                    for shape in source_slide.shapes:
                        if shape.has_text_frame:
                            self._copy_text_frame(shape.text_frame, new_slide)

            except Exception as e:
                print(f"Error processing {ppt_file.name}: {e}")
                continue

        # Save merged presentation
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged_presentation.save(output_path)
        print(f"Saved merged presentation: {output_path}")

    def _copy_text_frame(self, source_text_frame, target_slide):
        """Helper to copy text frame (simplified)"""
        # This is a placeholder - full implementation would need to handle all shape types
        pass


def main():
    import argparse

    parser = argparse_description = argparse.ArgumentParser(description='Merge multiple PPT files')
    parser.add_argument('ppt_files', nargs='+', help='PPT files to merge')
    parser.add_argument('--output', default='merged_book.pptx', help='Output PPT file')
    parser.add_argument('--use-python-pptx', action='store_true',
                       help='Use python-pptx instead of win32com')

    args = parser.parse_args()

    ppt_files = [Path(f) for f in sorted(args.ppt_files)]
    output_path = Path(args.output)

    merger = PPTMerger()

    if args.use_python_pptx:
        merger.merge_with_python_pptx(ppt_files, output_path)
    else:
        merger.merge_presentations(ppt_files, output_path)


if __name__ == '__main__':
    main()
