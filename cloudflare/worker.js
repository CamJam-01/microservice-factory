// Cloudflare Worker for the SEO Meta Description Generator
//
// This worker accepts a GET request with `title` and `description` query
// parameters and returns a JSON object with a generated meta description.  It
// uses the OpenAI API when available, falling back to simple truncation.

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const title = url.searchParams.get('title') || '';
    const description = url.searchParams.get('description') || '';

    if (!title || !description) {
      return new Response(JSON.stringify({ error: 'Missing title or description' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    let meta;
    if (env.OPENAI_API_KEY) {
      // Use OpenAI's ChatCompletion API to generate the meta description
      const prompt =
        `Generate an SEO meta description under 160 characters for a page titled "${title}" with this context: ${description}`;
      try {
        const openaiRes = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.OPENAI_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model: 'gpt-4o',
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 100
          })
        });
        const data = await openaiRes.json();
        meta = data.choices?.[0]?.message?.content?.trim().slice(0, 160);
      } catch (err) {
        meta = null;
      }
    }
    if (!meta) {
      // Fallback truncation logic
      meta = description.length > 160 ? description.slice(0, 157) + '...' : description;
    }
    return new Response(JSON.stringify({ meta }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
};