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
st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.title("🍴 NutriPlanAI - AI Meal Planner")
st.subheader("🧠 Smart Meal Planning & Calorie Estimation")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ✅ Sidebar for Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("", ("🏠 Home", "🔍 Find Calories in Meal", "🥗 Find Your Diet Plan"))

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
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.write(
        "Welcome to **NutriPlanAI**, your personal AI-powered nutrition assistant. "
        "Upload your meal image to find calorie estimates, or get a personalized diet plan!"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ Find Calories in Meal Page
elif option == "🔍 Find Calories in Meal":
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

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
    'candy_bar': 541, 'honey': 304
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
    'egg': 13, 'duck': 27, 'lamb': 25, 'turkey': 29,

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
    'pasta': 31, 'barley': 73, 'millet': 72, 'cornmeal': 79, 'buckwheat': 71,

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
    'egg': 11, 'duck': 28, 'lamb': 21, 'turkey': 7.4,

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
                calorie_value = calories_dict.get(label.lower(), "Not available")
                protein_value = protein_dict.get(label.lower(), "Not available")
                fat_value = fat_dict.get(label.lower(), "Not available")
                st.write(f"**Prediction {i + 1}:** {label} (🔥 Confidence: {score:.2%}),  **Protein:** {protein_value} grams,  **Calories:** {calorie_value} kcal,  **Fats:** {fat_value} grams")
            st.session_state.predicted_cnt = sum(calories_dict.get(label.lower(), 0) for _, label, _ in predictions)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
             st.markdown(""" <div class="stSucc"> 
        ⚠ No predictions available. Try a different image.
        </div> """,unsafe_allow_html=True)
            
        
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
       
# ✅ Footer
st.markdown("---")
st.markdown("💡 **Built with AI & Streamlit | Powered by Deep Learning**")
