import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input as preprocess_input_resnet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import decode_predictions as decode_predictions_resnet
import google.generativeai as genai
import geocoder
import re

# ✅ Set Page Config
st.set_page_config(
    page_title="NutriPlanAI",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Apply Custom Styles
st.markdown("""
    <style>
        /* 🌈 Soft Gradient Background */
        .stApp {
            background: linear-gradient(to right, #8ddaf0, #f8f6ff, #5fe3f5);
            color: #333;
            font-family: 'Poppins', sans-serif;
        }
        
        /* 📦 Container Styling */
        .block-container {
            max-width: 900px;
            margin: auto;
            padding: 2rem;
        }

        .stSucc {
            background-color: #a0fad6;
            color:#333;
            padding: 15px;
            font-size:18px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }

        .stWarn {
            background-color: #f0f5b3;
            color:#333;
            padding: 15px;
            font-size:18px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
        }


        /* ✨ Glassmorphism Cards */
        .stCard {
            background: #c3eefa;
            color:white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            transition: 0.3s ease;
        }

        .stCard:hover {
            transform: scale(1.03);
            box-shadow: 0px 6px 20px #8ddaf0;
        }

        /* 🎨 Buttons - Soft Pastel Effect */
        .stButton button {
            background: linear-gradient(45deg, #ff9a9e, #fad0c4) !important;
            color: white !important;
            border-radius: 10px;
            font-size: 18px;
            padding: 12px 24px;
            border: none;
            box-shadow: 0px 4px 10px rgba(255, 160, 160, 0.5);
            transition: 0.3s ease;
        }

        .stButton button:hover {
            background: linear-gradient(45deg, #ff758c, #ff7eb3) !important;
            transform: scale(1.05);
            box-shadow: 0px 6px 15px rgba(255, 120, 150, 0.6);
        }

        /* 📌 Sidebar - Soft Blurry Card */
      /* 🌈 Sidebar Background - Soft Gradient */
        .css-1d391kg {
            background: white;
            color: white;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(200, 200, 200, 0.3);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        }

        /* 🎯 Sidebar Title Styling */
        .css-1v0mbdj {
            color: white !important;
            font-size: 22px !important;
            font-weight: bold !important;
            text-align: center !important;
        }

        /* 🔘 Sidebar Radio Buttons - Beautiful Custom Look */
        .stRadio label {
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            color: black;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 10px;
            font-weight: 500;
            box-shadow: 0px 2px 8px rgba(255, 150, 150, 0.3);
            transition: all 0.3s ease;
        }
        .stAppHeader{
        background:#f0f4fa;
        padding-bottom: 15px;

        }

        /* 🖱️ Hover Effect for Sidebar Buttons */
        .stRadio label:hover {
            background: #5fe3f5;
            transform: scale(1.05);
            box-shadow: 0px 4px 12px rgba(255, 100, 100, 0.4);
        }


        /* 🔘 Active Selection Highlight */
        .stRadio div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
            background: #b3e3fc !important;
            color: black !important;
            font-weight: bold !important;
            transform: scale(1.08);
            box-shadow: 0px 5px 15px rgba(255, 80, 120, 0.5);
        }
        /* 🔤 Input Fields with Soft Shadows */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            border-radius: 10px !important;
            padding: 12px !important;
            font-size: 16px !important;
            background: rgba(255, 255, 255, 0.9);
            color: black;
            border: 1px solid rgba(200, 200, 200, 0.5);
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            transition: 0.3s ease;
        }

        /* 📸 Image Styling */
        .stImage img {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
        }

        /* 🔽 Dropdown Menu Styling */
        .stSelectbox select {
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            color: #444;
        }

        /* ⚡ Footer - Elegant Soft Blur */
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 15px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.1);
        }
        .stTextInput label,.stNumberInput label{
        color : black;
        font-size: 40px;
        }
        /* 📌 Styling for st.expander */
        .stExpander {
            font-size: 22px !important; /* Increase font size */
            color: black !important; /* Change text color to black */
            font-weight: bold !important;
        }
        .stTxt{
        color:black
        }

    </style>
""", unsafe_allow_html=True)



# ✅ Title & Description
# st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.title("🍴 NutriPlanAI - AI Meal Planner")
st.subheader("🧠 Smart Meal Planning & Calorie Estimation")
# st.markdown("</div>", unsafe_allow_html=True)
genai.configure(api_key="AIzaSyA2GOwEVa2Q62mreWYgteYvXOdYGd1fdzc")  # Replace with your actual Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")
# st.set_page_config(page_title="Smart Diet Recommender", layout="centered")

st.divider()

# ✅ Sidebar for Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("", ("🏠 Home", "🔍 Find Calories in Meal", "🥗 Find Your Diet Plan","📃Plan Your Diet-chart"))

def resize_image(url, width, height):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, allow_redirects=True)

    if response.status_code == 200 and "image" in response.headers["content-type"]:
        img = Image.open(BytesIO(response.content))
        img = img.resize((width, height))  # Resize to fixed size
        return img
    else:
        st.warning("⚠ Unable to load image from URL: " + url)
        return None  

# ✅ Home Page
if "calories" not in st.session_state:
    st.session_state.calories = 0
if "predicted_cnt" not in st.session_state:
    st.session_state.predicted_cnt = 0
if option == "🏠 Home":
    # st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.write(
        "Welcome to **NutriPlanAI**, your personal AI-powered nutrition assistant. "
        "Upload your meal image to find calorie estimates, or get a personalized diet plan!"
    )
    # st.markdown("</div>", unsafe_allow_html=True)

# ✅ Find Calories in Meal Page
elif option == "🔍 Find Calories in Meal":
    # st.markdown('<div class="stCard">', unsafe_allow_html=True)
    
    # st.markdown("</div>", unsafe_allow_html=True)

    # 🔷 User Details Section
    with st.expander("📝 Enter Your Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
            gender = st.radio("Gender", ("Male", "Female", "Other"))
        with col2:
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
 
    # ✅ Function to Calculate Daily Calorie Intake
    def calculate_calories(age, weight, height, gender, activity_level):
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif gender == "Female":
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr = (10 * weight + 6.25 * height - 5 * age)  # Default neutral calculation

        activity_multipliers = {
            "Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725
        }
        return round(bmr * activity_multipliers[activity_level])

    if age and weight and height and activity_level and gender and name:
        daily_calories = calculate_calories(age, weight, height, gender, activity_level)
        st.success(f"🔥 Based on your details, your daily required calorie intake is **{daily_calories} kcal**.")
        st.session_state.calories = daily_calories 

    # 🔷 Meal Image Upload Section
    st.subheader("📸 Upload Your Meal Image")
    uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

    qty = st.number_input("Quantity", min_value=1, max_value=120, step=1)
    
    if uploaded_image:
        
        st.image(uploaded_image, caption="Uploaded Meal Image", use_container_width =True)

        calories_dict = {
    # Fast Food
    'pizza': 285, 'burger': 354, 'salad': 120, 'hotdog': 150, 'fries': 222, 

    # Fruits
    'banana': 115, 'lemon': 40, 'bell_pepper': 75, 'apple': 95, 'orange': 62, 'grapes': 69, 'watermelon': 30, 
    'strawberry': 32, 'blueberry': 57, 'pineapple': 50, 'mango': 99, 'kiwi': 42, 'pomegranate': 83, 'peach': 59, 
    'plum': 46, 'pear': 101, 'cherry': 63, 'fig': 74, 'apricot': 48, 'coconut': 354, 'blackberry': 43, 'raspberry': 52, 
    'guava': 68, 'papaya': 43, 'cranberry': 46, 'dragonfruit': 60, 'lychee': 66, 'jackfruit': 95, 'dates': 282,

    # Vegetables
    'carrot': 41, 'broccoli': 55, 'spinach': 23, 'potato': 77, 'sweet_potato': 86, 'cabbage': 25, 'lettuce': 15, 
    'cucumber': 16, 'tomato': 22, 'onion': 40, 'garlic': 149, 'ginger': 80, 'beetroot': 43, 'cauliflower': 25, 
    'zucchini': 17, 'brussels_sprout': 43, 'pumpkin': 26, 'radish': 16, 'asparagus': 20, 'okra': 33, 'artichoke': 47, 
    'mushroom': 22, 'avocado': 240, 'corn': 96, 'celery': 14, 'kale': 33, 'bok_choy': 13, 'turnip': 28, 'parsnip': 75, 
    'swiss_chard': 19, 'arugula': 25, 'seaweed': 45, 'butternut_squash': 45, 'spaghetti_squash': 42,

    # Nuts & Legumes
    'almond': 579, 'walnut': 654, 'cashew': 553, 'peanut': 567, 'hazelnut': 628, 'pistachio': 562, 'chickpeas': 164, 
    'lentils': 116, 'kidney_beans': 127, 'black_beans': 132, 'soybeans': 446, 'green_peas': 81, 'sunflower_seeds': 584,
    'flaxseeds': 534, 'chia_seeds': 486,

    # Grains
    'white_rice': 130, 'brown_rice': 111, 'quinoa': 120, 'oats': 389, 'whole_wheat_bread': 247, 'white_bread': 265, 
    'pasta': 157, 'barley': 354, 'millet': 378, 'cornmeal': 384, 'buckwheat': 343,

    # Dairy
    'milk': 42, 'cheese': 402, 'yogurt': 59, 'butter': 717, 'cream': 340, 'cottage_cheese': 98, 'ice_cream': 207,

    # Meat & Seafood
    'chicken_breast': 165, 'chicken_thigh': 209, 'beef': 250, 'pork': 242, 'salmon': 206, 'tuna': 132, 'shrimp': 85, 
    'egg': 78, 'duck': 337, 'lamb': 294, 'turkey': 189,

    # Beverages
    'coffee': 2, 'tea': 0, 'orange_juice': 45, 'apple_juice': 46, 'soda': 140,

    # Snacks & Desserts
    'dark_chocolate': 604, 'popcorn': 387, 'peanut_butter': 588, 'granola_bar': 250, 'cookies': 502, 'cake': 350, 
    'candy_bar': 541, 'honey': 304, 'mixing_bowl':1024, 
    }
        
        sugar_dict = {
    # Fast Food
    'pizza': 3.6, 'burger': 4.2, 'salad': 2.1, 'hotdog': 1.5, 'fries': 0.3,

    # Fruits
    'banana': 12.2, 'lemon': 2.5, 'bell_pepper': 2.4, 'apple': 10.4, 'orange': 8.2, 'grapes': 15.5, 'watermelon': 6.2, 
    'strawberry': 4.9, 'blueberry': 9.7, 'pineapple': 9.9, 'mango': 13.7, 'kiwi': 8.9, 'pomegranate': 13.7, 'peach': 8.4, 
    'plum': 9.9, 'pear': 9.8, 'cherry': 12.8, 'fig': 16.3, 'apricot': 3.9, 'coconut': 6.2, 'blackberry': 4.9, 'raspberry': 4.4, 
    'guava': 5.4, 'papaya': 5.9, 'cranberry': 4.0, 'dragonfruit': 8.0, 'lychee': 15.2, 'jackfruit': 19.1, 'dates': 66.5,

    # Vegetables
    'carrot': 4.7, 'broccoli': 1.7, 'spinach': 0.4, 'potato': 0.9, 'sweet_potato': 4.2, 'cabbage': 3.2, 'lettuce': 0.8, 
    'cucumber': 1.7, 'tomato': 2.6, 'onion': 4.2, 'garlic': 1.0, 'ginger': 1.7, 'beetroot': 6.8, 'cauliflower': 1.9, 
    'zucchini': 2.0, 'brussels_sprout': 2.2, 'pumpkin': 2.8, 'radish': 1.9, 'asparagus': 1.9, 'okra': 1.5, 'artichoke': 0.9, 
    'mushroom': 1.0, 'avocado': 0.2, 'corn': 6.3, 'celery': 1.4, 'kale': 1.6, 'bok_choy': 1.2, 'turnip': 3.8, 'parsnip': 4.8, 
    'swiss_chard': 1.1, 'arugula': 2.1, 'seaweed': 0.9, 'butternut_squash': 4.5, 'spaghetti_squash': 2.8,

    # Nuts & Legumes
    'almond': 4.4, 'walnut': 2.6, 'cashew': 5.9, 'peanut': 4.2, 'hazelnut': 4.3, 'pistachio': 7.7, 'chickpeas': 10.7, 
    'lentils': 2.0, 'kidney_beans': 0.3, 'black_beans': 0.5, 'soybeans': 7.5, 'green_peas': 5.7, 'sunflower_seeds': 2.6, 
    'flaxseeds': 1.5, 'chia_seeds': 0.8,

    # Grains
    'white_rice': 0.2, 'brown_rice': 0.7, 'quinoa': 0.9, 'oats': 0.5, 'whole_wheat_bread': 3.8, 'white_bread': 5.0, 
    'pasta': 0.9, 'barley': 0.8, 'millet': 1.3, 'cornmeal': 1.5, 'buckwheat': 1.0,

    # Dairy
    'milk': 5.0, 'cheese': 1.3, 'yogurt': 4.7, 'butter': 0.1, 'cream': 3.0, 'cottage_cheese': 2.7, 'ice_cream': 21.2,

    # Meat & Seafood
    'chicken_breast': 0, 'chicken_thigh': 0, 'beef': 0, 'pork': 0, 'salmon': 0, 'tuna': 0, 'shrimp': 0, 
    'egg': 0.3, 'duck': 0, 'lamb': 0, 'turkey': 0,

    # Beverages
    'coffee': 0, 'tea': 0, 'orange_juice': 8.4, 'apple_juice': 9.6, 'soda': 39,

    # Snacks & Desserts
    'dark_chocolate': 24.0, 'popcorn': 0.9, 'peanut_butter': 9.2, 'granola_bar': 18.0, 'cookies': 38.2, 'cake': 38.0, 
    'candy_bar': 48.5, 'honey': 82.4
}



        protein_dict = {
    # Fast Food
    'pizza': 12, 'burger': 17, 'salad': 3, 'hotdog': 10, 'fries': 3.4,  

    # Fruits
    'banana': 1.3, 'lemon': 1.1, 'bell_pepper': 1, 'apple': 0.5, 'orange': 1.2, 'grapes': 0.7, 'watermelon': 0.6, 
    'strawberry': 0.8, 'blueberry': 0.7, 'pineapple': 0.5, 'mango': 0.8, 'kiwi': 1.1, 'pomegranate': 1.7, 'peach': 0.9, 
    'plum': 0.7, 'pear': 0.4, 'cherry': 1.1, 'fig': 0.8, 'apricot': 1.4, 'coconut': 3.3, 'blackberry': 2, 'raspberry': 1.5, 
    'guava': 2.6, 'papaya': 0.5, 'cranberry': 0.4, 'dragonfruit': 1.2, 'lychee': 0.8, 'jackfruit': 1.7, 'dates': 2.5,

    # Vegetables
    'carrot': 0.9, 'broccoli': 4.3, 'spinach': 2.9, 'potato': 2, 'sweet_potato': 1.6, 'cabbage': 1.3, 'lettuce': 1.4, 
    'cucumber': 0.7, 'tomato': 0.9, 'onion': 1.1, 'garlic': 6.4, 'ginger': 1.8, 'beetroot': 1.6, 'cauliflower': 1.9, 
    'zucchini': 1.2, 'brussels_sprout': 3.4, 'pumpkin': 1, 'radish': 0.7, 'asparagus': 2.2, 'okra': 1.9, 'artichoke': 3.3, 
    'mushroom': 3.1, 'avocado': 2, 'corn': 3.4, 'celery': 0.7, 'kale': 4.3, 'bok_choy': 1.5, 'turnip': 1, 'parsnip': 1.2, 
    'swiss_chard': 1.8, 'arugula': 2.6, 'seaweed': 5, 'butternut_squash': 1, 'spaghetti_squash': 0.6,

    # Nuts & Legumes
    'almond': 21, 'walnut': 15, 'cashew': 18, 'peanut': 25, 'hazelnut': 15, 'pistachio': 20, 'chickpeas': 9, 
    'lentils': 9, 'kidney_beans': 9, 'black_beans': 9, 'soybeans': 36, 'green_peas': 5.4, 'sunflower_seeds': 20, 
    'flaxseeds': 18, 'chia_seeds': 17,

    # Grains
    'white_rice': 2.7, 'brown_rice': 2.6, 'quinoa': 4.1, 'oats': 13, 'whole_wheat_bread': 13, 'white_bread': 8.5, 
    'pasta': 5.8, 'barley': 12, 'millet': 11, 'cornmeal': 7.5, 'buckwheat': 13,

    # Dairy
    'milk': 3.4, 'cheese': 25, 'yogurt': 10, 'butter': 0.9, 'cream': 2.8, 'cottage_cheese': 11, 'ice_cream': 4,

    # Meat & Seafood
    'chicken_breast': 31, 'chicken_thigh': 24, 'beef': 26, 'pork': 25, 'salmon': 22, 'tuna': 29, 'shrimp': 20, 
    'egg': 13, 'duck': 27, 'lamb': 25, 'turkey': 29,'mixing_bowl':102,

    # Beverages
    'coffee': 0.1, 'tea': 0, 'orange_juice': 0.7, 'apple_juice': 0.1, 'soda': 0,

    # Snacks & Desserts
    'dark_chocolate': 7.8, 'popcorn': 12, 'peanut_butter': 25, 'granola_bar': 7, 'cookies': 6, 'cake': 5, 
    'candy_bar': 5, 'honey': 0.3
    }

        carbs_dict = {
    # Fast Food
    'pizza': 36, 'burger': 29, 'salad': 7, 'hotdog': 23, 'fries': 30, 

    # Fruits
    'banana': 27, 'lemon': 9.3, 'bell_pepper': 6, 'apple': 25, 'orange': 15.5, 'grapes': 18, 'watermelon': 8, 
    'strawberry': 7.7, 'blueberry': 14.5, 'pineapple': 13, 'mango': 25, 'kiwi': 10, 'pomegranate': 19, 'peach': 14, 
    'plum': 11, 'pear': 27, 'cherry': 16, 'fig': 19, 'apricot': 11, 'coconut': 15, 'blackberry': 10, 'raspberry': 12, 
    'guava': 14, 'papaya': 11, 'cranberry': 12, 'dragonfruit': 13, 'lychee': 16, 'jackfruit': 24, 'dates': 75,

    # Vegetables
    'carrot': 10, 'broccoli': 11, 'spinach': 3.6, 'potato': 17, 'sweet_potato': 20, 'cabbage': 6, 'lettuce': 2.9, 
    'cucumber': 3.6, 'tomato': 4.7, 'onion': 9, 'garlic': 33, 'ginger': 18, 'beetroot': 9, 'cauliflower': 5, 
    'zucchini': 3, 'brussels_sprout': 9, 'pumpkin': 6.5, 'radish': 3, 'asparagus': 3.9, 'okra': 7.5, 'artichoke': 11, 
    'mushroom': 3.3, 'avocado': 9, 'corn': 21, 'celery': 3, 'kale': 10, 'bok_choy': 2.2, 'turnip': 6, 'parsnip': 18, 
    'swiss_chard': 3, 'arugula': 3.7, 'seaweed': 10, 'butternut_squash': 11, 'spaghetti_squash': 10,

    # Nuts & Legumes
    'almond': 21, 'walnut': 14, 'cashew': 30, 'peanut': 16, 'hazelnut': 17, 'pistachio': 28, 'chickpeas': 27, 
    'lentils': 20, 'kidney_beans': 22, 'black_beans': 23, 'soybeans': 30, 'green_peas': 14, 'sunflower_seeds': 20, 
    'flaxseeds': 29, 'chia_seeds': 42,

    # Grains
    'white_rice': 28, 'brown_rice': 23, 'quinoa': 21, 'oats': 67, 'whole_wheat_bread': 41, 'white_bread': 49, 
    'pasta': 31, 'barley': 73, 'millet': 72, 'cornmeal': 79, 'buckwheat': 71,'mixing_bowl':73,

    # Dairy, Meat, Beverages, Snacks omitted for brevity...
}


        fat_dict = {
    # Fast Food
    'pizza': 10, 'burger': 19, 'salad': 7, 'hotdog': 13, 'fries': 10,  

    # Fruits
    'banana': 0.3, 'lemon': 0.3, 'bell_pepper': 0.3, 'apple': 0.3, 'orange': 0.2, 'grapes': 0.2, 'watermelon': 0.2, 
    'strawberry': 0.3, 'blueberry': 0.3, 'pineapple': 0.1, 'mango': 0.6, 'kiwi': 0.4, 'pomegranate': 1.2, 'peach': 0.3, 
    'plum': 0.3, 'pear': 0.2, 'cherry': 0.2, 'fig': 0.3, 'apricot': 0.4, 'coconut': 33, 'blackberry': 0.5, 'raspberry': 0.7, 
    'guava': 0.9, 'papaya': 0.3, 'cranberry': 0.1, 'dragonfruit': 0.1, 'lychee': 0.4, 'jackfruit': 0.6, 'dates': 0.2,

    # Vegetables
    'carrot': 0.2, 'broccoli': 0.4, 'spinach': 0.4, 'potato': 0.1, 'sweet_potato': 0.1, 'cabbage': 0.1, 'lettuce': 0.2, 
    'cucumber': 0.1, 'tomato': 0.2, 'onion': 0.1, 'garlic': 0.5, 'ginger': 0.8, 'beetroot': 0.1, 'cauliflower': 0.3, 
    'zucchini': 0.3, 'brussels_sprout': 0.3, 'pumpkin': 0.1, 'radish': 0.1, 'asparagus': 0.2, 'okra': 0.2, 'artichoke': 0.3, 
    'mushroom': 0.3, 'avocado': 21, 'corn': 1.2, 'celery': 0.1, 'kale': 0.7, 'bok_choy': 0.2, 'turnip': 0.1, 'parsnip': 0.3, 
    'swiss_chard': 0.2, 'arugula': 0.7, 'seaweed': 0.6, 'butternut_squash': 0.1, 'spaghetti_squash': 0.3,

    # Nuts & Legumes
    'almond': 50, 'walnut': 65, 'cashew': 44, 'peanut': 49, 'hazelnut': 61, 'pistachio': 45, 'chickpeas': 2.6, 
    'lentils': 0.4, 'kidney_beans': 0.5, 'black_beans': 0.5, 'soybeans': 20, 'green_peas': 0.4, 'sunflower_seeds': 51, 
    'flaxseeds': 42, 'chia_seeds': 31,

    # Grains
    'white_rice': 0.3, 'brown_rice': 0.9, 'quinoa': 1.9, 'oats': 6.9, 'whole_wheat_bread': 4.2, 'white_bread': 3.2, 
    'pasta': 1.1, 'barley': 2.3, 'millet': 4.2, 'cornmeal': 3.9, 'buckwheat': 3.4,

    # Dairy
    'milk': 1, 'cheese': 33, 'yogurt': 3.3, 'butter': 81, 'cream': 36, 'cottage_cheese': 4.3, 'ice_cream': 11,

    # Meat & Seafood
    'chicken_breast': 3.6, 'chicken_thigh': 8, 'beef': 19, 'pork': 21, 'salmon': 13, 'tuna': 1, 'shrimp': 1.7, 
    'egg': 11, 'duck': 28, 'lamb': 21, 'turkey': 7.4,'mixing_bowl':24,

    # Beverages
    'coffee': 0.2, 'tea': 0, 'orange_juice': 0.2, 'apple_juice': 0.1, 'soda': 0,

    # Snacks & Desserts
    'dark_chocolate': 43, 'popcorn': 4.5, 'peanut_butter': 50, 'granola_bar': 11, 'cookies': 24, 'cake': 15, 
    'candy_bar': 30, 'honey': 0
}

    
        

        # Load Model
        @st.cache_resource
        def load_model():
            return ResNet50(weights='imagenet', include_top=True)

        model = load_model()

        # Classify Image
        def classify_image(model, preprocess_input, uploaded_file, decode_predictions):
            try:
                img = image.load_img(uploaded_file, target_size=(224, 224))
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = preprocess_input(img_array)

                predictions = model.predict(img_array)
                decoded_predictions = decode_predictions(predictions, top=3)[0]

                return decoded_predictions
            except Exception as e:
                st.error(f"⚠ Error processing image: {e}")
                return []

        predictions = classify_image(model, preprocess_input_resnet, uploaded_image, decode_predictions_resnet)

        # 🔷 Display Results

        if predictions:
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("🔍 Meal Analysis Results")
            for i, (imagenet_id, label, score) in enumerate(predictions):
                global calorie_value
                calorie_value = calories_dict.get(label.lower(), "Not available")
                if calorie_value!="Not available":
                    calorie_value*=qty
                global protein_value
                protein_value = protein_dict.get(label.lower(), "Not available")
                if protein_value!="Not available":
                    protein_value*=qty
                global fat_value 
                fat_value = fat_dict.get(label.lower(), "Not available")
                if fat_value!="Not available":
                    fat_value*=qty
                global sugar_value 
                sugar_value =sugar_dict.get(label.lower(), "Not available")
                if sugar_value!="Not available":
                    sugar_value*=qty
                st.write(f"**Prediction {i + 1}:** {label} (🔥 Confidence: {score:.2%}),  **Protein:** {protein_value} grams,  **Calories:** {calorie_value} kcal,  **Fats:** {fat_value} grams, **Sugar:** {fat_value} grams")
            st.session_state.predicted_cnt = sum(calories_dict.get(label.lower(), 0) for _, label, _ in predictions)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
             st.markdown(""" <div class="stSucc"> 
        ⚠ No predictions available. Try a different image.
        </div> """,unsafe_allow_html=True)

    st.subheader(" Select below if Any of the Problem You Are Having")
    global BodyState
    BodyState = st.selectbox("", ["Select","diabetes", "heart_disease", "obesity", "hypertension (high blood pressure)","PCOS (Polycystic Ovary Syndrome)","thyroid disorders (hypothyroidism)","liver disease (fatty liver)","kidney disease","anemia","osteoporosis","cancer patients (during treatment)"] )
    print(BodyState)
    if BodyState!='Select' and uploaded_image:
        max_intake = {
    "diabetes": {
        "max_calories": 1800,  # Typically 1500-2000 kcal/day
        "max_fat": 50,  # Keep saturated fat low (<10% of total calories)
        "max_sugar": 25  # WHO recommends <25g added sugar
    },
    "heart_disease": {
        "max_calories": 2000,  # General healthy diet
        "max_fat": 60,  # 20-35% of total calories from fat
        "max_sugar": 25  # Limit added sugars to prevent cholesterol buildup
    },
    "obesity": {
        "max_calories": 1200,  # Caloric deficit diet
        "max_fat": 40,  # Reduced fat intake
        "max_sugar": 15  # Minimal added sugar
    },
    "hypertension (high blood pressure)": {
        "max_calories": 2000,  
        "max_fat": 55,  # Focus on healthy fats (avocado, nuts)
        "max_sugar": 25  # Low added sugar to maintain blood pressure
    },
    "PCOS (Polycystic Ovary Syndrome)": {
        "max_calories": 1800,  
        "max_fat": 50,  
        "max_sugar": 20  # Low sugar to manage insulin resistance
    },
    "thyroid disorders (hypothyroidism)": {
        "max_calories": 1600,  # Moderate calorie intake
        "max_fat": 50,  # Balanced fat intake
        "max_sugar": 25  # Avoid excess sugar to control weight gain
    },
    "liver disease (fatty liver)": {
        "max_calories": 1500,  # Controlled intake to reduce fat accumulation
        "max_fat": 40,  # Low-fat diet
        "max_sugar": 20  # Reduce fructose/sugar to prevent fat buildup
    },
    "kidney disease": {
        "max_calories": 2000,  # Balanced intake
        "max_fat": 50,  # Moderate fat intake
        "max_sugar": 30  # Low sugar for blood pressure control
    },
    "anemia": {
        "max_calories": 2200,  # Increased energy intake
        "max_fat": 60,  # Healthy fats are beneficial
        "max_sugar": 30  # Normal sugar levels
    },
    "osteoporosis": {
        "max_calories": 2000,  # Normal intake
        "max_fat": 60,  # Healthy fats for bone health
        "max_sugar": 30  # Normal sugar intake
    },
    "cancer patients (during treatment)": {
        "max_calories": 2500,  # Increased energy needs
        "max_fat": 80,  # Healthy fats for energy
        "max_sugar": 40  # Can be slightly higher for energy
    }
}       
        
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("🔍 Current Health condition Based Analysis Results")
        st.write(f"Selected Condition: {BodyState}")  # Debugging step
        defl=False
        if (max_intake[BodyState]['max_calories'])< (calorie_value):
            diff=calorie_value - max_intake[BodyState]['max_calories'] 
            st.warning(f"⚠ Your Intake calories is {diff} More than the Maximum suggested calories for {BodyState} : {max_intake[BodyState]['max_calories']}")
            defl=True
        if (max_intake[BodyState]['max_fat'])<(fat_value):
            diff=fat_value - max_intake[BodyState]['max_fat']
            defl=True
            st.warning(f"⚠ Your Intake Fat is {diff} More than the Maximum suggested calories for {BodyState} : {max_intake[BodyState]['max_fat'] }")
        if (max_intake[BodyState]['max_sugar'])<(sugar_value):
            diff=sugar_value - max_intake[BodyState]['max_sugar']
            defl=True
            st.warning(f"⚠ Your Intake Sugar is {diff} More than the Maximum suggested calories for {BodyState} : {max_intake[BodyState]['max_sugar']}")
        if not defl:
            st.info("✅ **Bingo-->:** It Seems Your Intake is Not Harmfull for Your Condition.")

        st.markdown('</div>', unsafe_allow_html=True)



elif option == "🥗 Find Your Diet Plan":
    calorie_difference = st.session_state.calories - st.session_state.predicted_cnt
    if calorie_difference > 0:
        st.success(f"✅ Your meal contains **{st.session_state.predicted_cnt} kcal**, which is **{calorie_difference} kcal** less than your required intake.")
        st.write("💡 **Suggestion:** You need to consume additional calories to meet your daily needs.")
        
        additional_foods = ["Nuts", "Avocado", "Whole grains", "Dairy products", "Lean proteins"]
        st.markdown("🍽 **You can add:** " + ", ".join(additional_foods))
        
        st.markdown("### 🍽 **Suggested Meal Plan for the Day**")
        image_width = 200
        image_height = 150  
        col1, col2, col3 = st.columns(3)
        with col1:
            img1 = resize_image("https://thumbs.dreamstime.com/b/nutritious-colorful-breakfast-smoothie-blended-fresh-fruits-yogurt-sprinkle-granola-served-tall-frosted-glass-274748062.jpg", image_width, image_height)
            st.image(img1, caption="Oatmeal with Fruits & Nuts")
        with col2:
            #st.image("https://i.ytimg.com/vi/JqAYN1i0a4Y/maxresdefault.jpg", caption="Brown Rice & Chicken", width=150)
             img1 = resize_image("https://theviewfromgreatisland.com/wp-content/uploads/2013/02/DIY-Instant-Fruit-and-Nut-Oatmeal-vegan-and-gluten-free.jpg", image_width, image_height)
             st.image(img1, caption="Oatmeal with fruits and nuts, or scrambled eggs with whole grain toast")
        with col3:
            #st.image("https://www.eatingbirdfood.com/wp-content/uploads/2022/05/Protein-Salads-BLOG-IMAGE-min.jpg", caption="Salad & Cottage Cheese", width=150)
            img1 = resize_image("https://runningonrealfood.com/wp-content/uploads/2020/08/Healthy-Vegan-Tofu-Tempeh-Chickpea-Protein-Salad-19-700x1050.jpg", image_width, image_height)
            st.image(img1, caption="Light dinner with a salad and protein-rich food like cottage cheese or tofu.")

    elif calorie_difference < 0:
        st.warning(f"⚠ Your meal contains **{st.session_state.predicted_cnt} kcal**, which **exceeds your required intake** by **{-calorie_difference} kcal**.")
        st.write("💡 **Suggestion:** Consider adjusting your meals to balance your daily intake.")

        st.markdown("### 🍽 **Recommended Adjustments for Your Diet**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://thumbs.dreamstime.com/b/nutritious-colorful-breakfast-smoothie-blended-fresh-fruits-yogurt-sprinkle-granola-served-tall-frosted-glass-274748062.jpg", caption="Fruit Smoothie", width=150)
            st.write("**Morning:** Light breakfast with a fruit smoothie or yogurt.")
        with col2:
            st.image("https://th.bing.com/th/id/OIP.YCBbm9Weva0zCqR9BCi0IAHaEJ?rs=1&pid=ImgDetMain", caption="Lean Protein & Veggies", width=150)
            st.write("**Afternoon:** Opt for a balanced portion of lean protein with lots of vegetables.")
        with col3:
            st.image("https://th.bing.com/th/id/R.c2f38784bc7b87cf7d3f7158d979afeb?rik=5JLb2tVPvoMgrQ&riu=http%3a%2f%2fwww.muddyplimsolls.com%2fwp-content%2fuploads%2f2012%2f05%2fTasty-Lunchbox-Salad.jpg&ehk=OhUUaSdHWahatTJUP3OLMwi0rsAQvWmPvRyWJi5PAVU%3d&risl=&pid=ImgRaw&r=0", caption="Light Salad", width=150)
            st.write("**Evening:** Avoid high-carb or heavy meals; consider a light salad with some nuts.")

        st.info("✅ **Tip:** Increase physical activity to burn excess calories.")
    else:
        st.markdown(""" <div class="stSucc"> 
        🎯 Perfect! Your meal intake is well-balanced with your daily needs.
        </div> """,unsafe_allow_html=True)
elif option=="📃Plan Your Diet-chart":
    if "page" not in st.session_state:
        st.session_state.page = "home"
    def go_to_results():
        st.session_state.page = "results"
    def calculate_bmi(weight, height):
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"
        return round(bmi, 1), category
    def get_current_location():
        try:
            g = geocoder.ip('me')
            if g.ok and g.city and g.country:
                return f"{g.city}, {g.country}"
            elif g.ok and g.country:
                return g.country
        except:
            return None
    if st.session_state.page == "home":
        st.markdown("<h1 style='color:#2989ff;'>🥗 Smart Diet Planner</h1>", unsafe_allow_html=True)
        use_geo = st.toggle("📍 Use my location automatically")
        if use_geo:
            detected_location = get_current_location()
            if detected_location:
                st.success(f"Detected location: {detected_location}")
                location = detected_location
            else:
                st.warning("Unable to detect location. Please enter manually.")
                use_geo = False
        if not use_geo:
            location = st.text_input("Enter your location (City, State or Country)", placeholder="e.g., Bangalore, India")
        with st.form("diet_form"):
            st.subheader("👤 Your Info")
            name = st.text_input("Name")
            col1, col2 = st.columns(2)
            with col1:
                height = st.number_input("Height (cm)", min_value=50, max_value=250)
            with col2:
                weight = st.number_input("Weight (kg)", min_value=20, max_value=200)
            st.subheader("🍽️ Preferences")
            season = st.selectbox("Season", ["Summer", "Winter", "Monsoon"])
            meal_type = st.radio("Meal Type", ["Veg", "Non-Veg", "Vegan"], horizontal=True)
            diet_type = st.selectbox("Diet Goal", [
            "Low Calorie", "High Protein", "Vegan", "Diabetic-Friendly", "Keto", "Gluten-Free"])
            submitted = st.form_submit_button("Get My Diet Chart")
            if submitted:
                if not location:
                    st.error("📍 Please enter or detect a location to continue.")
                else:
                    with st.spinner("⏳ Generating your personalized diet chart..."):
                        bmi, category = calculate_bmi(weight, height)
                        prompt = f"""
                        You are a certified nutritionist. Generate a one-day diet chart for a person living in {location} during the {season} season.
                        Name: {name}, Height: {height} cm, Weight: {weight} kg (BMI: {bmi}, {category})
                        Preferences: {meal_type} | Goal: {diet_type}
                        Provide the following sections clearly:
                        - Breakfast
                        - Lunch
                        - Dinner
                        - Side Dish
                        - Fruits
                        - Vegetables
                        Use local and seasonal foods from {location}. Format the output with clear section headings and avoid using asterisks (*).
                        """
                        try:
                            response = model.generate_content(prompt)
                            tip_prompt = f"Give one practical tip for someone on a {diet_type.lower()} diet from {location} with BMI {bmi} ({category})."
                            tip = model.generate_content(tip_prompt).text.strip()
                            st.session_state.diet_chart = response.text
                            st.session_state.tip = tip
                            st.session_state.bmi = bmi
                            st.session_state.bmi_category = category
                            st.session_state.name = name
                            go_to_results()
                        except Exception as e:
                            st.error("❌ Error generating content. Please check your API key.")
                            st.text(f"Error: {e}")
    elif st.session_state.page == "results":
        st.markdown("<h1 style='color:#2989ff;'>🧾 Your Personalized Diet Chart</h1>", unsafe_allow_html=True)
        st.markdown(f"#### 👋 Hello, **{st.session_state.name}**!")
        st.markdown(f"**🧮 BMI:** `{st.session_state.bmi}` ({st.session_state.bmi_category})")
        st.markdown("### 🍽️ Diet Chart")
        chart = st.session_state.diet_chart
        sections = ["Breakfast", "Lunch", "Dinner", "Side Dish", "Fruits", "Vegetables"]
        split_chart = {key: "" for key in sections}
        current_section = None
        for line in chart.splitlines():
            line = re.sub(r"[*•]", "", line).strip()  # Remove unwanted symbols
            for section in sections:
                if section.lower() in line.lower():
                    current_section = section
                    break
            else:
                if current_section:
                    split_chart[current_section] += line + " "
        for section in sections:
            if split_chart[section].strip():
                st.markdown(f"""
                        <div style="background-color:#f4f9ff;padding:15px 20px;margin-bottom:10px;
                            border-radius:10px;border-left:5px solid #2989ff;">
                    <h4 style='color:#2989ff'>{section}</h4>
                    <p style='color:#333;'>{split_chart[section].strip()}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("### 💡 Daily Tip")
        st.info(st.session_state.tip)
    if st.button("🔄 Generate Another"):
        st.session_state.page = "home"

       
# ✅ Footer
st.markdown("---")
st.markdown("💡 **Built with AI & Streamlit | Powered by Deep Learning**")
