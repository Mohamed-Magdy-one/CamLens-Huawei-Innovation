# 👁️ CamLens: Privacy-First Optical Vision Correction Engine

**Team:** Apex_Coders  
**Competition:** Huawei ICT Innovation Track 2026

---

## 📌 Project Overview
CamLens is a software-based vision correction system that replaces expensive, privacy-invasive hardware eye-tracking cameras with a **1D Lenticular Sheet** and a real-time **NumPy Vectorized Interlacing Engine**.

By dynamically restructuring on-screen pixels, CamLens compensates for refractive errors (like myopia), allowing users to read text, write code, and view dashboards clearly—**without wearing prescription glasses** and **without camera surveillance**.

---

## 🚀 Core Features
1. **Privacy-First Design:** Zero cameras used. The system relies entirely on computational optics and manual digital calibration.
2. **Real-Time Vectorization:** Built using pure `NumPy` array manipulations and `OpenCV` affine transformations, ensuring **zero latency** and minimal CPU overhead.
3. **Hardware Calibration Mode (F11):** A pixel-perfect fullscreen mode that aligns the software's interlacing pitch with the physical 1D lenticular sheet down to the micrometer.
4. **Digital Eye-Shift (A/D Keys):** A software alternative to eye-tracking. Users can dynamically shift the optical "sweet spot" to match their viewing angle using simple keyboard inputs.
5. **Interactive UI:** Built with `customtkinter`, featuring dynamic in-memory sample generators for text documents, code editors, and UI dashboards.

---

## 🛠️ System Architecture
* **Frontend:** `customtkinter` (Dark-mode responsive UI)
* **Image Processing Engine:** `OpenCV` (cv2)
* **Algorithm Acceleration:** `NumPy` (Vectorized array math)
* **Optical Hardware:** 1D Lenticular Plastic Sheet

---

## ⚙️ Quick Start (Installation & Execution)

### 1. Clone the Repository
```bash
git clone https://github.com/Mohamed-Magdy-one/CamLens-Huawei-Innovation.git
cd CamLens-Huawei-Innovation