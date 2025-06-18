# Advanced QR Code Scanner and Generator 🧠🔍

This Python application uses OpenCV and Pyzbar to scan QR codes from both live webcam feed and images. It automatically detects the type of data encoded in the QR and performs relevant actions, such as opening URLs, copying text, parsing WiFi credentials, and more. It also allows QR code generation.

## 💡 Features

- 📷 **Live QR Code Scanning** via webcam
- 🖼️ **Image-Based QR Scanning**
- 🧾 **QR Data Auto-Detection**:
  - URLs (auto-open in browser)
  - WiFi config (prompts to connect)
  - Email addresses
  - SMS commands
  - Phone numbers
  - vCards
  - Text
- 🔗 **Auto Clipboard Copying**
- 🌐 **Auto URL Launching**
- 📶 **WiFi QR Parsing (Display info + suggest connection)**
- 📦 **QR Code Generation with Save Dialog**
- 🧠 **Naive Bayes Model (Optional)** for classifying QR type automatically

---

## 🚀 Getting Started

### 🔧 Prerequisites

Install required libraries:

```bash
pip install opencv-python pyzbar numpy qrcode pyperclip
