import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
import os
import json

st.set_page_config(page_title="Zero Waste Kitchen Assistant", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Rubik:wght@400;500;700&display=swap');

:root {
  --bg-1: #0c0f1a;
  --bg-2: #1b1430;
  --bg-3: #241b3f;
  --accent: #ff7ab6;
  --accent-2: #fbbf24;
  --accent-3: #60a5fa;
  --accent-4: #34d399;
  --ink: #f8f7ff;
  --muted: #cbd5f5;
  --card: #17152a;
  --card-border: #2a2746;
}

html, body, [class*="stApp"] {
  background:
    radial-gradient(600px 400px at -5% -10%, #3a2f7a 0%, transparent 60%),
    radial-gradient(600px 400px at 105% 10%, #2f7a60 0%, transparent 55%),
    linear-gradient(180deg, var(--bg-2), var(--bg-1));
  color: var(--ink);
  font-family: "Rubik", system-ui, sans-serif;
}

.block-container {
  padding-top: 1.5rem;
  padding-bottom: 3rem;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
  align-items: center;
  background:
    linear-gradient(135deg, rgba(255,122,182,0.18), rgba(96,165,250,0.16)),
    var(--card);
  border: 2px dashed rgba(255,255,255,0.18);
  border-radius: 26px;
  padding: 28px 32px;
  margin-bottom: 20px;
  box-shadow: 0 22px 70px rgba(10, 20, 45, 0.45);
  animation: fadeIn 600ms ease-out;
  position: relative;
  overflow: hidden;
}

.hero h1 {
  font-family: "Baloo 2", cursive;
  font-size: 2.8rem;
  margin: 0 0 6px 0;
  letter-spacing: 0.2px;
}

.hero .kicker {
  color: var(--accent-2);
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  font-size: 0.7rem;
}

.hero p {
  color: var(--muted);
  margin: 0;
}

.hero-badge {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-3) 100%);
  color: #0b1020;
  padding: 10px 16px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 0.95rem;
  box-shadow: 0 14px 34px rgba(255, 122, 182, 0.35);
  transform: rotate(-2deg);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.emoji-badges {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.emoji-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 999px;
  padding: 6px 12px;
  font-weight: 600;
  font-size: 0.9rem;
  box-shadow: 0 10px 24px rgba(0,0,0,0.25);
  backdrop-filter: blur(6px);
}

.emoji-badge .emoji {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #0b1020;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.2);
  font-size: 1rem;
}

.card {
  background:
    linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.00)),
    var(--card);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 22px;
  padding: 20px;
  box-shadow: 0 18px 46px rgba(0,0,0,0.35);
  animation: riseIn 700ms ease-out;
}

.card h3 {
  margin: 0 0 12px 0;
  font-weight: 600;
}

.result-pill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 122, 182, 0.25);
  color: var(--accent);
  padding: 10px 14px;
  border-radius: 14px;
  border: 1px solid rgba(255, 122, 182, 0.45);
  font-weight: 700;
}

.muted {
  color: var(--muted);
}

.table-wrap {
  margin-top: 18px;
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 16px;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-top: 12px;
}

.metric {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 12px 14px;
}

.metric .label {
  color: var(--muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

.metric .value {
  font-size: 1.2rem;
  font-weight: 700;
}

.stButton > button {
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.28);
  background: linear-gradient(135deg, rgba(255,122,182,0.25), rgba(96,165,250,0.25));
  color: var(--ink);
  font-weight: 700;
  padding: 0.55rem 1rem;
  box-shadow: 0 10px 24px rgba(0,0,0,0.25);
  transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
}

.stButton > button:hover {
  transform: translateY(-1px);
  border-color: rgba(255,255,255,0.45);
  box-shadow: 0 14px 30px rgba(0,0,0,0.3);
}

.stButton > button:active {
  transform: translateY(0);
  box-shadow: 0 8px 18px rgba(0,0,0,0.22);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes riseIn {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Zero Waste Kitchen")


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "models/food_model.h5",
        custom_objects={
            "preprocess_input": tf.keras.applications.mobilenet_v2.preprocess_input
        },
    )


@st.cache_data
def load_class_names():
    with open("models/class_names.json") as f:
        return json.load(f)


@st.cache_data
def load_shelf_life():
    if os.path.exists("shelf_life.csv"):
        return pd.read_csv("shelf_life.csv")
    return pd.DataFrame(columns=["item", "days"])


# Load model (cached)
model = load_model()

# Load class names (match training order)
class_names = load_class_names()

# Upload image
col_left, col_right = st.columns([1.05, 1], gap="large")
with col_left:
    st.markdown(
        """
<div class="card">
  <h3>Upload a food image</h3>
  <p class="muted">Drag & drop or browse. JPG, PNG, JPEG supported.</p>
</div>
""",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

with col_right:
    st.markdown(
        """
<div class="card">
  <h3>Preview & Results</h3>
  <p class="muted">See the prediction, confidence, and shelf-life estimate.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB").resize((128, 128))
        st.image(image, caption="Uploaded Image", width=160)

        # Model already includes preprocess_input as a Lambda layer
        img_array = np.array(image, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array, verbose=0)
        predicted_index = int(np.argmax(prediction))
        predicted_item = class_names[predicted_index]

        st.markdown(f"<div class='result-pill'>Predicted: {predicted_item}</div>", unsafe_allow_html=True)

        top_k = 3
        probs = prediction[0]
        top_indices = np.argsort(probs)[-top_k:][::-1]
        top_labels = [class_names[i] for i in top_indices]
        top_scores = [float(probs[i]) for i in top_indices]

        st.markdown(
            f"""
<div class="metric-grid">
  <div class="metric"><div class="label">Top 1</div><div class="value">{top_labels[0]} · {top_scores[0]:.1%}</div></div>
  <div class="metric"><div class="label">Top 2</div><div class="value">{top_labels[1]} · {top_scores[1]:.1%}</div></div>
  <div class="metric"><div class="label">Top 3</div><div class="value">{top_labels[2]} · {top_scores[2]:.1%}</div></div>
</div>
""",
            unsafe_allow_html=True,
        )

        # Read-only shelf-life display
        shelf_df = load_shelf_life()
        expiry_days = None
        row = shelf_df[shelf_df["item"] == predicted_item]
        if not row.empty:
            expiry_days = int(row["days"].values[0])

        if expiry_days is not None:
            st.info(f"Estimated Shelf Life: {expiry_days} days")
        else:
            st.warning("Shelf-life not found for this item.")
    else:
        st.markdown("<p class='muted'>Upload an image to see results here.</p>", unsafe_allow_html=True)

# Full shelf-life table
st.markdown("<div class='table-wrap'>", unsafe_allow_html=True)
st.subheader("Shelf-Life Table")
shelf_df = load_shelf_life()
if not shelf_df.empty:
    st.dataframe(shelf_df, use_container_width=True)
else:
    st.warning("shelf_life.csv not found.")
st.markdown("</div>", unsafe_allow_html=True)
