export const config = {
  api: {
    bodyParser: {
      sizeLimit: '30mb',  // must be set here AND response size limit raised
    },
    responseLimit: '30mb',
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'GROQ_API_KEY not set.' });

  let body;
  try {
    body = req.body;
  } catch (e) {
    return res.status(400).json({ error: 'Failed to parse request body.' });
  }

  const { audioBase64, mimeType, filename } = body || {};
  if (!audioBase64) return res.status(400).json({ error: 'No audio data provided.' });

  try {
    const buffer = Buffer.from(audioBase64, 'base64');
    const mime = mimeType || 'audio/mp4';
    const ext = (filename?.split('.').pop()) || 'mp4';

    // Use FormData — more reliable than manual multipart
    const { FormData, Blob } = await import('node-fetch').catch(() => ({
      FormData: global.FormData,
      Blob: global.Blob
    }));

    // Node 18+ has built-in FormData and Blob
    const form = new global.FormData();
    form.append('file', new global.Blob([buffer], { type: mime }), `audio.${ext}`);
    form.append('model', 'whisper-large-v3');
    form.append('response_format', 'text');

    const response = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${apiKey}` },
      body: form,
    });

    if (!response.ok) {
      const errText = await response.text();
      return res.status(response.status).json({ error: errText });
    }

    const transcript = await response.text();
    return res.status(200).json({ transcript: transcript.trim() });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}