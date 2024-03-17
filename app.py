import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key, openai_api_key
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)
genai.configure(api_key=google_gemini_api_key)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

st.set_page_config(layout = "wide")
st.title("Blogcraft")
st.subheader("Craft perfect blog using AI")

with st.sidebar:
    st.title("Blog details:")
    st.subheader("Enter blog details")

    blog_title = st.text_input("Title")

    keywords = st.text_input("Keywords (comma separated)")

    text_style = st.selectbox("Text style", ["Informative", "Persuasive", "Narrative", "Descriptive", "Conversational", "Creative"])

    language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Russian", "Japanese", "Chinese"])

    num_words = st.number_input("Number of words", min_value=200, max_value=1000, step=100)

    num_images = st.number_input("Number of images", min_value=0, max_value=10, step=1)

    prompt_parts = [
        f"Craft an all-encompassing and captivating blog post tailored to the provided {blog_title} and {keywords}. The post should span approximately {num_words} words, catering to an online readership. Emphasize originality, provide valuable insights, and sustain a coherent tone across the piece. The blog post should be written in {language} and should be optimized for search engines.  The post should be written in a {text_style} style, and should be free from any grammatical errors or plagiarism."
    ]

    

    submit_button = st.button("Generate blog")

if submit_button:

    response = model.generate_content(prompt_parts)

    img_response = client.images.generate(
        model="dall-e-3",
        prompt="a white siamese cat",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = img_response.data[0].url

    st.image(image_url, caption="Generated image")
    st.title("Your blog post:")
    st.write(response.text)