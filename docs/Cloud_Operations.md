# Cloud Operations

This project can run cloud validation without storing secrets in the repo.

## Default Path

- Code hosting: GitHub
- Cloud development: GitHub Codespaces via `.devcontainer/devcontainer.json`
- CI validation: `.github/workflows/cloud-validate.yml`
- Preview deployment: Vercel, Netlify, Cloudflare Pages, or a static server
- Monitoring: GitHub Actions schedule every 6 hours through `scripts/cloud_monitor.py`
- Report backflow: `.agent/memory/*-cloud.md` and workflow artifacts

## Required GitHub Settings

Set repository variable `PREVIEW_URL` after deployment, for example:

```text
https://your-project.vercel.app
```

No API keys are required for the built-in validation path. External services such as UptimeRobot or Better Stack should store their API keys in their own dashboards or GitHub Secrets, never in the repo.

## Commands

```bash
cd CourseApp
npm ci
npm run build
cd ..
python scripts/verify_course.py
python scripts/cloud_monitor.py --base-url http://localhost:4173 --write-memory
```

## Deployment Notes

- Vercel reads `vercel.json`.
- Netlify reads `netlify.toml`.
- Cloudflare Pages can use `wrangler.toml` or dashboard settings.
- Self-hosted static deployment should serve `CourseApp/dist` and rewrite unknown routes to `index.html`.
