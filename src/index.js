const ALLOWED_EVENTS = new Set([
  'rfq_open',
  'rfq_mailto_submit',
  'whatsapp_click',
  'email_click',
  'phone_click',
  'resource_download',
  'contact_click'
]);

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'x-content-type-options': 'nosniff'
  }
});

function clean(value, max = 240) {
  return String(value || '').replace(/[\u0000-\u001f\u007f]/g, '').slice(0, max);
}

function referrerHost(value) {
  try { return new URL(value).hostname.slice(0, 120); } catch { return ''; }
}

function sameSiteRequest(request, url) {
  const origin = request.headers.get('origin');
  if (!origin) return true;
  try {
    const host = new URL(origin).hostname;
    return host === url.hostname || host === 'pomerol.in' || host.endsWith('.nostalgia-ho.workers.dev');
  } catch {
    return false;
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/event') {
      if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
      if (!sameSiteRequest(request, url)) return json({ error: 'forbidden' }, 403);

      const length = Number(request.headers.get('content-length') || 0);
      if (length > 4096) return json({ error: 'payload_too_large' }, 413);

      let body;
      try { body = await request.json(); } catch { return json({ error: 'invalid_json' }, 400); }

      const event = clean(body.event, 48);
      if (!ALLOWED_EVENTS.has(event)) return json({ error: 'invalid_event' }, 400);

      const page = clean(body.page || url.pathname, 240);
      const target = clean(body.target, 240);
      const language = clean(body.language, 16);
      const country = clean(request.cf?.country, 8);
      const referrer = referrerHost(request.headers.get('referer') || '');

      env.ANALYTICS.writeDataPoint({
        indexes: [event],
        blobs: [page, target, language, country, referrer]
      });

      return new Response(null, {
        status: 204,
        headers: {
          'cache-control': 'no-store',
          'x-content-type-options': 'nosniff'
        }
      });
    }

    return env.ASSETS.fetch(request);
  }
};
