# PPT Style Configuration Guide

## iSlide Integration

### Prerequisites

1. **Install iSlide Plugin**
   - Download from: https://www.islide.cc/
   - Install in PowerPoint
   - Verify installation: PowerPoint Ribbon → iSlide tab

2. **iSlide COM Interface**
   ```python
   # Example automation (requires actual iSlide API docs)
   powerpoint.Run("iSlide.ApplyTheme", theme_id)
   powerpoint.Run("iSlide.ApplyLayout", layout_id)
   ```

### Theme Templates

Common iSlide theme categories:

1. **Business** - Professional, clean
2. **Education** - Academic, structured
3. **Technology** - Modern, minimalist
4. **Creative** - Colorful, dynamic

## Slide Layouts

### Standard Layouts

```python
# PowerPoint built-in layouts
LAYOUTS = {
    'title': 0,           # Title slide
    'title_content': 1,   # Title and content
    'section_header': 2,  # Section header
    'two_content': 3,     # Two content columns
    'comparison': 4,      # Comparison
    'title_only': 5,      # Title only
    'blank': 6,           # Blank
    'content_caption': 7, # Content with caption
}
```

### Custom Layout Creation

```python
def create_custom_layout(presentation):
    """Create custom slide layout"""
    # Add master slide
    master = presentation.slide_masters[0]

    # Add custom layout
    custom_layout = master.slide_layouts.add_layout(1)

    # Customize placeholder positions
    # ...
```

## Color Schemes

### Professional Color Palettes

```python
COLOR_SCHEMES = {
    'blue': {
        'primary': '1F4E78',
        'secondary': '4472C4',
        'accent': 'FFC000',
        'background': 'FFFFFF',
        'text': '000000'
    },
    'green': {
        'primary': '2E5030',
        'secondary': '70AD47',
        'accent': 'FF0000',
        'background': 'FFFFFF',
        'text': '000000'
    },
    'red': {
        'primary': '7F2E2E',
        'secondary': 'C00000',
        'accent': 'FFC000',
        'background': 'FFFFFF',
        'text': '000000'
    }
}
```

### Apply Color Scheme

```python
def apply_color_scheme(slide, scheme):
    """Apply color scheme to slide"""
    # Set background
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = hex_to_rgb(scheme['background'])

    # Set text colors
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                paragraph.font.color.rgb = hex_to_rgb(scheme['text'])
```