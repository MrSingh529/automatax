// api/contact.js
import nodemailer from "nodemailer";

export default async function handler(req, res) {
  if (req.method === "POST") {
    const { name, email, message } = req.body;

    // 1. Configure your SMTP transport (example: Gmail)
    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: process.env.GMAIL_USER,  // e.g. "youremail@gmail.com"
        pass: process.env.GMAIL_PASS   // an App Password or your Gmail password
      }
    });

    try {
      // 2. Send mail
      await transporter.sendMail({
        from: `"AutomataX Contact" <${process.env.GMAIL_USER}>`,
        to: "harpindersingh529@gmail.com", // where you want to receive
        subject: `New Contact Form Submission from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\nMessage:\n${message}`
      });

      // 3. Success
      return res.status(200).json({ success: true, message: "Email sent" });
    } catch (error) {
      console.error(error);
      return res.status(500).json({ success: false, message: "Email failed" });
    }
  } else {
    // Not a POST request
    res.status(405).json({ success: false, message: "Method not allowed" });
  }
}