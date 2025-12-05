# =====================================================
# Project: Generative Abstract Poster (Step 4 – Style Presets, Streamlit Version)
# Author: HUANG SHIXIAN
# =====================================================

import streamlit as st
import random, math, os, colorsys
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Color helpers / palettes
# ------------------------------
def clamp01(x): return max(0.0, min(1.0, float(x)))

def hsv_to_rgb_tuple(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(clamp01(h), clamp01(s), clamp01(v))
    return (r, g, b)

def pastel_palette(k=6):
    hues = np.linspace(0, 1, k, endpoint=False)
    random.shuffle(hues)
    return [hsv_to_rgb_tuple(h, random.uniform(0.20, 0.45), random.uniform(0.85, 0.98)) for h in hues]

def vivid_palette(k=6):
    hues = np.linspace(0, 1, k, endpoint=False)
    random.shuffle(hues)
    return [hsv_to_rgb_tuple(h, random.uniform(0.80, 1.00), random.uniform(0.70, 0.95)) for h in hues]

def mono_palette(k=6, base_hue=0.58):
    return [hsv_to_rgb_tuple(base_hue, random.uniform(0.25, 0.85), random.uniform(0.55, 0.98)) for _ in range(k)]

# -----------------------------------------------
# Geometry: Wobbly blob
# -----------------------------------------------
def blob(center=(0.5, 0.5), r=0.3, points=220, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ------------------------------------------------
# Rendering function
# ------------------------------------------------
def _render(palette_fn, n_layers, wobble_range, radius_range,
            background=(0.98, 0.98, 0.97), title="Generative Poster – Step 4",
            subtitle="", seed=None, noise_touch=False):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    fig = plt.figure(figsize=(7, 10))
    ax = plt.gca()
    ax.axis('off')
    ax.set_facecolor(background)

    palette = palette_fn(k=7)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(*radius_range)
        wob = random.uniform(*wobble_range)

        if noise_touch:
            cx = clamp01(cx + np.random.normal(0, 0.06))
            cy = clamp01(cy + np.random.normal(0, 0.06))
            rr = max(0.05, rr + np.random.normal(0, 0.04))
            wob = max(0.01, wob + np.random.normal(0, 0.06))

        x, y = blob(center=(cx, cy), r=rr, wobble=wob)
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        if noise_touch:
            alpha = clamp01(np.random.normal(alpha, 0.15))
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    ax.text(0.05, 0.95, title, fontsize=18, weight='bold', transform=ax.transAxes)
    if subtitle:
        ax.text(0.05, 0.91, subtitle, fontsize=11, transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    return fig

# ----------------------------------------
# Public API: style-driven poster function
# ----------------------------------------
def generate_poster(style="Minimal", seed=None):
    style = style.strip().lower()

    if style == "minimal":
        return _render(pastel_palette, n_layers=5, wobble_range=(0.01, 0.06),
                       radius_range=(0.15, 0.35),
                       subtitle="Style: Minimal (pastel, low wobble, fewer layers)", seed=seed)

    if style == "vivid":
        return _render(vivid_palette, n_layers=16, wobble_range=(0.05, 0.20),
                       radius_range=(0.18, 0.50),
                       subtitle="Style: Vivid (strong colors, many layers)", seed=seed)

    if style == "noisetouch":
        return _render(lambda k: mono_palette(k=k, base_hue=0.58), n_layers=12,
                       wobble_range=(0.20, 0.45), radius_range=(0.12, 0.48),
                       subtitle="Style: NoiseTouch (randomness, high wobble)",
                       seed=seed, noise_touch=True)

    raise ValueError("Unknown style")

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎨 Generative Abstract Poster — Step 4 (Style Presets)")

style = st.selectbox("Choose a style preset:", ["Minimal", "Vivid", "NoiseTouch"])
seed = st.number_input("Random Seed", value=123, step=1)
if st.button("Generate Poster"):
    fig = generate_poster(style=style, seed=seed)
    st.pyplot(fig)
