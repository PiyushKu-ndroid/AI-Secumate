// api/transform.js (Runs securely on Vercel's server)
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { prompt } = req.body;
  const apiKey = process.env.GEMINI_API_KEY; // Read securely from Vercel

  if (!apiKey) {
    return res.status(500).json({ error: 'Server GEMINI_API_KEY is not configured.' });
  }

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key=${apiKey}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }]
      })
    });

    const data = await response.json();
    if (data.candidates && data.candidates[0].content.parts[0].text) {
      return res.status(200).json({ text: data.candidates[0].content.parts[0].text });
    } else {
      return res.status(500).json({ error: 'Failed to generate content from Gemini' });
    }
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}