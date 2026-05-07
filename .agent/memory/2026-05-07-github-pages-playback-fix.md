# 2026-05-07 GitHub Pages Playback Fix

## Trigger

The user reported that the online GitHub Pages route could no longer play:

```text
https://gino-y.github.io/ShaderGUI_Learning_v1.0/module/Module_01/slide/p01
```

## Diagnosis

Two issues were confirmed:

1. The deep route returned 404 because `dist/404.html` was missing.
2. Audio and subtitles were referenced as root paths such as `/audio/Module_01/p01.mp3`, but GitHub Pages serves this project under `/ShaderGUI_Learning_v1.0/`.

The online audio file exists at:

```text
https://gino-y.github.io/ShaderGUI_Learning_v1.0/audio/Module_01/p01.mp3
```

## Fix

- `CourseApp/src/components/SlideNav.vue`
- `.agent/templates/course-app/src/components/SlideNav.vue`

Both now resolve public audio and subtitle assets through `import.meta.env.BASE_URL`.

Added:

- `CourseApp/scripts/postbuild-pages.mjs`
- `.agent/templates/course-app/scripts/postbuild-pages.mjs`

Updated:

- `CourseApp/package.json`
- `.agent/templates/course-app/package.json`

Build now writes:

```text
CourseApp/dist/404.html
CourseApp/dist/.nojekyll
```

## Verification

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

Both passed.

## DAG Impact

No DAG node order change. This strengthens the GitHub Pages deployment/runtime asset path gate.
