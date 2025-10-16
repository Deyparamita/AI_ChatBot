import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from gemini_utility import (load_gemini_flash_model, gemini_flash_vision, embedding_model_response, gemini_flash_response)

# have to specify the directory for imports to work (for accessing files uploaded in streamlit)
working_directory = os.path.dirname(os.path.abspath(__file__))

# print(working_directory)

# Setting the page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu("Gemini AI",
                           ["ChatBot",
                           "Image Captioning",
                           "Embed text",
                           "Ask me anything"],
                           menu_icon = 'robot', icons=['chat-dots-fill', 'image-fill','textarea-t', 'patch-question-fill'],
                           default_index=0 # will show the firstpage by default
                           )
    

# function to translate role between gemini and streamlit terminology

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == "ChatBot":
    model = load_gemini_flash_model()
    # initialize chat session in streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title
    st.title("🤖 ChatBot")

    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user's message
    user_prompt = st.chat_input("Ask Gemini Pro...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # display gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


if selected == "Image Captioning":
    st.title("🖼️ Image Captioning")
    uploaded_image = st.file_uploader(
        "Upload an image.....",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        if st.button("Generate caption"):
            image = Image.open(uploaded_image)
            # col1, col2 = st.columns(2)
            # with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

            default_prompt = "Generate a caption for this image"
            caption = gemini_flash_vision(default_prompt, image)

            # with col2:
            st.info(caption)
    else:
        st.warning("Please upload an image before generating a caption.")

        
# text embedding page

if selected == "Embed text":
    st.title("🔤 Embed Text")
        
    # input text box
    input_text = st.text_area(label="text", placeholder="Enter the text to get the embeddings")

    if st.button("Get Embeddings"):
        try:
            response = embedding_model_response(input_text)
            st.markdown(response)
        except Exception as e:

            # Convert the exception to string for easier checking
            error_message = str(e)

            # Check if the error is about quota exceeded
            if "Quota exceeded" in error_message:
                st.error("⚠️ Can't generate embeddings — this API model doesn't provide free credits for embedding text. Please enable billing or use another free model.")
            else:
                st.error(f"❌ An unexpected error occurred:\n\n{error_message}")


if selected == "Ask me anything":
    st.title("❔ Ask me anything")
    user_question = st.text_area(label="text",placeholder="Ask me anything")
    if st.button("Get answer"):
        if user_question:
            try:
                response = gemini_flash_response(user_question)
                st.success(response)
                
            except Exception as e:
                st.error(f"Error getting answer: {e}")
