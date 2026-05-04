# v0 React Prototype Handoff

- Provider: `v0`
- Status: `prototype_ready`
- Module: `Module_01`
- Chat ID: `qAnaC7HeGO9`
- Chat URL: `https://v0.app/chat/qAnaC7HeGO9`

## Vue Translation Rules

### layout
- Dark full-screen course player shell with a luminous slide canvas centered above subtitles and controls.
- Concept slides use a hero statement plus three progressive content cards.
- Code slides use a split reading path: principle cards beside a high-contrast code panel.

### visual
- Use deep slate/neutral backgrounds, cyan or emerald accents, soft radial highlights, and glass-like cards.
- Keep controls outside the learner-facing slide canvas.
- Reserve strong accent treatments for the current teaching beat or code callout.

### interaction
- Bottom controls stay compact and touch-friendly.
- Subtitles remain event-driven and visually separate from full transcripts.
- Mobile surface tap toggles playback; vertical swipe navigates slides.
- 做题页 renders the question bank table first, then answer cards and immediate feedback.
- Option swapping, answer selection, submission, reset, and scoring must remain live Vue state interactions.

## React Prototype Files

- `app/globals.css`
- `package.json`
- `app/layout.tsx`
- `components/course/SlideCanvas.tsx`
- `components/course/AudioBar.tsx`
- `components/course/SubtitleBar.tsx`
- `components/course/NavDots.tsx`
- `components/course/CoursePlayer.tsx`
- `components/course/QuizView.tsx`
- `app/page.tsx`
