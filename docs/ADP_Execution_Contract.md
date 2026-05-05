# ADP Execution Contract

## Purpose
This contract defines the execution boundaries and cleanup scope for ADPMCP (full ADP generation, not MVP).

## Cleanup Scope
ADPMCP cleans the following paths before generating:
- `CourseApp/src` - Regenerated from templates
- `CourseApp/public` - Regenerated (audio, transcripts, etc.)
- `CourseApp/dist` - Rebuilt
- `CourseApp/package.json` - Regenerated from templates
- `CourseApp/index.html` - Regenerated from templates
- `CourseApp/vite.config.js` - Regenerated from templates
- `CourseApp/tailwind.config.js` - Regenerated from templates
- `CourseApp/postcss.config.js` - Regenerated from templates
- `scripts/generate_audio.py` - Regenerated from templates
- `scripts/verify_course.py` - Regenerated from templates

## Deny List
The following paths are NEVER cleaned:
- `.agent/**` - Agent configuration and state
- `.git/**` - Git repository data
- `docs/**` - Documentation
- `CourseApp/node_modules/**` - Dependencies (preserved)
- `CourseApp/package-lock.json` - Lock file (preserved)
- `node_modules/**` - Root dependencies
- `.env` - Environment variables
- `**/.env` - Nested environment variables

## Readonly List
The following paths are readonly (never modified by ADPMCP):
- `.agent/**`
- `docs/**`
- `CourseApp/node_modules/**`
- `CourseApp/package-lock.json`

## Pipeline Steps
1. `adp_generate` - Generate all course slides (full ADP)
2. `storyboard_prepare` - Prepare storyboard contracts
3. `storyboard_validate` - Validate storyboard contracts
4. `design_prepare` - Prepare design contracts
5. `design_validate` - Validate design contracts
6. `audio` - Generate audio files
7. `stitch` - Stitch everything together
8. `verify` - Verify the build
9. `build` - Build the production bundle

## Notes
- ADPMCP is a parallel DAG node to MVPMCP
- ADPMCP reads from `adp-scope.json` (not `mvp-scope.json`)
- ADPMCP generates ALL slides (not just MVP slides)
- Cleanup scope is defined in `.agent/adp-execution-scope.json`
