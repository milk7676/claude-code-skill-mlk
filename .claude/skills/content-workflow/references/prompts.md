# Prompt Templates

This file contains detailed prompt templates for each workflow step. Load this when you need specific guidance on crafting prompts for a particular stage.

## Article Outline Generation Prompt Template

```
Based on the user requirements and reference materials, create a comprehensive article outline:

**Topic**: {topic}
**Audience**: {audience}
**Length**: {word_count} words
**Key Points**: {key_points}
**Tone**: {tone}

**Reference Materials Summary**:
{reference_summary}

Create an outline with:
1. Compelling title options (3-5 suggestions)
2. Introduction with hook and thesis
3. 3-5 main sections with subsections
4. Conclusion with call-to-action
5. Notes on which references to use in each section

Ensure logical flow and balanced structure.
```

## Article Writing Prompt Template

```
Write the full article based on the approved outline:

**Outline**:
{outline}

**Reference Materials**:
{reference_details}

**Requirements**:
- Target length: {word_count} words
- Tone: {tone}
- Audience: {audience}

**Writing Guidelines**:
1. Start with engaging hook in introduction
2. Develop each main section with 2-3 paragraphs
3. Incorporate evidence, quotes, data from references
4. Use smooth transitions between sections
5. End with strong conclusion and call-to-action
6. Use {formatting_style} headings and formatting

Write complete, polished article ready for publication.
```

## PPT Outline Generation Prompt Template

```
Convert the article into a presentation outline:

**Article**:
{article_summary}

**Requirements**:
- Target slide count: {slide_count} slides
- Presentation length: {presentation_minutes} minutes
- Visual style: {visual_style}

**Create slide-by-slide outline**:

Slide 1: Title Slide
- Main title
- Subtitle/presenter info

Slide 2: Overview/Agenda
- 3-5 main topics

Slides 3-N: Content Slides
For each main section:
- Create 1-3 slides
- 3-5 bullet points per slide
- Note visual elements needed (charts, images, diagrams)
- Highlight key data or quotes

Final slides: Conclusion + Q&A

Ensure each slide has ONE main idea and clear visual hierarchy.
```

## Speaker Script Generation Prompt Template

```
Create detailed speaker notes for each slide:

**PPT Outline**:
{ppt_outline}

**Article Content**:
{article_content}

**Presentation Style**: {presentation_style}
**Audience**: {audience}

**For each slide, provide**:

## Slide [N]: [Title]

**On Screen**: [Visual elements summary]

**Speaker Script** (150-200 words per slide):
- Opening: Introduce the slide topic
- Point 1: [Talking point with example/story]
- Point 2: [Talking point with data/evidence]
- Point 3: [Talking point with application]
- Transition: [Link to next slide]

**Notes**:
- [Emphasis points - where to pause or stress]
- [Questions to ask audience]
- [References to visual elements]

Write in natural, conversational spoken language. Include stories, examples, and transitions.
```

## Tone and Style Guide

### Formal/Academic
- Use third-person perspective
- Complete sentences, proper grammar
- Technical terminology where appropriate
- Objective language
- Citations and references

### Professional/Business
- Second or third person
- Clear, concise language
- Active voice
- Business metrics and ROI focus
- Action-oriented language

### Conversational/Educational
- First or second person ("we", "you")
- Simpler vocabulary
- Stories and analogies
- Questions to engage audience
- Relatable examples

### Inspirational/Motivational
- Emotional language
- Rhetorical devices (repetition, rule of three)
- Stories and personal connections
- Future-focused vision
- Call-to-action emphasis
