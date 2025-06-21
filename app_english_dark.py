def main():
    st.write('✅ App started successfully')
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌾 Krishi Saaransh 🌾</h1>
        <h3>भारतीय किसानों के लिए स्मार्ट AI सहायक</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🌐 Language / भाषा")
        st.session_state.selected_language = st.selectbox(
            "Select Language / भाषा चुनें:",
            ['English'],
            index=['English'].index(st.session_state.selected_language)
        )
        
        st.header("📍 Location / स्थान")
        city = st.text_input("City / शहर:", value=st.session_state.user_location['city'])
        state = st.selectbox("State / राज्य:", 
                           ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 
                            'Telangana', 'Kerala', 'Punjab', 'Haryana', 'Uttar Pradesh', 
                            'West Bengal', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Bihar'])
        
        if st.button("Update Location / स्थान अपडेट करें"):
            st.session_state.user_location = {'city': city, 'state': state}
            st.success(f"Location updated to {city}, {state}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"🌤️ {get_text('weather')}", 
        f"🌱 {get_text('crop_planning')}", 
        f"💰 {get_text('market_prices')}", 
        f"🏛️ {get_text('govt_schemes')}", 
        f"🤖 {get_text('ai_assistant')}"
    ])
    
    # Weather Tab
    with tab1:
        st.subheader(f"🌤️ {get_text('weather')} - {st.session_state.user_location['city']}")
        
        weather_data = get_weather_data(st.session_state.user_location['city'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"{get_text('temperature')}", f"{weather_data['temperature']}°C")
        with col2:
            st.metric(f"{get_text('humidity')}", f"{weather_data['humidity']}%")
        with col3:
            st.metric(f"{get_text('rainfall')}", f"{weather_data['rainfall']}mm")
        with col4:
            st.metric("Status", weather_data['description'])
        
        # Weather forecast chart
        forecast_df = pd.DataFrame(weather_data['forecast'])
        fig = px.line(forecast_df, x='day', y='temp', title='5-Day Temperature Forecast',
                     markers=True, line_shape='spline')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Weather alerts
        if weather_data['rainfall'] > 5:
            st.warning("⚠️ Heavy rainfall expected. Protect your crops!")
        elif weather_data['temperature'] > 35:
            st.warning("🌡️ High temperature alert. Ensure proper irrigation!")
    
    # Crop Planning Tab
    with tab2:
        st.subheader(f"🌱 {get_text('crop_planning')}")
        
        col1, col2 = st.columns(2)
        with col1:
            season = st.selectbox("Season / मौसम:", ['Kharif', 'Rabi', 'Zaid'])
            soil_type = st.selectbox("Soil Type / मिट्टी का प्रकार:", 
                                   ['Alluvial', 'Clay', 'Sandy', 'Loamy', 'Black Cotton'])
        
        with col2:
            area = st.number_input("Land Area (acres) / भूमि क्षेत्र:", min_value=0.1, value=1.0)
            irrigation = st.selectbox("Irrigation / सिंचाई:", ['Rain Fed', 'Drip', 'Sprinkler', 'Flood'])
        
        if st.button(f"Get {get_text('crop_recommendations')} / फसल सुझाव पाएं"):
            recommendations = get_crop_recommendations(season, soil_type, st.session_state.user_location['city'])
            
            st.success(f"**Recommended Crops for {season} Season:**")
            for crop in recommendations:
                st.markdown(f"🌾 **{crop}**")
            
            # Create a simple crop planning chart
            crop_data = pd.DataFrame({
                'Crop': recommendations,
                'Expected Yield (tons/acre)': [2.5, 1.8, 3.2, 2.1, 1.5][:len(recommendations)],
                'Market Price (₹/quintal)': [2100, 5800, 350, 2050, 1800][:len(recommendations)]
            })
            
            fig = px.bar(crop_data, x='Crop', y='Expected Yield (tons/acre)', 
                        title='Expected Yield by Crop')
            st.plotly_chart(fig, use_container_width=True)
    
    # Market Prices Tab
    with tab3:
        st.subheader(f"💰 {get_text('market_prices')}")
        
        price_data = get_market_prices()
        
        for item in price_data:
            change_color = "green" if "+" in item['change'] else "red"
            st.markdown(f"""
            <div class="price-card">
                <h4>{item['crop']}</h4>
                <p><strong>Price:</strong> {item['price']}</p>
                <p><strong>Change:</strong> <span style="color: {change_color};">{item['change']}</span></p>
                <p><strong>Market:</strong> {item['market']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Price trend chart
        price_trend = pd.DataFrame({
            'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
            'Rice Price': [2000 + i*2 + (i%5)*10 for i in range(30)],
            'Wheat Price': [1950 + i*1.5 + (i%3)*8 for i in range(30)]
        })
        
        fig = px.line(price_trend, x='Date', y=['Rice Price', 'Wheat Price'], 
                     title='30-Day Price Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    # Government Schemes Tab
    with tab4:
        st.subheader(f"🏛️ {get_text('govt_schemes')}")
        
        schemes = get_government_schemes()
        
        for scheme in schemes:
            st.markdown(f"""
            <div class="scheme-card">
                <h4>{scheme['name']}</h4>
                <p><strong>Description:</strong> {scheme['description']}</p>
                <p><strong>Eligibility:</strong> {scheme['eligibility']}</p>
                <p><strong>Benefit:</strong> {scheme['benefit']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 **Tip:** Visit your nearest CSC (Common Service Center) or bank for scheme registration")
    
    # AI Assistant Tab
    with tab5:
        st.subheader(f"🤖 {get_text('ai_assistant')}")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Krishi AI:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(get_text('ask_question'), height=100,
                                    placeholder="Type your farming question here...")
            submitted = st.form_submit_button(get_text('send'))
            
            if submitted and user_input:
                # Add user message to history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # Generate AI response
                response = ai_response(user_input, st.session_state.selected_language)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
        
        # Quick action buttons
        st.markdown("**Quick Questions:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Weather Info / मौसम जानकारी"):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': 'What is today\'s weather?'
                })
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response('weather', st.session_state.selected_language)
                })
                st.rerun()
        
        with col2:
            if st.button("Crop Advice / फसल सलाह"):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': 'What crops should I grow?'
                })
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response('crop', st.session_state.selected_language)
                })
import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import time

# Page configuration
st.set_page_config(
    page_title="Krishi Saaransh",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile responsiveness and Indian theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF9933 0%, #FFFAF0 50%, #138808 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1e3c1e 0%, #2e2f3e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #138808;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .weather-card {
        background: linear-gradient(135deg, #1e2b3e 0%, #2f3e4f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .price-card {
        background: linear-gradient(135deg, #2e2e2e 0%, #3e3e3e 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF9933;
    }
    
    .scheme-card {
        background: linear-gradient(135deg, #2a2a40 0%, #3a3a50 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4169E1;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background-color: #DCF8C6;
        border-left: 4px solid #25D366;
    }
    
    .bot-message {
        background-color: #F1F1F1;
        border-left: 4px solid #128C7E;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            font-size: 0.9rem;
        }
        .feature-card, .weather-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'
if 'user_location' not in st.session_state:
    st.session_state.user_location = {'city': 'Delhi', 'state': 'Delhi'}

# Language translations
TRANSLATIONS = {
    'Hindi': {
        'welcome': 'स्वागत है',
        'app_name': 'कृषि सारांश - स्मार्ट किसान सहायक',
        'description': 'भारतीय किसानों के लिए AI-संचालित प्लेटफॉर्म',
        'weather': 'मौसम पूर्वानुमान',
        'crop_planning': 'फसल योजना',
        'market_prices': 'बाजार मूल्य',
        'govt_schemes': 'सरकारी योजनाएं',
        'ai_assistant': 'AI सहायक',
        'location': 'स्थान',
        'temperature': 'तापमान',
        'humidity': 'आर्द्रता',
        'rainfall': 'वर्षा',
        'crop_recommendations': 'फसल सुझाव',
        'ask_question': 'अपना प्रश्न पूछें',
        'send': 'भेजें'
    },
    'English': {
        'welcome': 'Welcome',
        'app_name': 'Krishi Saaransh - Smart Farmer Assistant',
        'description': 'AI-Powered Platform for Indian Farmers',
        'weather': 'Weather Forecast',
        'crop_planning': 'Crop Planning',
        'market_prices': 'Market Prices',
        'govt_schemes': 'Government Schemes',
        'ai_assistant': 'AI Assistant',
        'location': 'Location',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'rainfall': 'Rainfall',
        'crop_recommendations': 'Crop Recommendations',
        'ask_question': 'Ask your question',
        'send': 'Send'
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
        'location': 'இடம்',
        'temperature': 'வெப்பநிலை',
        'humidity': 'ஈரப்பதம்',
        'rainfall': 'மழைப்பொழிவு',
        'crop_recommendations': 'பயிர் பரிந்துரைகள்',
        'ask_question': 'உங்கள் கேள்வியைக் கேளுங்கள்',
        'send': 'அனுப்பு'
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
        'location': 'స్థానం',
        'temperature': 'ఉష్ణోగ్రత',
        'humidity': 'తేమ',
        'rainfall': 'వర్షపాతం',
        'crop_recommendations': 'పంట సిఫార్సులు',
        'ask_question': 'మీ ప్రశ్న అడుగండి',
        'send': 'పంపు'
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
        'location': 'സ്ഥലം',
        'temperature': 'താപനില',
        'humidity': 'ആർദ്രത',
        'rainfall': 'മഴ',
        'crop_recommendations': 'വിള ശുപാർശകൾ',
        'ask_question': 'നിങ്ങളുടെ ചോദ്യം ചോദിക്കുക',
        'send': 'അയയ്ക്കുക'
    }
}

def get_text(key):
    return TRANSLATIONS[st.session_state.selected_language].get(key, key)

# Sample data functions (In production, these would connect to real APIs)
def get_weather_data(city):
    """Simulate weather data - In production, use OpenWeatherMap API"""
    import random
    return {
        'temperature': random.randint(20, 35),
        'humidity': random.randint(40, 80),
        'rainfall': random.randint(0, 10),
        'description': random.choice(['Sunny', 'Partly Cloudy', 'Rainy', 'Cloudy']),
        'forecast': [
            {'day': 'Today', 'temp': random.randint(20, 35), 'desc': 'Sunny'},
            {'day': 'Tomorrow', 'temp': random.randint(20, 35), 'desc': 'Cloudy'},
            {'day': 'Day 3', 'temp': random.randint(20, 35), 'desc': 'Rainy'},
            {'day': 'Day 4', 'temp': random.randint(20, 35), 'desc': 'Sunny'},
            {'day': 'Day 5', 'temp': random.randint(20, 35), 'desc': 'Partly Cloudy'}
        ]
    }

def get_market_prices():
    """Simulate market prices - In production, use AgriMarket API"""
    return [
        {'crop': 'Rice (धान)', 'price': '₹2,100/quintal', 'change': '+5%', 'market': 'APMC Delhi'},
        {'crop': 'Wheat (गेहूं)', 'price': '₹2,050/quintal', 'change': '+2%', 'market': 'APMC Mumbai'},
        {'crop': 'Cotton (कपास)', 'price': '₹5,800/quintal', 'change': '-3%', 'market': 'APMC Ahmedabad'},
        {'crop': 'Sugarcane (गन्ना)', 'price': '₹350/quintal', 'change': '+1%', 'market': 'APMC Lucknow'},
        {'crop': 'Onion (प्याज)', 'price': '₹25/kg', 'change': '+15%', 'market': 'APMC Nashik'}
    ]

def get_government_schemes():
    """Government schemes for farmers"""
    return [
        {
            'name': 'PM-KISAN (पीएम-किसान)',
            'description': '₹6,000 annual income support to farmers',
            'eligibility': 'All landholding farmers',
            'benefit': '₹6,000/year in 3 installments'
        },
        {
            'name': 'Crop Insurance (फसल बीमा)',
            'description': 'Pradhan Mantri Fasal Bima Yojana',
            'eligibility': 'All farmers growing notified crops',
            'benefit': 'Compensation for crop loss'
        },
        {
            'name': 'Kisan Credit Card (किसान क्रेडिट कार्ड)',
            'description': 'Easy credit access for farmers',
            'eligibility': 'Farmers with land records',
            'benefit': 'Low-interest agriculture loans'
        },
        {
            'name': 'Soil Health Card (मृदा स्वास्थ्य कार्ड)',
            'description': 'Soil testing and recommendations',
            'eligibility': 'All farmers',
            'benefit': 'Free soil testing and fertilizer recommendations'
        }
    ]

def get_crop_recommendations(season, soil_type, location):
    """Crop recommendations based on conditions"""
    recommendations = {
        'Kharif': ['Rice', 'Cotton', 'Sugarcane', 'Maize', 'Bajra'],
        'Rabi': ['Wheat', 'Barley', 'Gram', 'Mustard', 'Peas'],
        'Zaid': ['Watermelon', 'Cucumber', 'Fodder crops', 'Sugarcane']
    }
    return recommendations.get(season, ['Rice', 'Wheat', 'Cotton'])

def ai_response(query, language):
    """Simulate AI response - In production, integrate with OpenAI/Gemini API"""
    responses = {
        'Hindi': {
            'weather': 'आज का मौसम साफ है। तापमान 28°C है और 70% आर्द्रता है। खेती के लिए अच्छा दिन है।',
            'crop': 'इस मौसम में गेहूं, चना और सरसों की बुवाई अच्छी होगी। मिट्टी की जांच कराएं।',
            'price': 'आज के बाजार भाव: गेहूं ₹2050/क्विंटल, धान ₹2100/क्विंटल। कल से दाम बढ़ सकते हैं।',
            'scheme': 'PM-KISAN योजना के तहत ₹6000 सालाना मिलता है। आधार कार्ड से रजिस्ट्रेशन कराएं।'
        },
        'English': {
            'weather': 'Today\'s weather is clear with 28°C temperature and 70% humidity. Good day for farming activities.',
            'crop': 'This season is good for wheat, gram, and mustard cultivation. Get your soil tested first.',
            'price': 'Today\'s market rates: Wheat ₹2050/quintal, Rice ₹2100/quintal. Prices may rise tomorrow.',
            'scheme': 'Under PM-KISAN scheme, you get ₹6000 annually. Register with your Aadhaar card.'
        },
        'Tamil': {
            'weather': 'இன்றைய வானிலை தெளிவாக உள்ளது. வெப்பநிலை 28°C மற்றும் 70% ஈரப்பதம். விவசாயத்திற்கு நல்ல நாள்.',
            'crop': 'இந்த பருவத்தில் கோதுமை, கடலை மற்றும் கடுகு பயிரிடுவது நல்லது. முதலில் மண் பரிசோதனை செய்யுங்கள்.',
            'price': 'இன்றைய சந்தை விலைகள்: கோதுமை ₹2050/குவிண்டால், அரிசி ₹2100/குவிண்டால். நாளை விலை உயரலாம்.',
            'scheme': 'PM-KISAN திட்டத்தின் கீழ் ஆண்டுக்கு ₹6000 கிடைக்கும். ஆதார் கார்டு மூலம் பதிவு செய்யுங்கள்.'
        },
        'Telugu': {
            'weather': 'నేటి వాతావరణం మంచిది. ఉష్ణోగ్రత 28°C మరియు 70% తేమ ఉంది. వ్యవసాయానికి మంచి రోజు.',
            'crop': 'ఈ సీజన్‌లో గోధుమలు, శనగలు మరియు ఆవాల పండించడం మంచిది. మొదట మట్టి పరీక్ష చేయండి.',
            'price': 'నేటి మార్కెట్ రేట్లు: గోధుమలు ₹2050/క్వింటల్, వరి ₹2100/క్వింటల్. రేపు ధరలు పెరుగుతాయి.',
            'scheme': 'PM-KISAN పథకంలో సంవత్సరానికి ₹6000 లభిస్తుంది. ఆధార్ కార్డుతో రిజిస్టర్ చేసుకోండి.'
        },
        'Malayalam': {
            'weather': 'ഇന്നത്തെ കാലാവസ്ഥ വ്യക്തമാണ്. താപനില 28°C ഉം 70% ആർദ്രതയും ഉണ്ട്. കൃഷിയ്ക്ക് നല്ല ദിവസം.',
            'crop': 'ഈ സീസണിൽ ഗോതമ്പ്, ചെറുപയർ, കടുക് എന്നിവ കൃഷി ചെയ്യാം. ആദ്യം മണ്ണ് പരിശോധന നടത്തുക.',
            'price': 'ഇന്നത്തെ വിപണി നിരക്കുകൾ: ഗോതമ്പ് ₹2050/ക്വിന്റൽ, അരി ₹2100/ക്വിന്റൽ. നാളെ വില കൂടാം.',
            'scheme': 'PM-KISAN പദ്ധതിയിൽ വർഷത്തിൽ ₹6000 കിട്ടും. ആധാർ കാർഡ് ഉപയോഗിച്ച് രജിസ്റ്റർ ചെയ്യുക.'
        }
    }
    
    # Simple keyword matching for demo
    query_lower = query.lower()
    lang_responses = responses.get(language, responses['English'])
    
    if any(word in query_lower for word in ['weather', 'मौसम', 'वाතावरण', 'వాతావరణం', 'കാലാവസ്ഥ']):
        return lang_responses['weather']
    elif any(word in query_lower for word in ['crop', 'फसल', 'பயிर்', 'పంట', 'വിള']):
        return lang_responses['crop']
    elif any(word in query_lower for word in ['price', 'मूल्य', 'விலை', 'ధర', 'വില']):
        return lang_responses['price']
    elif any(word in query_lower for word in ['scheme', 'योजना', 'திட்டம்', 'పథకం', 'പദ്ധതി']):
        return lang_responses['scheme']
    else:
        return lang_responses['weather']  # Default response

if __name__ == "__main__":
    main()
