# Runtime Architecture Gate

This site must remain a pure Cloudflare Workers Static Assets website.

## Allowed runtime dependencies

- Cloudflare Workers / Workers Static Assets
- Local HTML, CSS, JavaScript, SVG, PNG/JPG/WebP and downloadable files shipped with the Worker
- Browser-native capabilities such as `mailto:` and `tel:`
- Optional outbound links such as WhatsApp that are not required for the site itself to render or function

## Forbidden runtime dependencies

- ChatGPT-hosted sites or embeds
- OpenAI / ChatGPT APIs
- Any AI service required for rendering or navigation
- Third-party JavaScript or CSS CDNs
- Google Fonts or other externally hosted fonts
- Externally hot-linked images required for page rendering
- Third-party databases or APIs required to load the core website

A visitor must be able to use the website even when ChatGPT/OpenAI and other unrelated third-party services are unavailable in the visitor's region.
