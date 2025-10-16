import os
from dotenv import load_dotenv
import google.generativeai as genai

# accessing files uploaded in streamlit
working_directory = os.path.dirname(os.path.abspath(__file__))

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# configuring google.generativeai with the API key
genai.configure(api_key=api_key)

# load gemini model
# def load_model(model_name):
#     try:
#         model = genai.Model(model_name)
#         return model
#     except Exception as e:
#         print(f"Error loading model {model_name}: {e}")
#         return None

# List available models and their capabilities
# for model in genai.list_models():
#     print(f"Model name: {model.name}")
#     print(f"Supported methods: {model.supported_generation_methods}")
#     print("-" * 40)

def load_gemini_flash_model():
    gemini_flash_model = genai.GenerativeModel("gemini-2.0-flash")
    return gemini_flash_model

# Function for image captioning
def gemini_flash_vision(prompt, image):
    gemini_flash_vision_model = genai.GenerativeModel("gemini-2.5-flash")
    response = gemini_flash_vision_model.generate_content((prompt, image))
    result = response.text
    return result

# Function to get embedding for text
def embedding_model_response(input_text):
    embedding_model = 'models/embedding-001'
    embedding = genai.embed_content(model=embedding_model, content=input_text, task_type="retrieval_document")

    embedding_list = embedding['embedding']
    return embedding_list

# To see the output
# output = embedding_model_response("What is the meaning of life?")
# print(output)

# Function to get a response from gemini-flash
def gemini_flash_response(user_prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(user_prompt)
    result = response.text
    return result

# output = gemini_flash_response("What is ML Ops?")
# print(output)