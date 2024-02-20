import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from streamlit_carousel import carousel

genai.configure(api_key="AIzaSyA8TesjTLzuqovktzzhu4Vvdo3F0Tbcpvc")
client = OpenAI(api_key="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")


singel_image=dict(
        title="",
        text="",
        interval = None,
        img="",
    )


# Set up the model
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


st.set_page_config(layout="wide")
st.title("🤖 AI Blog Buddy: Crafting Compelling Content with Ease 🚀")

st.subheader("Now you can craft perfact blogs with the help of AI Blog Buddy is your New AI Blog Companion")

with st.sidebar:
    st.title("Input your Blog Details")
    st.subheader("Enter details of the Blog you want to generate")

    #Blog Title
    blog_title = st.text_input("Blog Title")

    KeyWords = st.text_area("Keywords (Comma-separated)")

    num_words = st.slider("Number of Words",min_value=300,max_value=1500,step=250)

    num_image = st.number_input("Number of Images",min_value=1,max_value=5,step=1)

    prompt_parts = [
  f"Generate a comprehensive engaging blog post relevant to the give {blog_title} and {KeyWords}. The Blog should be approximately {num_words} words in length sutiable for an online audience. Ensure the content is original, informative and maintains a consistent tone throughout.",
]

    Submit_button = st.button("Generate blog")


if Submit_button:
    

    response = model.generate_content(prompt_parts)
    images =[]
    images_gallery=[]

    for i in range (num_image):

        image_response = client.images.generate(
        model="dall-e-2",
        prompt=f"Generate a Blog Post image on the title: {blog_title}",
        size="1024x1024",
        quality="standard",
        n=1)
        new_image = singel_image.copy()
        new_image['title']= f"Image{i+1}"
        new_image['text']= f"{blog_title}"
        new_image['img']= image_response.data[0].url
        images_gallery.append(new_image)
    
    st.title("Your Blog Images are here")
    carousel(items=images_gallery, width=1)

    st.title("Your Blog Post is Here")
    st.write(response.text)
