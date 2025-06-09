import streamlit as st
from google import genai
from google.genai import types
import pathlib

# --- HARDCODE YOUR API KEY HERE ---
GOOGLE_API_KEY = "AIzaSyAYlgueM3h9Q6z9zJ308keNIj_QzK6e1hY"

# --- Initialize Gemini client ---
client = genai.Client(api_key=GOOGLE_API_KEY)

st.title("📚 Hindi Book Chat with Gemini 2.0 Flash")

# --- Path to all chapter PDFs ---
chapter_paths = {
    "Chapter 1: उड़ चल, हारिल": "chapters/ch1.pdf",
    "Chapter 2: डिनर": "chapters/ch2.pdf",
    "Chapter 3: नाम चर्चा": "chapters/ch3.pdf",
    "Chapter 4: मेरी स्मृति": "chapters/ch4.pdf",
    "Chapter 5: भाषा का प्रश्न": "chapters/ch5.pdf",
    "Chapter 6: दो संस्मरण": "chapters/ch6.pdf",
    "Chapter 7: हिम": "chapters/ch7.pdf",
    "Chapter 8: प्रण": "chapters/ch8.pdf",
    "Chapter 9: ब्रजवासी": "chapters/ch9.pdf",
    "Chapter 10: गुरुदेव का घर": "chapters/ch10.pdf",
    "Chapter 11: दो लघुकथाएँ": "chapters/ch11.pdf",
}

# --- Select chapter with full name display ---
selected_chapter = st.selectbox("अध्याय चुनें (Select a Chapter)", list(chapter_paths.keys()))
chapter_file_path = pathlib.Path(chapter_paths[selected_chapter])

if chapter_file_path.exists():
    st.success(f"📄 चयनित अध्याय: {selected_chapter}")

    # Upload to Gemini if new chapter or not uploaded before
    if 'uploaded_file_id' not in st.session_state or st.session_state.get("current_chapter") != selected_chapter:
        with st.spinner(f"📤 {selected_chapter} को Gemini को भेजा जा रहा है..."):
            uploaded_file_obj = client.files.upload(file=chapter_file_path)
            st.session_state.uploaded_file_id = uploaded_file_obj
            st.session_state.current_chapter = selected_chapter
            st.success("✅ अध्याय सफलतापूर्वक अपलोड हुआ!")

    # --- Creativity level ---
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.5, 0.05)

    # --- Question input ---
    prompt = st.text_area("प्रश्न पूछें (हिंदी में)", height=100)

    if st.button("उत्तर प्राप्त करें") and prompt.strip():
        config = types.GenerateContentConfig(
            temperature=temperature,
            top_k=40,
            top_p=1.0,
            max_output_tokens=2048
        )

        with st.spinner("🧠 Gemini उत्तर तैयार कर रहा है..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=config,
                contents=[st.session_state.uploaded_file_id, prompt]
            )

        st.markdown("### 📘 Gemini का उत्तर:")
        st.markdown(response.text)
else:
    st.error("❌ चयनित अध्याय PDF फ़ाइल मौजूद नहीं है। कृपया paths जांचें।")
