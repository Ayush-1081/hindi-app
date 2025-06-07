import streamlit as st
from google import genai
from google.genai import types
import pathlib
import httpx
from tempfile import NamedTemporaryFile

# --- HARDCODE YOUR API KEY HERE ---
GOOGLE_API_KEY = "AIzaSyAYlgueM3h9Q6z9zJ308keNIj_QzK6e1hY"  # 🔴 Replace this with your real key

# --- Initialize Gemini client ---
client = genai.Client(api_key=GOOGLE_API_KEY)

st.title("📚 Hindi Book Chat with Gemini 2.0 Flash")

# --- Upload PDF or provide URL ---
uploaded_file = st.file_uploader("अपना हिंदी PDF बुक अपलोड करें", type=["pdf"])
pdf_url = st.text_input("या PDF का लिंक डालें:")

file_path = None
if uploaded_file is not None:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        file_path = pathlib.Path(tmp.name)
elif pdf_url:
    try:
        file_path = pathlib.Path("downloaded_book.pdf")
        file_path.write_bytes(httpx.get(pdf_url).content)
    except Exception as e:
        st.error(f"PDF डाउनलोड नहीं हो सका: {e}")
        st.stop()

if file_path is not None:
    st.success(f"📄 PDF तैयार: {file_path.name}")

    if 'uploaded_file_id' not in st.session_state:
        with st.spinner("Gemini को PDF भेजा जा रहा है..."):
            uploaded_file_obj = client.files.upload(file=file_path)
            st.session_state.uploaded_file_id = uploaded_file_obj
            st.success("✅ PDF सफलतापूर्वक अपलोड हुआ!")

    # --- Set creativity level ---
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.5, 0.05)

    # --- User prompt in Hindi ---
    prompt = st.text_area("प्रश्न पूछें (हिंदी में)", height=100)

    if st.button("उत्तर प्राप्त करें") and prompt.strip():
        config = types.GenerateContentConfig(
            temperature=temperature,
            top_k=40,
            top_p=1.0,
            max_output_tokens=2048
        )

        with st.spinner("उत्तर तैयार किया जा रहा है..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=config,
                contents=[st.session_state.uploaded_file_id, prompt]
            )

        st.markdown("### 📘 Gemini का उत्तर:")
        st.markdown(response.text)
else:
    st.info("कृपया पहले एक PDF अपलोड करें या लिंक डालें।")
