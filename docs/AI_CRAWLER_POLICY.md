# Search and AI crawler policy

The production `robots.txt` allows public search crawlers, including Googlebot, Bingbot, YandexBot and Baiduspider. It also explicitly allows OpenAI's OAI-SearchBot, Anthropic's Claude-SearchBot, PerplexityBot and Apple's Applebot so public pages can be discovered for search and user-requested answers.

Training crawlers GPTBot, ClaudeBot and Applebot-Extended are disallowed. User-triggered fetchers ChatGPT-User, Claude-User and Perplexity-User remain allowed for public pages. Google-Extended remains governed by the default rule pending a choice because Google uses it for both Gemini grounding and model-training controls.

These directives set crawler access preferences; they do not guarantee indexing, citations or search rankings. Cloudflare WAF and bot controls must also avoid challenging verified search crawlers.
