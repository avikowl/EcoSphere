import streamlit as st
import base64
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
from geopy.distance import distance
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="EcoSphere", page_icon="icon.ico")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "D:/Carbon_footprint/carbon.jpg"
base64_img = get_base64_of_bin_file(img_path)

st.markdown(f"""
    <style>
        /* Background image */
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        /* Transparent background for selectboxes */
        .stSelectbox select {{
            background-color: transparent; /* Transparent background */
            color: #333; /* Text color */
        }}

        .stSelectbox div[role="listbox"] {{
            background-color: rgba(144, 238, 144, 0.3); /* Light Green */
        }}
    </style>
""", unsafe_allow_html=True)

page = st.selectbox("Navigate", ["Home", "Carbon Footprint Calculator", "Travel Recommendation", "Recent News", "Food choice", "Digital Footprint"])

def calculate_travel_emissions(distance_km, mode):
    EMISSION_FACTORS = {
        "flight": 0.25,    # kg CO2 per km for flights
        "car": 0.12,       # kg CO2 per km for car travel
        "bus": 0.05,       # kg CO2 per km for bus travel
        "bicycle": 0,      # no emissions for bicycles
        "train": 0.04,     # kg CO2 per km for train travel
        "electric_vehicle": 0.03,  # kg CO2 per km for electric vehicles
        "walking": 0       # no emissions for walking
    }
    return round(EMISSION_FACTORS.get(mode, 0) * distance_km / 1000, 2)  

def calculate_travel_time(distance_km, mode):
    SPEEDS = {
        "flight": 800,         # km/h for flights
        "car": 60,             # km/h for car
        "bus": 50,             # km/h for bus
        "bicycle": 15,         # km/h for bicycle
        "train": 100,          # km/h for train
        "electric_vehicle": 70,# km/h for electric vehicle
        "walking": 5           # km/h for walking
    }
    return round(distance_km / SPEEDS.get(mode, 1), 2) 

if page == "Home":
    st.title("Welcome to Your Sustainability Journey! 🌍")
    st.markdown("""
    ## Make Sustainability Simple, Fun, and Impactful 🌱
    Did you know that the average carbon footprint of a person in the United States is a staggering 16 tons, one of the highest rates in the world? In contrast, the global average is around 4 tons. Carbon emissions make up 60% of humanity's overall Ecological Footprint, and this is the fastest-growing component. The impact of our choices is undeniable. Food production alone accounts for 83% of global carbon emissions each year, and carbon dioxide is the most significant greenhouse gas, contributing to global warming by absorbing and re-radiating heat.
    
    The effects of carbon footprints are far-reaching: from harmful greenhouse gas emissions and depletion of natural resources to loss of biodiversity and soil degradation. But it’s not too late to make a difference. Every action you take to reduce your carbon footprint helps fight climate change and build a cleaner, healthier world for future generations.

    ### Key Features:
    - **Carbon Footprint Calculator**: Instantly measure your personal environmental impact and discover simple, actionable steps to reduce it.
    - **Travel Recommendations**: Explore eco-friendly travel options that allow you to enjoy the world while minimizing your carbon footprint.
    - **Sustainable Food Choices**: Make informed decisions about the food you eat, supporting both your health and the planet’s well-being.
    - **Recent News & Updates**: Stay inspired with the latest sustainability news and breakthroughs in climate action.

    ### Why Sustainability Matters:
    Every choice you make, from the food you eat to the way you travel, directly impacts the planet. By reducing your carbon footprint, you help mitigate the environmental effects of harmful emissions, conserve natural resources, and protect biodiversity. Together, we can turn small actions into significant change.

    ### Ready to Make an Impact?
    Embark on your sustainability journey today. With our tools and resources, you can start making eco-conscious decisions right away, helping create a greener future—one step at a time!
""")


elif page == "Carbon Footprint Calculator":
    st.title("Carbon Footprint Calculator")
    st.subheader("Your Country")
    
    EMISSION_FACTORS = {
        "India": {
            "Transportation": 0.14,  # kgCO2/km
            "Electricity": 0.82,     # kgCO2/KwH
            "Diet": 1.25,            # kgCO2/meal
            "Waste": 0.1             # kgCO2/kg
        },
        "US": {
            "Transportation": 0.21,  # kgCO2/km
            "Electricity": 0.5,      # kgCO2/KwH
            "Diet": 1.5,             # kgCO2/meal
            "Waste": 0.09            # kgCO2/kg
        },
        "China": {
            "Transportation": 0.14,  # kgCO2/km
            "Electricity": 0.72,     # kgCO2/KwH
            "Diet": 1.2,             # kgCO2/meal
            "Waste": 0.12            # kgCO2/kg
        },
        "Russia": {
            "Transportation": 0.22,  # kgCO2/km
            "Electricity": 0.58,     # kgCO2/KwH
            "Diet": 1.4,             # kgCO2/meal
            "Waste": 0.11            # kgCO2/kg
        },
        "European Union": {
            "Transportation": 0.16,  # kgCO2/km
            "Electricity": 0.3,      # kgCO2/KwH
            "Diet": 1.1,             # kgCO2/meal
            "Waste": 0.08            # kgCO2/kg
        }
    }

    country = st.selectbox("Select your country", ["India", "US", "China", "Russia", "European Union"])
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("House size (in square meters)")
        house_size = st.number_input("House size", min_value=0, max_value=1000, value=100, key="house_size_input")

        st.subheader("Daily water usage (in liters)")
        water_usage = st.number_input("Water usage", min_value=0, max_value=1000, value=200, key="water_usage_input")

        st.subheader("Daily air conditioning usage (in hours)")
        ac_usage = st.slider("Air conditioning usage", 0, 24, 4, key="ac_usage_input")

    with col2:
        st.subheader("Car mileage (in km per liter)")
        car_mileage = st.number_input("Car mileage", min_value=0.1, max_value=100.0, value=10.0, key="car_mileage_input")

        st.subheader("Annual car travel distance (in km)")
        car_distance = st.number_input("Car travel distance", min_value=0, max_value=50000, value=15000, key="car_distance_input")

        st.subheader("Waste generated per week (in kg)")
        waste = st.slider("Waste", 0.0, 100.0, key="waste_input")

        st.subheader("Number of meals per day")
        meals = st.number_input("Meals", 0, key="meals_input")

    car_distance = car_distance
    water_usage = water_usage * 365 if water_usage > 0 else 0
    ac_usage = ac_usage * 365 if ac_usage > 0 else 0

    transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * car_distance / car_mileage
    electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * water_usage / 1000 
    diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
    waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste
    house_emissions = house_size * 0.15  
    ac_emissions = ac_usage * 1.2 
    transportation_emissions = round(transportation_emissions / 1000, 2)
    electricity_emissions = round(electricity_emissions / 1000, 2)
    diet_emissions = round(diet_emissions / 1000, 2)
    waste_emissions = round(waste_emissions / 1000, 2)
    house_emissions = round(house_emissions / 1000, 2) 
    ac_emissions = round(ac_emissions / 1000, 2) 

    total_emissions = round(
        transportation_emissions + electricity_emissions + diet_emissions + waste_emissions +
        house_emissions + ac_emissions, 2
    )

    if st.button("Calculate CO2 Emissions"):
        st.session_state.transportation_emissions = transportation_emissions
        st.session_state.electricity_emissions = electricity_emissions
        st.session_state.diet_emissions = diet_emissions
        st.session_state.waste_emissions = waste_emissions
        st.session_state.house_emissions = house_emissions
        st.session_state.ac_emissions = ac_emissions
        st.session_state.total_emissions = total_emissions

    if "total_emissions" in st.session_state:
        st.header("Results")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Carbon Emissions by Categories")
            st.info(f"Transportation: {st.session_state.transportation_emissions} tonnes CO2 per year")
            st.info(f"Electricity: {st.session_state.electricity_emissions} tonnes CO2 per year")
            st.info(f"Diet: {st.session_state.diet_emissions} tonnes CO2 per year")
            st.info(f"Waste: {st.session_state.waste_emissions} tonnes CO2 per year")
            st.info(f"House size: {st.session_state.house_emissions} tonnes CO2 per year")
            st.info(f"Air conditioning: {st.session_state.ac_emissions} tonnes CO2 per year")

        with col4:
            st.subheader("Total Carbon Footprint")
            st.info(f"Total carbon footprint is: {st.session_state.total_emissions} tonnes CO2 per year")
            st.warning('''🌍 Emergency: Immediate Action Required!
            The current trajectory of your carbon emissions will further exacerbate climate change. If everyone lived like you, global temperatures would rise dangerously.
            It’s time to make changes in your lifestyle. Choose sustainable energy, reduce waste, and adopt eco-friendly habits. The future depends on you.''')

elif page == "Travel Recommendation":
    st.title("Travel Recommendation")

    origin = st.text_input("Enter your starting location (e.g., New York)")
    destination = st.text_input("Enter your destination (e.g., Los Angeles)")

    if st.button("Submit"):
        geolocator = Nominatim(user_agent="carbon_calculator_app")
        origin_location = geolocator.geocode(origin)
        destination_location = geolocator.geocode(destination)

        if origin_location and destination_location:
            distance_km = distance(
                (origin_location.latitude, origin_location.longitude),
                (destination_location.latitude, destination_location.longitude)
            ).km
            st.session_state.origin = origin
            st.session_state.destination = destination
            st.session_state.distance_km = round(distance_km, 2)
            travel_options = ["flight", "car", "bus", "bicycle", "train", "electric_vehicle", "walking"]
            emissions_info = {}
            time_info = {}
            for mode in travel_options:
                emissions = calculate_travel_emissions(distance_km, mode)
                time = calculate_travel_time(distance_km, mode)
                emissions_info[mode] = emissions
                time_info[mode] = time
            st.session_state.emissions_info = emissions_info
            st.session_state.time_info = time_info
            map_center = [(origin_location.latitude + destination_location.latitude) / 2,
                          (origin_location.longitude + destination_location.longitude) / 2]
            travel_map = folium.Map(location=map_center, zoom_start=5)
            folium.Marker([origin_location.latitude, origin_location.longitude],
                          tooltip="Starting Point", popup=origin).add_to(travel_map)
            folium.Marker([destination_location.latitude, destination_location.longitude],
                          tooltip="Destination", popup=destination).add_to(travel_map)
            folium.PolyLine([(origin_location.latitude, origin_location.longitude),
                             (destination_location.latitude, destination_location.longitude)],
                            color="blue", weight=2.5, opacity=0.8).add_to(travel_map)
            st.session_state.travel_map = travel_map

        else:
            st.error("Could not geocode one or both of the locations. Please check the entered addresses.")
    if "distance_km" in st.session_state:
        st.subheader("Travel Distance and Emissions")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Distance: {st.session_state.distance_km} km")

        with col2:
            st.info("Emission estimates and travel times:")
            for mode in st.session_state.emissions_info:
                emissions = st.session_state.emissions_info[mode]
                time = st.session_state.time_info[mode]
                st.info(f"{mode.capitalize()}: {emissions} tonnes CO2, Time: {time} hours")

    if "travel_map" in st.session_state:
        st.subheader("Map of the Journey")

        map_width = 1300 
        map_height = 600  

        st_folium(st.session_state.travel_map, width=map_width, height=map_height)

elif page == "Recent News":
    st.title("Recent News")

    api_url = "https://newsapi.org/v2/everything"
    api_key = "998065ae8b0543fdb0bdae02d38c663c"  
    query = "environment OR sustainability OR tourism OR climate"

    params = {
        "apiKey": api_key,
        "q": query,
        "language": "en",
        "pageSize": 25, 
        "sortBy": "publishedAt",
        "from": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") 
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("articles", [])
        displayed_urls = set() 

        if articles:
            for article in articles:
                url = article.get("url")
                if url in displayed_urls:
                    continue 
                displayed_urls.add(url)

                image_url = article.get("urlToImage")
                if image_url:
                    st.image(image_url, use_container_width=True)

                st.subheader(f"[{article.get('title')}]({url})")

                st.write(f"**Description**: {article.get('description', 'No Description available.')}")
                
                st.write(f"**Published on**: {article.get('publishedAt', 'No date available.')}")
                
                st.write("**Source**:", article.get("source", {}).get("name"))
                st.markdown("---") 

        else:
            st.info("No recent articles found.")
    else:
        st.error(f"Error fetching news articles: {response.json().get('message', 'Unknown error')}")

elif page == "Food choice":
    st.title("Food Choice")

    st.header("Sustainability Score for Food Items")

    protein_items = [
        {"name": "Tofu", "score": 8, "info": "Low environmental impact plant protein."},
        {"name": "Chicken", "score": 5, "info": "Lower impact than red meat."},
        {"name": "Lentils", "score": 9, "info": "High protein, low emissions."},
        {"name": "Tempeh", "score": 7, "info": "Sustainable soy-based protein."},
        {"name": "Eggs", "score": 6, "info": "Moderate impact, nutrient-dense."},
        {"name": "Pork", "score": 4, "info": "Higher impact than poultry."},
        {"name": "Fish", "score": 6, "info": "Varies based on sourcing."},
        {"name": "Beans", "score": 8, "info": "Low water and land use."},
        {"name": "Nuts", "score": 5, "info": "Water-intensive but high in protein."},
        {"name": "Turkey", "score": 6, "info": "Moderate impact, versatile."},
        {"name": "Quinoa", "score": 7, "info": "Low-impact ancient grain."},
    ]

    vegetable_items = [
        {"name": "Spinach", "score": 10, "info": "Highly sustainable leafy green."},
        {"name": "Tomatoes", "score": 9, "info": "Seasonal and moderate water use."},
        {"name": "Peppers", "score": 8, "info": "Low water usage, nutrient-rich."},
        {"name": "Carrots", "score": 8, "info": "Low impact, widely available."},
        {"name": "Broccoli", "score": 9, "info": "High nutrient density, low impact."},
        {"name": "Kale", "score": 10, "info": "Very sustainable, low water needs."},
        {"name": "Lettuce", "score": 7, "info": "Hydroponic options available."},
        {"name": "Cucumber", "score": 8, "info": "Low-impact, refreshing."},
        {"name": "Eggplant", "score": 8, "info": "Water-efficient, versatile."},
        {"name": "Zucchini", "score": 9, "info": "Low-impact, easy to grow."},
        {"name": "Cabbage", "score": 9, "info": "Long shelf life, low impact."},
        {"name": "Beetroot", "score": 8, "info": "High nutrient density."},
    ]

    carb_items = [
        {"name": "Rice", "score": 3, "info": "High water usage."},
        {"name": "Potatoes", "score": 6, "info": "Relatively low-impact."},
        {"name": "Sweet Potatoes", "score": 7, "info": "Lower water needs than potatoes."},
        {"name": "Quinoa", "score": 7, "info": "Low-impact ancient grain."},
        {"name": "Pasta", "score": 5, "info": "Moderate environmental impact."},
        {"name": "Bread", "score": 4, "info": "Varies by ingredients."},
        {"name": "Corn", "score": 6, "info": "Low water use and versatile."},
        {"name": "Oats", "score": 8, "info": "High in fiber, low impact."},
        {"name": "Barley", "score": 8, "info": "Sustainable grain option."},
        {"name": "Wheat", "score": 5, "info": "Varies based on farming practices."},
        {"name": "Millet", "score": 9, "info": "Low water requirements."},
        {"name": "Couscous", "score": 7, "info": "Low impact, wheat-based."},
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Proteins")
        for idx, item in enumerate(protein_items):
            if st.button(item["name"], key=f"protein_{idx}"):
                st.write(f"Sustainability Score: {item['score']}")
                st.write(item["info"])

    with col2:
        st.subheader("Vegetables and Fruits")
        for idx, item in enumerate(vegetable_items):
            if st.button(item["name"], key=f"veg_{idx}"):
                st.write(f"Sustainability Score: {item['score']}")
                st.write(item["info"])

    with col3:
        st.subheader("Carbohydrates")
        for idx, item in enumerate(carb_items):
            if st.button(item["name"], key=f"carb_{idx}"):
                st.write(f"Sustainability Score: {item['score']}")
                st.write(item["info"])

    st.header("Interactive Food Comparison Tool")
    comparison_data = {
        "Food": ["Tofu", "Chicken", "Spinach", "Rice", "Potatoes", "Quinoa", "Broccoli", "Pasta", "Bread"],
        "Carbon Footprint (kg CO2)": [0.7, 6.9, 0.3, 2.7, 0.5, 0.9, 0.4, 1.7, 1.2],
        "Water Usage (L)": [300, 4325, 200, 2500, 287, 460, 200, 290, 320],
        "Land Use (sq meters)": [1, 5, 0.4, 1.5, 0.3, 0.8, 0.2, 0.6, 0.4],
    }

    df = pd.DataFrame(comparison_data)

    food_options = df["Food"].unique()
    food1 = st.selectbox("Select first food to compare", food_options, index=0)
    food2 = st.selectbox("Select second food to compare", food_options, index=1)

    selected_data = df[df["Food"].isin([food1, food2])]

    fig, ax = plt.subplots(figsize=(6, 4))
    selected_data.plot(kind="bar", x="Food", y="Carbon Footprint (kg CO2)", ax=ax, color="#3498db", width=0.8)

    ax.set_title("Carbon Footprint Comparison", fontsize=14)
    ax.set_ylabel("Carbon Footprint (kg CO2)", fontsize=12)
    ax.set_xlabel("Food", fontsize=12)
    ax.tick_params(axis="x", rotation=0)

    st.pyplot(fig)
    st.header("Sustainable Recipes")

    recipes = [
        {"name": "Spicy Lentil Soup", "summary": "A hearty, protein-rich soup made with lentils, onions, garlic, tomatoes, and a mix of spices like cumin, turmeric, and coriander. Simmer the lentils until tender and blend for a creamy texture."},
        {"name": "Roasted Seasonal Vegetables", "summary": "Use local, seasonal veggies like carrots, potatoes, and cauliflower. Toss with olive oil, garlic, and herbs, then roast in the oven until crispy. Great as a side or main dish."},
        {"name": "Quinoa Salad with Herbs", "summary": "A refreshing salad with cooked quinoa, cherry tomatoes, cucumber, red onion, and parsley. Toss with lemon juice, olive oil, and a sprinkle of salt for a simple, nutritious meal."},
        {"name": "Stuffed Bell Peppers", "summary": "Stuff bell peppers with a mixture of cooked quinoa, black beans, corn, and spices. Roast in the oven for a filling and nutritious plant-based dish."},
        {"name": "Avocado Toast", "summary": "Top toasted whole-grain bread with mashed avocado, a squeeze of lemon, and a pinch of salt. Add a sprinkle of chili flakes for extra flavor."},
        {"name": "Sweet Potato & Black Bean Tacos", "summary": "Sauté cubed sweet potatoes and black beans with cumin and chili powder. Serve in corn tortillas with avocado, cilantro, and a squeeze of lime for a delicious taco."},
        {"name": "Vegan Mushroom Risotto", "summary": "Make a creamy risotto by cooking Arborio rice with vegetable broth, sautéed mushrooms, garlic, and onions. Stir until the rice is tender and creamy."},
        {"name": "Chickpea Stir-Fry", "summary": "Stir-fry chickpeas with your favorite vegetables like bell peppers, broccoli, and spinach. Add soy sauce, garlic, and ginger for flavor and serve over brown rice."},
        {"name": "Cauliflower Rice Bowl", "summary": "Grate cauliflower to make 'rice' and sauté with garlic and olive oil. Serve with sautéed vegetables, tofu, or tempeh for a low-carb, nutrient-dense meal."},
        {"name": "Eggplant Parmesan", "summary": "Bread and bake slices of eggplant, then layer with marinara sauce and vegan cheese. Bake until bubbly and golden for a hearty, plant-based alternative to traditional Parmesan."},
        {"name": "Grilled Vegetable Skewers", "summary": "Thread vegetables like zucchini, mushrooms, and peppers onto skewers. Grill with olive oil and herbs for a quick and delicious dish."},
        {"name": "Spinach and Chickpea Curry", "summary": "Cook spinach and chickpeas in a rich, spiced tomato curry sauce. Serve with rice or naan for a comforting, flavorful meal."},
        {"name": "Butternut Squash Soup", "summary": "Roast butternut squash and blend with vegetable broth, onions, garlic, and spices for a creamy, comforting soup perfect for cooler months."},
        {"name": "Tomato Basil Pasta", "summary": "Cook pasta and toss with a fresh tomato sauce made from ripe tomatoes, garlic, olive oil, and fresh basil. Simple, yet bursting with flavor."},
        {"name": "Zucchini Noodles with Pesto", "summary": "Spiralize zucchini into noodles and toss with a vegan pesto made from basil, garlic, pine nuts, and olive oil for a low-carb, fresh alternative to pasta."},
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        for idx, recipe in enumerate(recipes[:5]):
            if st.button(recipe["name"], key=f"recipe_{idx}"):
                st.write(recipe["summary"])

    with col2:
        for idx, recipe in enumerate(recipes[5:10]):
            if st.button(recipe["name"], key=f"recipe_{idx+5}"):
                st.write(recipe["summary"])

    with col3:
        for idx, recipe in enumerate(recipes[10:]):
            if st.button(recipe["name"], key=f"recipe_{idx+10}"):
                st.write(recipe["summary"])

elif page == "Digital Footprint":
    st.title("Digital Footprint")

    st.header("Your Digital Habits")
    col1, col2 = st.columns(2)
    with col1:
        device_type = st.selectbox("Select Device Type", ["Smartphone", "Laptop", "Desktop", "Tablet"])
        streaming_hours = st.slider("Streaming hours per week", min_value=0, max_value=168, step=1)
        social_hours = st.number_input("Social media hours per week", min_value=0, max_value=168, step=1)
    with col2:
        connection_type = st.selectbox("Select Internet Connection", ["Wi-Fi", "4G", "5G"])
        browsing_hours = st.slider("Browsing hours per week", min_value=0, max_value=168, step=1)
    
    st.header("Calculate Digital Carbon Footprint")
    co2_streaming = streaming_hours * 0.12
    co2_social = social_hours * 0.05
    co2_browsing = browsing_hours * 0.03
    total_co2 = co2_streaming + co2_social + co2_browsing

    device_factors = {"Smartphone": 1.0, "Laptop": 1.5, "Desktop": 2.0, "Tablet": 1.2}
    connection_factors = {"Wi-Fi": 1.0, "4G": 1.5, "5G": 2.0}
    device_factor = device_factors[device_type]
    connection_factor = connection_factors[connection_type]
    adjusted_total_co2 = total_co2 * device_factor * connection_factor

    st.write(f"**Your Total Carbon Footprint:** {adjusted_total_co2:.2f} kg CO₂ per week")

    st.write("### Recommendations")
    st.write("- Reduce streaming quality to save data.")
    st.write("- Set daily limits for social media use.")
    st.write("- Unsubscribe from unused cloud services.")

    st.header("Compare with Average User")
    avg_co2 = 2.5
    percentage_diff = ((adjusted_total_co2 - avg_co2) / avg_co2) * 100
    comparison = "above" if adjusted_total_co2 > avg_co2 else "below"
    st.write(f"Your footprint is **{abs(percentage_diff):.2f}% {comparison}** the average user.")
    
    data = pd.DataFrame({"Source": ["Your Footprint", "Average User"], 
                         "CO₂ Emissions (kg)": [adjusted_total_co2, avg_co2]})
    fig, ax = plt.subplots()
    ax.bar(data["Source"], data["CO₂ Emissions (kg)"], color=["#4CAF50", "#FFC107"])
    ax.set_facecolor("none")
    ax.set_ylabel("CO₂ Emissions (kg)")
    st.pyplot(fig)

    st.header("Carbon Offset Options")
    st.write(f"To offset your footprint, you’d need to plant around **{adjusted_total_co2 * 0.05:.2f} trees**.")
    st.write("Other Options:")
    st.write("- Donate to renewable energy projects.")
    st.write("- Support reforestation initiatives.")
    st.write("[Offset your footprint online](https://www.carbonfootprint.com)")

    st.header("Set and Track Your Reduction Goals")
    st.write("Input your target limits for the next 6 months to reduce your footprint.")
    target_streaming = st.slider("Target streaming hours per week", 0, 168, int(streaming_hours * 0.85))
    target_social = st.slider("Target social media hours per week", 0, 168, int(social_hours * 0.85))
    target_browsing = st.slider("Target browsing hours per week", 0, 168, int(browsing_hours * 0.85))

    goal_total_co2 = (target_streaming * 0.12 + target_social * 0.05 + target_browsing * 0.03) * device_factor * connection_factor

    months = ["Current", "1 Month", "2 Months", "3 Months", "4 Months", "5 Months", "6 Months"]
    current_values = [adjusted_total_co2] * 7
    goal_values = [adjusted_total_co2] + [goal_total_co2 * (1 - 0.1 * i) for i in range(6)]

    reduction_data = pd.DataFrame({"Months": months, "Current CO₂": current_values, "Goal CO₂": goal_values})

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0) 
    ax.set_facecolor("none") 

    ax.plot(months, reduction_data["Current CO₂"], label="Current CO₂", color="#FF5733", linestyle="--")
    ax.plot(months, reduction_data["Goal CO₂"], label="Goal CO₂", color="#4CAF50", linestyle="-")
    ax.fill_between(months, reduction_data["Current CO₂"], reduction_data["Goal CO₂"], color="lightgrey", alpha=0.3)

    for i, (curr, goal) in enumerate(zip(reduction_data["Current CO₂"], reduction_data["Goal CO₂"])):
        percentage_reduction = ((curr - goal) / curr) * 100 if curr != 0 else 0
        ax.text(i, goal + 0.05, f"{percentage_reduction:.1f}%", ha="center", fontsize=8, color="green")

    ax.set_xlabel("Months")
    ax.set_ylabel("CO₂ Footprint (kg)")
    ax.legend()

    st.pyplot(fig)


