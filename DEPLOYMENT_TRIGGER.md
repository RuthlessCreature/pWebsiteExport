# Deployment trigger

This file documents the production deployment path for the export website.

- Production deploys are handled by `.github/workflows/deploy-cloudflare.yml`.
- The workflow runs on pushes to `main` and can also be dispatched manually from GitHub Actions.
- Required repository secrets: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.
- Worker name: `pwebsite-export`.

This commit was added to trigger a fresh production deployment after Cloudflare credentials were configured.
