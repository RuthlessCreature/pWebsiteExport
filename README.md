# Pomerol International — Export & China Sourcing Website

Public corporate sourcing website for **Pomerol International Trade (Zhuhai) Co., Ltd. / 波美猴国际贸易（珠海）有限公司**.

**Official website:** https://pomerol.trade/en/

## Public discovery entry points

- Website: https://pomerol.trade/en/
- China sourcing services: https://pomerol.trade/services/
- China sourcing agent: https://pomerol.trade/china-sourcing-agent/
- Buyer guides: https://pomerol.trade/resources/guides/
- Case library: https://pomerol.trade/cases/
- HTML site directory: https://pomerol.trade/sitemap/
- XML sitemap: https://pomerol.trade/sitemap.xml
- Robots policy: https://pomerol.trade/robots.txt
- AI-readable site overview: https://pomerol.trade/llms.txt
- Contact and inquiry page: https://pomerol.trade/contact/

## Business Contact

**Yusuf**
- Tel: +86 132 4269 4270
- Email: abd.yusuf.ibrahim.mustafa@gmail.com

The production site currently publishes English, Chinese, Japanese, Russian, Spanish and Portuguese content, including multilingual buyer guides with reciprocal `hreflang` relationships.

## Positioning

- China supplier sourcing and RFQ management
- OEM / ODM and custom manufacturing coordination
- Supplier qualification and factory audit coordination
- Quality inspection and shipment readiness
- Consolidation, export documentation and logistics coordination
- Industrial, automotive, energy, packaging, electronics and general merchandise sourcing

## Stack

Cloudflare Workers Static Assets. The public website has no OpenAI/ChatGPT runtime dependency, no database dependency, and no third-party JavaScript/CSS CDN dependency for core rendering or navigation.

## Production deployment

The Worker name is `pwebsite-export` and the production custom domain is **pomerol.trade**. Pushes to `main` run the SEO build/audit gates and deploy through GitHub Actions to Cloudflare Workers.

The production SEO pipeline validates canonical URLs, XML sitemap coverage, reciprocal multilingual `hreflang`, buyer-guide coverage, case/landing-page generation, static internal links, HTML sitemap discovery, public contact source truth and the active IndexNow verification key. Successful production deployments submit the canonical URL set through IndexNow.

## Local development

```bash
npm install
npm run dev
```

## Deploy

```bash
npm run deploy:dry
npm run deploy
```

## Content integrity

The case studies are explicitly described as representative engagement playbooks. They illustrate sourcing scope, workflow and control points; they are not claims about named customers or completed transactions unless a page is later replaced with verified customer evidence.
