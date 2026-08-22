# Production deployment trigger

Cloudflare Workers production deployment is automated through `.github/workflows/deploy-cloudflare.yml`.

Required GitHub Actions repository secrets:

- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`

Worker name: `pwebsite-export`.

This file also provides an auditable marker for the first deployment performed after repository credentials were configured.
