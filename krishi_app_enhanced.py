import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import time
import random

# Page configuration
st.set_page_config(
    page_title="Krishi Saaransh - Smart Farmer Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with better styling and mobile responsiveness
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        border: 2px solid #FFD700;
    }
    
    .main-header h1 {
        color: #2E8B57;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .main-header h3 {
        color: #1e3c1e;
        margin-top: 0.5rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1e3c1e 0%, #2e4f2e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #138808;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
    }
    
    .weather-card {
        background: linear-gradient(135deg, #1e2b3e 0%, #2f3e4f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        border: 2px solid #4169E1;
    }
    
    .price-card {
        background: linear-gradient(135deg, #2e2e2e 0%, #3e3e3e 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #FF9933;
        transition: all 0.3s ease;
    }
    
    .price-card:hover {
        border-left: 8px solid #FF9933;
        transform: translateX(5px);
    }
    
    .scheme-card {
        background: linear-gradient(135deg, #2a2a40 0%, #3a3a50 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #4169E1;
        transition: all 0.3s ease;
    }
    
    .scheme-card:hover {
        border-left: 8px solid #4169E1;
        transform: translateX(5px);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #DCF8C6 0%, #C8E6C9 100%);
        border-left: 4px solid #25D366;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #F1F1F1 0%, #E8E8E8 100%);
        border-left: 4px solid #128C7E;
        margin-right: 2rem;
    }
    
    .alert-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 4px solid #FF0000;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 4px solid #00FF00;
    }
    
    .info-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 4px solid #0000FF;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 3px solid #138808;
    }
    
    .quick-action-btn {
        background: linear-gradient(45deg, #FF9933, #FFB366);
        border: none;
        color: white;
        padding: 0.7rem 1rem;
        border-radius: 25px;
        margin: 0.3rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quick-action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #FF9933, #138808);
        color: white;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
            font-size: 0.9rem;
        }
        .feature-card, .weather-card {
            padding: 1rem;
        }
        .user-message {
            margin-left: 0.5rem;
        }
        .bot-message {
            margin-right: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with better defaults
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'  # Default to English
if 'user_location' not in st.session_state:
    st.session_state.user_location = {'city': 'Delhi', 'state': 'Delhi'}
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'farm_size': 1.0,
        'primary_crops': [],
        'farming_experience': 'Beginner'
    }
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'saved_data' not in st.session_state:
    st.session_state.saved_data = {
        'favorite_crops': [],
        'bookmarked_schemes': [],
        'price_alerts': []
    }

# Enhanced Language translations with more languages
TRANSLATIONS = {
    'English': {
        'welcome': 'Welcome',
        'app_name': 'Krishi Saaransh - Smart Farmer Assistant',
        'description': 'AI-Powered Platform for Indian Farmers',
        'weather': 'Weather Forecast',
        'crop_planning': 'Crop Planning',
        'market_prices': 'Market Prices',
        'govt_schemes': 'Government Schemes',
        'ai_assistant': 'AI Assistant',
        'profile': 'Farmer Profile',
        'notifications': 'Notifications',
        'location': 'Location',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'rainfall': 'Rainfall',
        'crop_recommendations': 'Crop Recommendations',
        'ask_question': 'Ask your farming question here...',
        'send': 'Send Message',
        'quick_questions': 'Quick Questions',
        'weather_info': 'Weather Info',
        'crop_advice': 'Crop Advice',
        'price_check': 'Price Check',
        'scheme_info': 'Scheme Info',
        'farming_tips': 'Farming Tips',
        'pest_control': 'Pest Control'
    },
    'Hindi': {
        'welcome': 'स्वागत है',
        'app_name': 'कृषि सारांश - स्मार्ट किसान सहायक',
        'description': 'भारतीय किसानों के लिए AI-संचालित प्लेटफॉर्म',
        'weather': 'मौसम पूर्वानुमान',
        'crop_planning': 'फसल योजना',
        'market_prices': 'बाजार मूल्य',
        'govt_schemes': 'सरकारी योजनाएं',
        'ai_assistant': 'AI सहायक',
        'profile': 'किसान प्रोफ़ाइल',
        'notifications': 'सूचनाएं',
        'location': 'स्थान',
        'temperature': 'तापमान',
        'humidity': 'आर्द्रता',
        'rainfall': 'वर्षा',
        'crop_recommendations': 'फसल सुझाव',
        'ask_question': 'अपना कृषि प्रश्न यहाँ पूछें...',
        'send': 'संदेश भेजें',
        'quick_questions': 'त्वरित प्रश्न',
        'weather_info': 'मौसम जानकारी',
        'crop_advice': 'फसल सलाह',
        'price_check': 'मूल्य जांच',
        'scheme_info': 'योजना जानकारी',
        'farming_tips': 'कृषि टिप्स',
        'pest_control': 'कीट नियंत्रण'
    },
    'Tamil': {
        'welcome': 'வணக்கம்',
        'app_name': 'கிருஷி சாரன்ஷ் - ஸ்மார்ட் விவசாயி உதவியாளர்',
        'description': 'இந்திய விவசாயிகளுக்கான AI-இயங்கும் தளம்',
        'weather': 'வானிலை முன்னறிவிப்பு',
        'crop_planning': 'பயிர் திட்டமிடல்',
        'market_prices': 'சந்தை விலைகள்',
        'govt_schemes': 'அரசு திட்டங்கள்',
        'ai_assistant': 'AI உதவியாளர்',
        'profile': 'விவசாயி சுயவிவரம்',
        'notifications': 'அறிவிப்புகள்',
        'location': 'இடம்',
        'temperature': 'வெப்பநிலை',
        'humidity': 'ஈரப்பதம்',
        'rainfall': 'மழைப்பொழிவு',
        'crop_recommendations': 'பயிர் பரிந்துரைகள்',
        'ask_question': 'உங்கள் வேளாண் கேள்வியை இங்கே கேளுங்கள்...',
        'send': 'செய்தி அனுப்பு',
        'quick_questions': 'விரைவு கேள்விகள்',
        'weather_info': 'வானிலை தகவல்',
        'crop_advice': 'பயிர் ஆலோசனை',
        'price_check': 'விலை சரிபார்ப்பு',
        'scheme_info': 'திட்ட தகவல்',
        'farming_tips': 'வேளாண் குறிப்புகள்',
        'pest_control': 'பூச்சி கட்டுப்பாடு'
    },
    'Telugu': {
        'welcome': 'స్వాగతం',
        'app_name': 'కృషి సారాంశ్ - స్మార్ట్ రైతు సహాయకుడు',
        'description': 'భారతీయ రైతుల కోసం AI-ఆధారిత ప్లాట్‌ఫారం',
        'weather': 'వాతావరణ సూచన',
        'crop_planning': 'పంట ప్రణాళిక',
        'market_prices': 'మార్కెట్ ధరలు',
        'govt_schemes': 'ప్రభుత్వ పథకాలు',
        'ai_assistant': 'AI సహాయకుడు',
        'profile': 'రైతు ప్రొఫైల్',
        'notifications': 'నోటిఫికేషన్లు',
        'location': 'స్థానం',
        'temperature': 'ఉష్ణోగ్రత',
        'humidity': 'తేమ',
        'rainfall': 'వర్షపాతం',
        'crop_recommendations': 'పంట సిఫార్సులు',
        'ask_question': 'మీ వ్యవసాయ ప్రశ్నను ఇక్కడ అడుగండి...',
        'send': 'సందేశం పంపండి',
        'quick_questions': 'త్వరిత ప్రశ్నలు',
        'weather_info': 'వాతావరణ సమాచారం',
        'crop_advice': 'పంట సలహా',
        'price_check': 'ధర తనిఖీ',
        'scheme_info': 'పథకం సమాచారం',
        'farming_tips': 'వ్యవసాయ చిట్కాలు',
        'pest_control': 'చీడపీడల నియంత్రణ'
    },
    'Malayalam': {
        'welcome': 'സ്വാഗതം',
        'app_name': 'കൃഷി സാരാംശ് - സ്മാർട്ട് കർഷക സഹായി',
        'description': 'ഇന്ത്യൻ കർഷകർക്കുള്ള AI-പവേർഡ് പ്ലാറ്റ്ഫോം',
        'weather': 'കാലാവസ്ഥ പ്രവചനം',
        'crop_planning': 'വിള ആസൂത്രണം',
        'market_prices': 'മാർക്കറ്റ് വിലകൾ',
        'govt_schemes': 'സർക്കാർ പദ്ധതികൾ',
        'ai_assistant': 'AI സഹായി',
        'profile': 'കർഷക പ്രൊഫൈൽ',
        'notifications': 'അറിയിപ്പുകൾ',
        'location': 'സ്ഥലം',
        'temperature': 'താപനില',
        'humidity': 'ആർദ്രത',
        'rainfall': 'മഴ',
        'crop_recommendations': 'വിള ശുപാർശകൾ',
        'ask_question': 'നിങ്ങളുടെ കൃഷി ചോദ്യം ഇവിടെ ചോദിക്കുക...',
        'send': 'സന്ദേശം അയയ്ക്കുക',
        'quick_questions': 'പെട്ടെന്നുള്ള ചോദ്യങ്ങൾ',
        'weather_info': 'കാലാവസ്ഥ വിവരം',
        'crop_advice': 'വിള ഉപദേശം',
        'price_check': 'വില പരിശോധന',
        'scheme_info': 'പദ്ധതി വിവരം',
        'farming_tips': 'കൃഷി നുറുങ്ങുകൾ',
        'pest_control': 'കീട നിയന്ത്രണം'
    },
    'Punjabi': {
        'welcome': 'ਸੁਆਗਤ ਹੈ',
        'app_name': 'ਕ੍ਰਿਸ਼ੀ ਸਾਰਾਂਸ਼ - ਸਮਾਰਟ ਕਿਸਾਨ ਸਹਾਇਕ',
        'description': 'ਭਾਰਤੀ ਕਿਸਾਨਾਂ ਲਈ AI-ਸੰਚਾਲਿਤ ਪਲੇਟਫਾਰਮ',
        'weather': 'ਮੌਸਮ ਪੂਰਵ ਅਨੁਮਾਨ',
        'crop_planning': 'ਫਸਲ ਯੋਜਨਾ',
        'market_prices': 'ਮਾਰਕਿਟ ਕੀਮਤਾਂ',
        'govt_schemes': 'ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ',
        'ai_assistant': 'AI ਸਹਾਇਕ',
        'profile': 'ਕਿਸਾਨ ਪ੍ਰੋਫਾਈਲ',
        'notifications': 'ਸੂਚਨਾਵਾਂ',
        'location': 'ਸਥਾਨ',
        'temperature': 'ਤਾਪਮਾਨ',
        'humidity': 'ਨਮੀ',
        'rainfall': 'ਬਾਰਿਸ਼',
        'crop_recommendations': 'ਫਸਲ ਸਿਫਾਰਸ਼ਾਂ',
        'ask_question': 'ਆਪਣਾ ਖੇਤੀਬਾੜੀ ਸਵਾਲ ਇੱਥੇ ਪੁੱਛੋ...',
        'send': 'ਸੁਨੇਹਾ ਭੇਜੋ',
        'quick_questions': 'ਤੁਰੰਤ ਸਵਾਲ',
        'weather_info': 'ਮੌਸਮ ਜਾਣਕਾਰੀ',
        'crop_advice': 'ਫਸਲ ਸਲਾਹ',
        'price_check': 'ਕੀਮਤ ਜਾਂਚ',
        'scheme_info': 'ਯੋਜਨਾ ਜਾਣਕਾਰੀ',
        'farming_tips': 'ਖੇਤੀਬਾੜੀ ਟਿਪਸ',
        'pest_control': 'ਕੀੜੇ ਨਿਯੰਤਰਣ'
    }
}

def get_text(key):
    """Get translated text based on selected language"""
    return TRANSLATIONS[st.session_state.selected_language].get(key, key)

# Enhanced sample data functions
def get_weather_data(city):
    """Enhanced weather data simulation"""
    temp = random.randint(18, 38)
    humidity = random.randint(35, 85)
    rainfall = random.randint(0, 15)
    
    return {
        'temperature': temp,
        'humidity': humidity,
        'rainfall': rainfall,
        'wind_speed': random.randint(5, 25),
        'pressure': random.randint(1010, 1025),
        'uv_index': random.randint(1, 11),
        'description': random.choice(['Sunny', 'Partly Cloudy', 'Rainy', 'Cloudy', 'Overcast']),
        'forecast': [
            {'day': 'Today', 'temp': temp, 'humidity': humidity, 'desc': 'Sunny', 'rain': rainfall},
            {'day': 'Tomorrow', 'temp': temp+2, 'humidity': humidity-5, 'desc': 'Cloudy', 'rain': rainfall+2},
            {'day': 'Day 3', 'temp': temp-3, 'humidity': humidity+10, 'desc': 'Rainy', 'rain': rainfall+8},
            {'day': 'Day 4', 'temp': temp+1, 'humidity': humidity-2, 'desc': 'Sunny', 'rain': rainfall-1},
            {'day': 'Day 5', 'temp': temp-1, 'humidity': humidity+3, 'desc': 'Partly Cloudy', 'rain': rainfall+3}
        ]
    }

def get_market_prices():
    """Enhanced market prices with trends"""
    base_prices = {
        'Rice (धान)': 2100, 'Wheat (गेहूं)': 2050, 'Cotton (कपास)': 5800, 
        'Sugarcane (गन्ना)': 350, 'Onion (प्याज)': 25, 'Potato (आलू)': 18,
        'Tomato (टमाटर)': 35, 'Maize (मक्का)': 1850, 'Soybean (सोयाबीन)': 4200
    }
    
    markets = ['APMC Delhi', 'APMC Mumbai', 'APMC Ahmedabad', 'APMC Lucknow', 'APMC Nashik', 'APMC Hyderabad']
    
    prices = []
    for crop, base_price in base_prices.items():
        change_pct = random.randint(-10, 15)
        current_price = base_price + (base_price * change_pct / 100)
        prices.append({
            'crop': crop,
            'price': f'₹{current_price:,.0f}/quintal' if current_price > 100 else f'₹{current_price}/kg',
            'change': f'+{change_pct}%' if change_pct > 0 else f'{change_pct}%',
            'market': random.choice(markets),
            'trend': 'up' if change_pct > 0 else 'down'
        })
    
    return prices

def get_government_schemes():
    """Enhanced government schemes"""
    return [
        {
            'name': 'PM-KISAN (पीएम-किसान)',
            'description': '₹6,000 annual income support to farmers',
            'eligibility': 'All landholding farmers',
            'benefit': '₹6,000/year in 3 installments',
            'application': 'Online/CSC/Bank',
            'status': 'Active'
        },
        {
            'name': 'Pradhan Mantri Fasal Bima Yojana',
            'description': 'Comprehensive crop insurance scheme',
            'eligibility': 'All farmers growing notified crops',
            'benefit': 'Up to 90% premium subsidy',
            'application': 'Banks/Insurance companies',
            'status': 'Active'
        },
        {
            'name': 'Kisan Credit Card (KCC)',
            'description': 'Easy credit access for farmers',
            'eligibility': 'Farmers with land records',
            'benefit': 'Low-interest agriculture loans (4% interest)',
            'application': 'Banks/Cooperative societies',
            'status': 'Active'
        },
        {
            'name': 'PM Kisan Samman Nidhi',
            'description': 'Income support for small farmers',
            'eligibility': 'Small and marginal farmers',
            'benefit': '₹6,000 per year',
            'application': 'Online portal',
            'status': 'Active'
        },
        {
            'name': 'Soil Health Card Scheme',
            'description': 'Soil testing and recommendations',
            'eligibility': 'All farmers',
            'benefit': 'Free soil testing and fertilizer recommendations',
            'application': 'Agriculture offices',
            'status': 'Active'
        }
    ]

def get_crop_recommendations(season, soil_type, location, user_preferences=None):
    """Enhanced crop recommendations"""
    recommendations = {
        'Kharif': {
            'Alluvial': ['Rice', 'Maize', 'Cotton', 'Sugarcane', 'Bajra'],
            'Clay': ['Rice', 'Wheat', 'Cotton', 'Gram'],
            'Sandy': ['Bajra', 'Groundnut', 'Castor', 'Sesame'],
            'Loamy': ['Rice', 'Maize', 'Cotton', 'Sugarcane', 'Soybean'],
            'Black Cotton': ['Cotton', 'Soybean', 'Sunflower', 'Jowar']
        },
        'Rabi': {
            'Alluvial': ['Wheat', 'Barley', 'Gram', 'Mustard', 'Peas'],
            'Clay': ['Wheat', 'Gram', 'Lentil', 'Mustard'],
            'Sandy': ['Barley', 'Gram', 'Mustard', 'Cumin'],
            'Loamy': ['Wheat', 'Barley', 'Gram', 'Mustard', 'Peas'],
            'Black Cotton': ['Wheat', 'Gram', 'Safflower', 'Coriander']
        },
        'Zaid': {
            'Alluvial': ['Watermelon', 'Cucumber', 'Fodder crops', 'Maize'],
            'Clay': ['Fodder crops', 'Vegetables'],
            'Sandy': ['Watermelon', 'Muskmelon', 'Fodder crops'],
            'Loamy': ['Watermelon', 'Cucumber', 'Vegetables', 'Fodder crops'],
            'Black Cotton': ['Fodder crops', 'Vegetables']
        }
    }
    
    base_recommendations = recommendations.get(season, {}).get(soil_type, ['Rice', 'Wheat', 'Cotton'])
    
    return base_recommendations[:5]  # Return top 5 recommendations

def get_farming_tips():
    """Get farming tips based on season and location"""
    tips = [
        "🌱 Start preparing your fields early for better crop yield",
        "💧 Install drip irrigation system to save 40-60% water",
        "🐛 Use neem-based pesticides for organic pest control",
        "🌿 Practice crop rotation to maintain soil health",
        "📊 Monitor market prices regularly before selling",
        "🚜 Maintain your farm equipment regularly",
        "🌾 Use certified seeds for better germination",
        "🧪 Get soil testing done every 2-3 years",
        "📱 Use mobile apps for weather updates",
        "👥 Join farmer producer organizations for better prices"
    ]
    return random.sample(tips, 3)

def get_pest_control_info():
    """Get pest control information"""
    pests = [
        {
            'name': 'Aphids',
            'crops': 'Cotton, Wheat, Mustard',
            'symptoms': 'Yellowing leaves, sticky honeydew',
            'control': 'Neem oil spray, ladybird beetles'
        },
        {
            'name': 'Bollworm',
            'crops': 'Cotton, Tomato',
            'symptoms': 'Holes in fruits/bolls',
            'control': 'Bt cotton, pheromone traps'
        },
        {
            'name': 'Stem Borer',
            'crops': 'Rice, Sugarcane',
            'symptoms': 'Dead hearts, white ears',
            'control': 'Trichogramma release, proper water management'
        }
    ]
    return pests

def get_ai_response(user_input):
    """Generate AI response based on user input"""
    responses = {
        "weather": "The weather in your area is favorable for farming activities with moderate temperatures and expected rainfall.",
        "crop": "Based on your soil type and season, I recommend growing wheat and mustard this season.",
        "price": "Current market prices for wheat are around ₹2,050 per quintal with an upward trend.",
        "scheme": "You may be eligible for the PM-KISAN scheme which provides ₹6,000 per year to farmers.",
        "pest": "For pest control, consider using neem-based pesticides which are effective and eco-friendly."
    }
    
    if "weather" in user_input.lower():
        return responses["weather"]
    elif "crop" in user_input.lower():
        return responses["crop"]
    elif "price" in user_input.lower():
        return responses["price"]
    elif "scheme" in user_input.lower():
        return responses["scheme"]
    elif "pest" in user_input.lower():
        return responses["pest"]
    else:
        return "I'm here to help with your farming queries. Please ask me about weather, crops, prices, government schemes, or pest control."

# Main Application UI
def main():
    # Header Section
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('app_name')}</h1>
        <h3>{get_text('description')}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Language Selector
    st.sidebar.title("Settings")
    st.session_state.selected_language = st.sidebar.selectbox(
        "Select Language",
        ["English", "Hindi", "Tamil", "Telugu", "Malayalam", "Punjabi"],
        index=["English", "Hindi", "Tamil", "Telugu", "Malayalam", "Punjabi"].index(st.session_state.selected_language)
    )
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_text('weather'),
        get_text('crop_planning'),
        get_text('market_prices'),
        get_text('govt_schemes'),
        get_text('ai_assistant')
    ])
    
    with tab1:
        # Weather Tab
        st.header(f"🌦️ {get_text('weather')}")
        weather_data = get_weather_data(st.session_state.user_location['city'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="weather-card">
                <h3>🌡️ {get_text('temperature')}</h3>
                <h2>{weather_data['temperature']}°C</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="weather-card">
                <h3>💧 {get_text('humidity')}</h3>
                <h2>{weather_data['humidity']}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="weather-card">
                <h3>🌧️ {get_text('rainfall')}</h3>
                <h2>{weather_data['rainfall']} mm</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Weather Forecast Chart
        forecast_df = pd.DataFrame(weather_data['forecast'])
        fig = px.line(forecast_df, x='day', y='temp', title='5-Day Temperature Forecast',
                     labels={'day': 'Day', 'temp': 'Temperature (°C)'})
        fig.update_traces(line=dict(width=4))
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        # Crop Planning Tab
        st.header(f"🌱 {get_text('crop_planning')}")
        
        col1, col2 = st.columns(2)
        with col1:
            season = st.selectbox("Select Season", ["Kharif", "Rabi", "Zaid"])
        with col2:
            soil_type = st.selectbox("Select Soil Type", ["Alluvial", "Clay", "Sandy", "Loamy", "Black Cotton"])
        
        recommendations = get_crop_recommendations(season, soil_type, st.session_state.user_location)
        
        st.subheader(f"📋 {get_text('crop_recommendations')}")
        for crop in recommendations:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{crop}</h3>
                <p>Ideal for {season} season in {soil_type} soil conditions</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Farming Tips
        st.subheader("💡 Farming Tips")
        tips = get_farming_tips()
        for tip in tips:
            st.markdown(f"""
            <div class="info-card">
                <p>{tip}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Market Prices Tab
        st.header(f"📊 {get_text('market_prices')}")
        prices = get_market_prices()
        
        for price in prices:
            st.markdown(f"""
            <div class="price-card">
                <h3>{price['crop']}</h3>
                <p><strong>Price:</strong> {price['price']} ({price['change']})</p>
                <p><strong>Market:</strong> {price['market']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Government Schemes Tab
        st.header(f"🏛️ {get_text('govt_schemes')}")
        schemes = get_government_schemes()
        
        for scheme in schemes:
            st.markdown(f"""
            <div class="scheme-card">
                <h3>{scheme['name']}</h3>
                <p>{scheme['description']}</p>
                <p><strong>Eligibility:</strong> {scheme['eligibility']}</p>
                <p><strong>Benefit:</strong> {scheme['benefit']}</p>
                <p><strong>Status:</strong> {scheme['status']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        # AI Assistant Tab
        st.header(f"🤖 {get_text('ai_assistant')}")
        
        # Chat History
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <p><strong>You:</strong> {message['content']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <p><strong>Krishi Assistant:</strong> {message['content']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick Questions
        # Quick Questions
        st.subheader(get_text('quick_questions'))
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(get_text('weather_info')):
                user_input = "Tell me about the weather"
                response = get_ai_response(user_input)
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.experimental_rerun()

        with col2:
            if st.button(get_text('crop_advice')):
                user_input = "What crops should I grow?"
                response = get_ai_response(user_input)
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.experimental_rerun()

        with col3:
            if st.button(get_text('price_check')):
                user_input = "What are the current crop prices?"
                response = get_ai_response(user_input)
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.experimental_rerun()

        with col4:
            if st.button(get_text('scheme_info')):
                user_input = "Tell me about government schemes"
                response = get_ai_response(user_input)
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.experimental_rerun()

        # Custom user input
        user_input = st.text_input(get_text('ask_question'), key="user_query")
        if st.button(get_text('send')):
            if user_input.strip():
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                response = get_ai_response(user_input)
                st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                st.experimental_rerun() 


if __name__ == "__main__":
    main()



  