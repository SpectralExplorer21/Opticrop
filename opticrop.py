import streamlit as st
import random
import pandas as pd



soil_data = {
    "alluvial": {"ph": (6.5, 8.4), "temp": (20.1, 31.1), "moisture": (50, 75)},
    "black": {"ph": (6.5, 8.4), "temp": (15, 35), "moisture": (50, 75)},
    "red": {"ph": (5.5, 8.5), "temp": (20, 32), "moisture": (60, 80)},
    "laterite": {"ph": (4.5, 6.5), "temp": (22, 35), "moisture": (40, 60)},
    "arid": {"ph": (4.5, 6.5), "temp": (20, 32), "moisture": (40, 60)},
    "mountain": {"ph": (5.5, 7.5), "temp": (10, 24), "moisture": (60, 80)}
}

crop_data = {
    "alluvial": ["Rice", "Wheat", "Sugarcane"],
    "black": ["Cotton", "Soybean"],
    "red": ["Groundnut", "Millets"],
    "laterite": ["Tea", "Coffee"],
    "arid": ["Dates", "Millets"],
    "mountain": ["Potato", "Barley"]
}

crop_conditions = {
    "Rice": {"ph": (5.5, 7.0), "temp": (20, 35), "moisture": (70, 90)},
    "Wheat": {"ph": (6.0, 7.5), "temp": (15, 25), "moisture": (40, 60)},
    "Sugarcane": {"ph": (6.0, 8.0), "temp": (20, 35), "moisture": (60, 80)},
    "Cotton": {"ph": (5.5, 8.0), "temp": (21, 30), "moisture": (50, 70)},
    "Soybean": {"ph": (6.0, 7.5), "temp": (20, 30), "moisture": (50, 70)},
    "Groundnut": {"ph": (6.0, 7.0), "temp": (25, 30), "moisture": (40, 60)},
    "Millets": {"ph": (5.0, 7.5), "temp": (25, 35), "moisture": (30, 50)},
    "Tea": {"ph": (4.5, 6.0), "temp": (18, 30), "moisture": (70, 90)},
    "Coffee": {"ph": (6.0, 6.5), "temp": (15, 28), "moisture": (60, 80)},
    "Dates": {"ph": (6.0, 8.5), "temp": (25, 40), "moisture": (20, 40)},
    "Potato": {"ph": (5.0, 6.5), "temp": (15, 20), "moisture": (60, 80)},
    "Barley": {"ph": (6.0, 7.5), "temp": (12, 25), "moisture": (40, 60)}
}

if "page" not in st.session_state:
    st.session_state.page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

if "show_history" not in st.session_state:
    st.session_state.show_history = False



if st.session_state.page == "home":
    st.title("OptiCrop")
    st.header("Soil Analysis System")
    st.subheader("Gain real time insights about your crops")

    if st.button("Alluvial Soil"):
        st.session_state.page = "alluvial"

    if st.button("Black Soil"):
        st.session_state.page = "black"

    if st.button("Red Soil"):
        st.session_state.page = "red"

    if st.button("Laterite Soil"):
        st.session_state.page = "laterite"

    if st.button("Arid Soil"):
        st.session_state.page = "arid"

    if st.button("Mountain Soil"):
        st.session_state.page = "mountain"



else:

    def analyze(value, low, high, label):
        if value < low:
            st.warning(f"{label} too low")
        elif value > high:
            st.warning(f"{label} too high")
        else:
            st.success(f"{label} optimal")

    def calculate_score(pH, temp, moisture, ph_range, temp_range, moist_range):
        score = 0

        if ph_range[0] <= pH <= ph_range[1]:
            score += 33
        if temp_range[0] <= temp <= temp_range[1]:
            score += 33
        if moist_range[0] <= moisture <= moist_range[1]:
            score += 34
        return score

    def crop_score(pH, temp, moisture, ideal):
        score = 0

        if ideal["ph"][0] <= pH <= ideal["ph"][1]:
            score += 1
        if ideal["temp"][0] <= temp <= ideal["temp"][1]:
            score += 1
        if ideal["moisture"][0] <= moisture <= ideal["moisture"][1]:
            score += 1

        return score

    soil = st.session_state.page
    data = soil_data[soil]

    ph_low, ph_high = data["ph"]
    temp_low, temp_high = data["temp"]
    moist_low, moist_high = data["moisture"]

    st.title(f"{soil.capitalize()} Soil Analysis")

    sensor_mode = st.toggle("Enable Sensor Mode")

    if sensor_mode:
        pH = round(random.uniform(4.5, 8.5), 2)
        moisture = round(random.uniform(30, 90), 2)
        temp = round(random.uniform(10, 40), 2)

        st.write(f"Sensor pH: {pH}")
        st.write(f"Sensor Moisture: {moisture}")
        st.write(f"Sensor Temperature: {temp}")

  
        weather = random.choice(["Sunny", "Rainy", "Cloudy"])
        st.write(f"Current Weather: {weather}")

        if weather == "Rainy":
            moisture += 5
        elif weather == "Sunny":
            moisture -= 5

    else:
        pH = st.number_input("pH", 0.0, 14.0)
        moisture = st.number_input("Moisture", 0.0, 100.0)
        temp = st.number_input("Temperature", 0.0, 50.0)

    if st.button("Analyze Soil"):

        score = calculate_score(pH, temp, moisture,
                        (ph_low, ph_high),
                        (temp_low, temp_high),
                        (moist_low, moist_high))

        st.subheader("Soil Score")
        st.progress(score)

        if score > 80:
            st.success("Excellent Soil ")
        elif score > 50:
            st.warning("Moderate Soil ️")
        else:
            st.error("Poor Soil ")
        analyze(pH, ph_low, ph_high, "pH")
        analyze(temp, temp_low, temp_high, "Temperature")
        analyze(moisture, moist_low, moist_high, "Moisture")

        st.session_state.history.append({
            "soil": soil,
            "pH": pH,
            "temperature": temp,
            "moisture": moisture
        })

    if st.button("Recommend Crops"):
        st.subheader("Smart Crop Ranking")

        results = []

        for crop in crop_data[soil]:
            score = crop_score(pH, temp, moisture, crop_conditions[crop.strip()])
            results.append((crop, score))

        results.sort(key=lambda x: x[1], reverse=True)

        for crop, score in results:
            if score == 3:
                st.success(f"{crop} → Highly Suitable ")
            elif score == 2:
                st.warning(f"{crop} → Moderately Suitable")
            else:
                st.error(f"{crop} → Not Recommended")

    if st.button("Back"):
        st.session_state.page = "home"

    
    if st.button("Show History"):
        st.session_state.show_history = True

    if st.session_state.show_history:

        if len(st.session_state.history) == 0:
            st.warning("No data available yet")

        else:
            df = pd.DataFrame(st.session_state.history)

            st.subheader("Soil Data History")
            st.dataframe(df)

            st.subheader("Soil Trends")
            st.line_chart(df[["pH", "temperature", "moisture"]])

            selected_soil = st.selectbox("Filter by Soil Type", df["soil"].unique())
            filtered_df = df[df["soil"] == selected_soil]

            st.line_chart(filtered_df[["pH", "temperature", "moisture"]])

            if len(filtered_df) > 1:
                latest = filtered_df.iloc[-1]
                previous = filtered_df.iloc[-2]

                st.subheader("Soil Health Trend")

                if latest["pH"] > previous["pH"]:
                    st.write(" pH increasing")
                elif latest["pH"] < previous["pH"]:
                    st.write(" pH decreasing")

                if latest["moisture"] > previous["moisture"]:
                    st.write(" Moisture increasing")
                elif latest["moisture"] < previous["moisture"]:
                    st.write(" Moisture decreasing")

                soil_latest = latest["soil"]
                soil_info = soil_data[soil_latest]

                ph_l, ph_h = soil_info["ph"]
                t_l, t_h = soil_info["temp"]
                m_l, m_h = soil_info["moisture"]

                score = 0

                if ph_l <= latest["pH"] <= ph_h:
                    score += 1
                if t_l <= latest["temperature"] <= t_h:
                    score += 1
                if m_l <= latest["moisture"] <= m_h:
                    score += 1

                st.subheader("Soil Health Score")

                if score == 3:
                    st.success("Excellent Soil Health ")
                elif score == 2:
                    st.warning("Moderate Soil Health")
                else:
                    st.error("Poor Soil Health")

            else:
                st.info("Not enough data to analyze trends yet")


            st.subheader("Prediction Engine")

            trend = 0

            if latest["pH"] > previous["pH"]:
                trend += 1
            elif latest["pH"] < previous["pH"]:
                trend -= 1

            if latest["moisture"] > previous["moisture"]:
                trend += 1
            elif latest["moisture"] < previous["moisture"]:
                 trend -= 1

            if latest["temperature"] > previous["temperature"]:
                trend -= 1  
            else:
                trend += 1

            if trend > 0:
                st.success("Soil condition improving ")
            elif trend < 0:
                st.error("Soil condition degrading ")
            else:
                st.info("Soil condition stable ")

            st.subheader("Smart Recommendations")

            if pH < ph_low:
                st.write(" Add lime to increase pH")
            elif pH > ph_high:
                st.write(" Add organic compost to reduce alkalinity")

            if moisture < moist_low:
                st.write(" Increase irrigation")
            elif moisture > moist_high:
                st.write(" Improve drainage")

            if temp > temp_high:
                st.write(" Use mulching to reduce heat")
            elif temp < temp_low:
                st.write(" Use greenhouse / cover crops")
            for entry in st.session_state.history:
                st.write(
                    f"{entry['soil']} | pH: {entry['pH']} | Temp: {entry['temperature']} | Moisture: {entry['moisture']}"
                )
        






    
        
                 
