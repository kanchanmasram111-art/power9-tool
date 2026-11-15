import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io

st.set_page_config(page_title="Power 9 - Classroom Style Converter", layout="centered")
st.title("Power 9 - Classroom Style Converter")
st.success("✅ No Limit! Convert Unlimited Images - No Google, No API Key Needed!")

style = st.selectbox("Choose Style - 9 Styles:", [
    "1. Pencil Sketch",
    "2. Watercolor Effect",
    "3. Cartoon / Poster",
    "4. Black & White Classic",
    "5. Sepia Vintage",
    "6. Bright Pop Art",
    "7. Soft Blur Dream",
    "8. High Contrast Bold",
    "9. Warm Sunset"
])

uploaded = st.file_uploader("Upload Your Image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Original Image", use_column_width=True)
    if st.button("CONVERT NOW 🚀"):
        if "Pencil" in style:
            out = ImageOps.grayscale(img)
            out = ImageOps.invert(out)
            out = out.filter(ImageFilter.GaussianBlur(2))
            out = ImageOps.invert(out)
            out = ImageEnhance.Contrast(out).enhance(1.5)
            out = out.convert("RGB")
        elif "Watercolor" in style:
            out = img.filter(ImageFilter.SMOOTH_MORE)
            out = ImageEnhance.Color(out).enhance(1.4)
            out = ImageEnhance.Brightness(out).enhance(1.1)
        elif "Cartoon" in style:
            out = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            out = ImageEnhance.Color(out).enhance(1.8)
            out = ImageEnhance.Contrast(out).enhance(1.3)
        elif "Black" in style:
            out = ImageOps.grayscale(img).convert("RGB")
            out = ImageEnhance.Contrast(out).enhance(1.2)
        elif "Sepia" in style:
            gray = ImageOps.grayscale(img)
            out = ImageOps.colorize(gray, black="#2b1a00", white="#ffE8b0")
        elif "Bright" in style:
            out = ImageEnhance.Color(img).enhance(2.0)
            out = ImageEnhance.Brightness(out).enhance(1.2)
            out = ImageEnhance.Contrast(out).enhance(1.2)
        elif "Soft" in style:
            out = img.filter(ImageFilter.GaussianBlur(1.5))
            out = ImageEnhance.Brightness(out).enhance(1.1)
        elif "High Contrast" in style:
            out = ImageEnhance.Contrast(img).enhance(2.0)
            out = ImageEnhance.Color(out).enhance(1.2)
        else:
            out = ImageEnhance.Color(img).enhance(1.3)
            out = ImageEnhance.Brightness(out).enhance(1.05)
            r,g,b = out.split()
            r = r.point(lambda i: min(255, int(i*1.15)))
            out = Image.merge("RGB", (r,g,b))
        st.image(out, caption=f"Converted - {style}", use_column_width=True)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button("Download Converted Image 📥", buf.getvalue(), file_name="power9_converted.png", mime="image/png")
        st.balloons()
        st.success("Done! Convert another image - Unlimited!")
