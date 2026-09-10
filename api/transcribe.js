export const config = { api: { bodyParser: { sizeLimit: '25mb' } } };

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { audioBase64, mimeType, filename } = req.body;
  const apiKey = process.env.GROQ_API_KEY;

  if (!apiKey) return res.status(500).json({ error: 'GROQ_API_KEY not set in environment variables.' });
  if (!audioBase64) return res.status(400).json({ error: 'No audio data provided.' });

  try {
    // Convert base64 back to binary buffer
    const buffer = Buffer.from(audioBase64, 'base64');
    const mime = mimeType || 'audio/mp4';
    const ext = filename?.split('.').pop() || 'mp4';

    // Build multipart form — Groq Whisper requires multipart/form-data
    const boundary = '----FormBoundary' + Math.random().toString(36).slice(2);

    const header = Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.${ext}"\r\nContent-Type: ${mime}\r\n\r\n`
    );
    const modelPart = Buffer.from(
      `\r\n--${boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-large-v3\r\n--${boundary}--\r\n`
    );

    const body = Buffer.concat([header, buffer, modelPart]);

    const response = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
      },
      body: body
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ error: data.error?.message || 'Groq Whisper error' });
    }

    return res.status(200).json({ transcript: data.text || '' });

  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}