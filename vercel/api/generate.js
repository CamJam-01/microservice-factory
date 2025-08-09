// Vercel Serverless Function for the SEO Meta Description Generator
//
// This API accepts `title` and `description` as query parameters and
// responds with a JSON payload containing a generated meta description.  It
// uses the OpenAI API if the `OPENAI_API_KEY` environment variable is set.

export default async function handler(req, res) {
  const { title = '', description = '' } = req.query;
  if (!title || !description) {
    res.status(400).json({ error: 'Missing title or description' });
    return;
  }
  let meta;
  const openaiApiKey = process.env.OPENAI_API_KEY;
  if (openaiApiKey) {
    const prompt = `Generate an SEO meta description under 160 characters for a page titled "${title}" with this context: ${description}`;
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${openaiApiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'gpt-4o',
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 100
        })
      });
      const data = await response.json();
      meta = data.choices?.[0]?.message?.content?.trim().slice(0, 160);
    } catch (err) {
      meta = null;
    }
  }
  if (!meta) {
    meta = description.length > 160 ? description.slice(0, 157) + '...' : description;
  }
  res.status(200).json({ meta });
}