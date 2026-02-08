# 🕵️‍♂️ SHERLOCK: Deepfake Detection System

<div align="center">

![Sherlock Banner](https://img.shields.io/badge/SHERLOCK-AI_CYBERSECURITY-00ff9d?style=for-the-badge&logo=openai&logoColor=black)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-black?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=flat-square&logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](./LICENSE)

*Advanced Multi-Modal Deepfake Detection secured by Edge Computing.*

[Report Bug](https://github.com/obsTR/Sherlock/issues) · [Request Feature](https://github.com/obsTR/Sherlock/issues)

</div>

---

## ⚡ Overview

**Sherlock** is a state-of-the-art cybersecurity platform designed to detect synthetic media manipulation. By combining **Visual Artifact Analysis** (EfficientNet) with **Audio Spectral Analysis** (MFCC/CNN), Sherlock provides a robust defense against deepfakes.

The system is built with a **Security-First** architecture, featuring an Edge Gateway that sanitizes and validates requests before they reach the core inference engine.

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| **👁️ Multi-Modal Detection** | Analyzes both **Video** (visual artifacts) and **Audio** (voice synthesis) concurrently. |
| **🛡️ Edge Security** | Protected by a **Cloudflare Worker** gateway that handles Auth, Rate Limiting, and Validation. |
| **⚡ Real-Time Inference** | Optimized PyTorch pipeline delivering sub-second frame analysis. |
| **📊 Cyber Dashboard** | Modern, dark-mode **React/Next.js** interface for visualization and reporting. |
| **🔍 Explainable AI** | Provides confidence scores for both visual and audio components. |

## 🏗️ Architecture

<img width="3961" height="3080" alt="sherlock_flow" src="https://github.com/user-attachments/assets/87f30ea0-ba80-45ed-9196-193b2bf586a3" />


## 🛠️ Technology Stack

### **Frontend (Command Center)**
*   **Framework**: Next.js 14 (App Router)
*   **Styling**: Tailwind CSS, Framer Motion
*   **Theme**: Cyberpunk / Dark Mode

### **Edge (Security Layer)**
*   **Platform**: Cloudflare Workers
*   **Language**: TypeScript
*   **Functions**: JWT Verification, Rate Limiting

### **Backend (The Brain)**
*   **Framework**: FastAPI
*   **ML Core**: PyTorch, TorchVision, Torchaudio
*   **Processing**: OpenCV, Librosa, NumPy

---

## 🏁 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   FFmpeg (Installed and in system PATH)

### 1. 🧠 Start the Backend (ML Engine)
```bash
cd backend
pip install -r requirements.txt
python app/main_api.py
```
> Server will start on `http://localhost:8000`

### 2. 🛡️ Start the Edge Gateway
```bash
cd edge
npm install
npx wrangler dev
```
> Gateway will start on `http://localhost:8787`

### 3. 💻 Start the Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
> UI will be available at `http://localhost:3000`

---

## 🧪 Usage & Testing

You can test the full pipeline using the included integration script or the Web UI.

**Option A: Web UI**
1.  Open `http://localhost:3000`.
2.  Drag & Drop a video file (MP4/AVI).
3.  Click **ANALYZE MEDIA**.

**Option B: CLI Test**
```bash
# Generates a dummy video and sends it through the pipeline
python integration_test.py
```

## 📂 Project Structure

```text
Sherlock/
├── 📂 backend/             # Python ML Engine
│   ├── 📂 app/             # Application Code
│   │   ├── 📂 core/        # Detection Logic
│   │   ├── 📂 services/    # Model & Processor Services
│   │   └── 📂 api/         # FastAPI Endpoints
│   └── main_api.py         # Entry Point
│
├── 📂 edge/                # Cloudflare Worker
│   ├── 📂 src/             # Worker Logic (Auth/Proxy)
│   └── wrangler.toml       # Edge Config
│
└── 📂 frontend/            # Next.js Dashboard
    ├── 📂 components/      # React UI Components
    └── 📂 app/             # Pages & Layouts
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

**Built for the future of Cybersecurity.**
<br>
<sub>Developed with ❤️ by Onur Kolay</sub>

</div>
