import formidable from 'formidable';
import fs from 'fs';

export const config = {
  api: { bodyParser: false }  // disable body parser — we handle raw multipart
};

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'GROQ_API_KEY not set.' });

  try {
    // Parse multipart form from frontend
    const form = formidable({ maxFileSize: 25 * 1024 * 1024 });
    const [fields, files] = await form.parse(req);

    const file = files.file?.[0];
    if (!file) return res.status(400).json({ error: 'No file uploaded.' });

    // Read the temp file and build FormData for Groq
    const fileBuffer = fs.readFileSync(file.filepath);
    const mimeType = file.mimetype || 'video/mp4';
    const origName = file.originalFilename || 'audio.mp4';

    const form2 = new FormData();
    form2.append('file', new Blob([fileBuffer], { type: mimeType }), origName);
    form2.append('model', 'whisper-large-v3');
    form2.append('response_format', 'text');

    const response = await fetch('https://api.groq.com/openai/v1/audio/transcriptions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${apiKey}` },
      body: form2,
    });

    // Cleanup temp file
    fs.unlinkSync(file.filepath);

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