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
        .stApp { background: linear-gradient(to right, #ff9966, #ff5e62); }
        .block-container { max-width: 800px; margin: auto; padding: 2rem; }
        .stCard { background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px;
                  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); backdrop-filter: blur(10px); }
        .stButton button { background-color: #ff4b4b !important; color: white !important;
                           border-radius: 10px; font-size: 18px; padding: 12px 24px; transition: 0.3s ease; }
        .stButton button:hover { background-color: #cc0000 !important; transform: scale(1.05); }
        .stRadio div { display: flex; justify-content: center; gap: 15px; }
        .stTextInput input, .stNumberInput input, .stSelectbox select { border-radius: 8px !important;
                                                                        padding: 8px !important; font-size: 16px !important; }
        .stImage img { max-width: 100%; border-radius: 12px; box-shadow: 0px 3px 10px rgba(0,0,0,0.2); }
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
    st.subheader("📸 Upload Your Meal Image")
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
    uploaded_image = st.file_uploader("Upload your meal image...", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Meal Image", use_column_width=True)

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
                st.write(f"**Prediction {i + 1}:** {label} (🔥 Confidence: {score:.2%}), **Calories:** {calorie_value}")
            st.session_state.predicted_cnt = sum(calories_dict.get(label.lower(), 0) for _, label, _ in predictions)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("⚠ No predictions available. Try a different image.")
        
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
        st.success("🎯 Perfect! Your meal intake is well-balanced with your daily needs.")
# ✅ Footer
st.markdown("---")
st.markdown("💡 **Built with AI & Streamlit | Powered by Deep Learning**")
