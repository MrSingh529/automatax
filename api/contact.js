// /api/contact.js
// Vercel Serverless Function to handle contact form submissions

import nodemailer from 'nodemailer';

// Configure body parsing (if needed adjust for urlencoded)
export const config = {
  api: {
    bodyParser: true,   // Next.js will parse JSON bodies by default
  }
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { name, email, subject, message } = req.body;
  if (!name || !email || !subject || !message) {
    return res.status(400).json({ error: 'Missing required fields.' });
  }

  // Create a transporter using SMTP (Gmail example). You can use any SMTP provider.
  let transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,    // e.g. your Gmail address
      pass: process.env.EMAIL_PASS,    // e.g. an App Password
    },
  });

  const mailOptions = {
    from: `${name} <${email}>`,        // sender address
    to: 'sales@automataxpro.site',      // your sales inbox
    subject: `[Contact Form] ${subject}`,
    text: `Name: ${name}\nEmail: ${email}\n\n${message}`,
    html: `
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Message:</strong><br/>${message.replace(/\n/g, '<br/>')}</p>
    `,
  };

  try {
    await transporter.sendMail(mailOptions);
    return res.status(200).json({ ok: true, message: 'Email sent.' });
  } catch (err) {
    console.error('Error sending email:', err);
    return res.status(500).json({ error: 'Failed to send email.' });
  }
}

/*
Environment Variables (set in Vercel dashboard under Settings → Environment Variables):
  EMAIL_USER = your-email@example.com
  EMAIL_PASS = your-email-app-password
*/
