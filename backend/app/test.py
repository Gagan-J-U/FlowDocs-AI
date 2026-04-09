import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDyRTS2NZj4wKR6owkVH4g4MsMJRgdMXxQ")

for model in genai.list_models():
    print(model.name, model.supported_generation_methods)