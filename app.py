import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

st.set_page_config(page_title="Power 9 - Style Converter", layout="wide")
st.title("👑 Power 9 - Style Converter - Cloud Version")

# KEY FROM SECRETS - Safe, Not in Code
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash-image")
    st.success("✅ Connected to Gemini - Ready!")
except:
    st.warning("⚠️ Key not added yet in Streamlit Secrets. Add it after deploy.")
    model = None

# 1. REFERENCE
st.subheader("1. Our Reference Style - LOCKED")
ref_file = st.file_uploader("Upload Our Classroom Image", type=["png","jpg","jpeg"], key="ref")
if ref_file:
    st.image(Image.open(ref_file), width=300, caption="Our Style")

# 2. INPUT
st.subheader("2. Upload Any Image")
input_file = st.file_uploader("Upload Tree / River / Cloud / Flower", type=["png","jpg","jpeg"], key="input")
if input_file:
    st.image(Image.open(input_file), width=300, caption="Original")

object_name = st.text_input("What is this? Example: Tree, River, Cloud")

# 3. CONVERT
if st.button("🔥 CONVERT TO OUR STYLE"):
    if ref_file and input_file and object_name and model:
        with st.spinner("Converting... 10 sec... Please wait..."):
            ref_img = Image.open(ref_file)
            input_img = Image.open(input_file)
            prompt = f"""
            Take the second image of {object_name}. Keep object shape exactly same.
            Change ONLY style to match first reference image style:
            3D cute cartoon for kids, warm orange-yellow lighting, soft edges,
            big happy eyes if character, vertical 9:16 kids poster, same classroom background.
            NO text, NO watermark.
            """
            response = model.generate_content([prompt, ref_img, input_img])
            # Gemini returns image
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    out_img = Image.open(io.BytesIO(part.inline_data.data))
                    st.image(out_img, caption=f"Our Style {object_name} - DONE!")
                    buf = io.BytesIO()
                    out_img.save(buf, format="PNG")
                    st.download_button("⬇️ Download Our Style Image", buf.getvalue(), f"our-style-{object_name}.png", "image/png")
                    break
            else:
                st.error("AI did not return image. Try again.")
    else:
        st.error("Boss, Upload Both Images + Write Name + Add Key in Secrets!")