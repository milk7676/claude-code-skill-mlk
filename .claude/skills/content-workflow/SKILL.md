---
name: content-workflow
description: Complete content creation workflow from user requirements to final presentation. Use when user needs to create comprehensive content including articles and presentations: (1) Interactive requirement gathering about topic, audience, length, and objectives, (2) Process user-uploaded reference documents for research materials, (3) Generate article outline, (4) Write full article based on outline, (5) Generate PPT outline, (6) Create speaker script/talking points, (7) Generate PowerPoint presentation from outline using pptx skill. This skill handles the entire content production pipeline from ideation to final presentation deck.
---

# Content Workflow

Complete workflow for creating articles and presentations from user requirements.

## When to Use This Skill

Use this skill when users need to:
- Create a presentation with accompanying article and speaker notes
- Transform reference materials into structured content
- Build comprehensive content packages (article + slides + script)

## Workflow Steps

### Step 1: Gather Requirements

Ask the user for:
- **Topic**: What is the subject matter?
- **Target Audience**: Who will read/view this content?
- **Content Type**: Educational, persuasive, informational, inspirational?
- **Length Requirements**: Article word count, PPT slide count
- **Key Points**: Must-cover information or messages
- **Tone/Style**: Formal, casual, professional, academic?

### Step 2: Collect Reference Materials

Request user to upload reference documents:
- PDFs, Word documents, Markdown files
- Research papers, articles, notes
- Any source materials to incorporate

**Process the references:**
1. Read all uploaded documents using Read tool
2. Extract key information, facts, and data points
3. Organize by themes or sections
4. Identify quotes, statistics, examples to include

### Step 3: Generate Article Outline

Create a structured article outline:

```markdown
# Title: [Article Title]

## I. Introduction
- Hook/Opening
- Background context
- Thesis statement

## II. Main Section 1
- Key point A
- Key point B
- Supporting evidence

## III. Main Section 2
...

## IV. Conclusion
- Summary of key points
- Call to action or closing thought
```

**Best practices:**
- 3-5 main sections for standard articles
- Logical flow and progression
- Balance between sections
- Include references to source materials

### Step 4: Generate Full Article

Write the complete article based on outline:

**Structure:**
1. **Engaging introduction** - Hook reader, establish context
2. **Body paragraphs** - Each main point with supporting evidence
3. **Smooth transitions** - Connect ideas logically
4. **Strong conclusion** - Reinforce main message

**Writing guidelines:**
- Use information from reference materials
- Incorporate quotes, data, examples from sources
- Maintain consistent tone throughout
- Use clear headings and subheadings
- Target the specified word count

### Step 5: Generate PPT Outline

Convert article into presentation outline:

**Structure:**
```markdown
Slide 1: Title Slide
- Title
- Subtitle/presenter info

Slide 2: Agenda/Overview
- Main topics to cover

Slide 3-5: Content Slides (one per main section)
- Heading: Section title
- Bullet points: 3-5 key points
- Visual suggestions: Charts, images, diagrams

Slide N: Conclusion
- Summary points
- Call to action

Slide N+1: Q&A / Thank You
```

**Guidelines:**
- One main idea per slide
- 3-5 bullet points maximum per slide
- Include speaker note hints
- Suggest visual elements where appropriate
- Plan for 1-2 minutes per slide

### Step 6: Generate Speaker Script

Create detailed speaking notes for each slide:

**For each slide:**
```markdown
## Slide [N]: [Slide Title]

**Visual Elements:** [What's on screen]

**Speaker Notes:**
[Detailed script - 2-3 sentences per bullet point]

- Talking point 1: [Elaboration with examples, stories]
- Talking point 2: [Elaboration with data, evidence]
- Talking point 3: [Elaboration with connections]

**Transition:** [How to move to next slide]
```

**Script writing tips:**
- Write in spoken language (conversational, natural)
- Include stories, analogies, examples
- Mark emphasis points (pause, stress)
- Include questions to ask audience
- Note where to reference visuals
- Time for ~1 minute per slide

### Step 7: Generate PowerPoint

Use the `pptx` skill to create the actual presentation:

1. Call `pptx` skill with the PPT outline
2. Provide additional context:
   - Slide count
   - Visual style preferences (minimal, colorful, corporate, creative)
   - Brand colors if specified
   - Any charts/graphs needed

The pptx skill will handle:
- Slide layout and design
- Visual hierarchy
- Professional formatting
- Speaker notes integration

## Quality Checklist

Before presenting final output to user:

- [ ] Article meets word count requirement
- [ ] Article incorporates reference materials
- [ ] Article has clear structure and flow
- [ ] PPT outline has logical progression
- [ ] PPT slide count is appropriate (typically 10-20 slides)
- [ ] Speaker script is conversational and natural
- [ ] All key points from requirements are covered
- [ ] Tone matches target audience

## Variations

**Academic/Research Presentation:**
- More formal tone
- Citations and references
- Data-heavy slides
- Detailed methodology section

**Business/Professional:**
- Concise bullet points
- Business metrics and ROI
- Clear call-to-action
- Professional design templates

**Educational/Training:**
- Learning objectives stated
- Clear explanations
- Examples and analogies
- Practice exercises or discussion questions
