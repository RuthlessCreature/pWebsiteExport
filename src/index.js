const ALLOWED_EVENTS = new Set([
  'rfq_open',
  'rfq_submit',
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

function escapeHtml(value) {
  return value.replace(/[&<>\"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', "'": '&#39;' })[char]);
}

async function handleInquiry(request, env, url) {
  if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405);
  if (!sameSiteRequest(request, url)) return json({ error: 'forbidden' }, 403);

  const length = Number(request.headers.get('content-length') || 0);
  if (length > 12000) return json({ error: 'payload_too_large' }, 413);

  let rawBody;
  try { rawBody = await request.text(); } catch { return json({ error: 'invalid_json' }, 400); }
  if (new TextEncoder().encode(rawBody).byteLength > 12000) return json({ error: 'payload_too_large' }, 413);
  let body;
  try { body = JSON.parse(rawBody); } catch { return json({ error: 'invalid_json' }, 400); }
  const field = (key, max = 1200) => clean(body[key], max).trim();
  if (field('website', 200)) return json({ success: true });

  const name = field('name', 120);
  const email = field('email', 180).toLowerCase();
  const company = field('company', 160);
  const market = field('market', 120);
  const product = field('product', 240);
  const quantity = field('quantity', 120);
  const timing = field('timing', 120);
  const message = field('message', 4000);
  if (!name || !email || !message || message.length < 10 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || body.consent !== true) {
    return json({ error: 'validation_error' }, 400);
  }
  if (!env.EMAIL || typeof env.EMAIL.send !== 'function') return json({ error: 'email_unavailable' }, 503);

  const text = [
    'New Pomerol.trade sourcing inquiry',
    '', `Name: ${name}`, `Company: ${company || '-'}`, `Email: ${email}`,
    `Country/Market: ${market || '-'}`, `Product / Category: ${product || '-'}`,
    `Estimated quantity: ${quantity || '-'}`, `Target timing: ${timing || '-'}`,
    '', 'Message:', message, '', `Page: ${clean(body.page || '/', 240)}`
  ].join('\n');
  try {
    const result = await env.EMAIL.send({
      to: 'abd.yusuf.ibrahim.mustafa@gmail.com',
      from: { email: 'contact@pomerol.trade', name: 'Pomerol International Website' },
      replyTo: { email, name },
      subject: `[Pomerol.trade inquiry] ${product || company || name}`,
      text,
      html: `<div style="font-family:Arial,sans-serif;line-height:1.55"><h2>New sourcing inquiry</h2><pre style="white-space:pre-wrap">${escapeHtml(text)}</pre></div>`
    });
    return json({ success: true, messageId: result?.messageId || null }, 201);
  } catch (error) {
    console.error('Inquiry email delivery failed', error);
    return json({ error: 'email_delivery_failed' }, 502);
  }
}

function sameSiteRequest(request, url) {
  const origin = request.headers.get('origin');
  if (!origin) return true;
  try {
    const host = new URL(origin).hostname;
    return host === url.hostname || host === 'pomerol.trade' || host.endsWith('.nostalgia-ho.workers.dev');
  } catch {
    return false;
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.pomerol.trade') {
      url.hostname = 'pomerol.trade';
      if (url.pathname === '/' || url.pathname === '/index.html') url.pathname = '/en/';
      return Response.redirect(url.toString(), 308);
    }

    if (url.pathname === '/' || url.pathname === '/index.html') {
      url.pathname = '/en/';
      return Response.redirect(url.toString(), 308);
    }

    if (url.pathname === '/api/inquiry') return handleInquiry(request, env, url);

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
