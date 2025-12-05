# 🎨 Generative Abstract Poster — Step 4 (Style Presets)

This Streamlit app showcases a **style-based generative art system** that produces posters with consistent visual identities using pre-defined presets.

---

## 💡 Concept
Each style preset defines a specific **visual language**:
- 🎨 **Minimal** — soft pastel tones, fewer layers, calm mood  
- 🔥 **Vivid** — bright, high-saturation colors, dynamic layout  
- 🌪 **NoiseTouch** — high randomness, rough texture, expressive feel  

The goal is to demonstrate how algorithmic design parameters can produce different emotional aesthetics while maintaining generative consistency.

---

## 🧠 How It Works
- Random geometry ("blobs") are generated using sine–cosine noise.  
- Each preset defines its **palette**, **layer count**, and **noise level**.  
- The same random seed will always reproduce the same artwork.

---

## ⚙️ Installation & Run
```bash
git clone https://github.com/yourusername/generative-poster-step4.git
cd generative-poster-step4
pip install -r requirements.txt
streamlit run app.py
