import json
from pathlib import Path
from datetime import datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import plotly.graph_objects as go

from forecast_engine import generate_forecast, aqi_details, FORECAST_FILE

st.set_page_config(
    page_title="Lahore Air Forecast",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --cream: #F5F1E8;
    --green: #243D35;
    --sage: #A8BBA5;
    --rose: #D9A6A0;
}

.stApp {
    background: #F5F1E8;
    color: #243D35;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: #F5F1E8 !important;
    height: 0 !important;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

#MainMenu, footer {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1320px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #243D35 !important;
    font-family: 'Playfair Display', serif !important;
}

p, li, label {
    color: #52645A;
}

.hero {
    background: linear-gradient(120deg, #263F36, #49685A);
    border-radius: 28px;
    padding: 55px 48px;
    color: #F5F1E8;
    margin-bottom: 25px;
    overflow: hidden;
}

.hero h1 {
    color: #F8F3E8 !important;
    font-size: clamp(38px, 6vw, 68px);
    line-height: 1.1;
}

.hero p {
    color: #DCE6D9;
    font-size: 16px;
    max-width: 650px;
}

.eyebrow {
    color: #D9A6A0;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    color: #243D35;
    margin: 25px 0 12px 0;
}

.card, .forecast-card {
    background: #FFFFFF;
    border: 1px solid #E5E5D9;
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 16px;
    box-shadow: 0 8px 25px rgba(40,60,45,.045);
}

.forecast-card {
    min-height: 300px;
}

.aqi-number {
    font-family: 'Playfair Display', serif;
    font-size: 55px;
    font-weight: 700;
    line-height: 1.2;
}

.small-label {
    color: #87968A;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.updated {
    background: #E8E9DD;
    color: #52645A;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    margin: 15px 0 22px 0;
}

.stButton button, .stLinkButton a {
    background: #243D35 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5E5D9;
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stMetricValue"] {
    color: #243D35;
}

hr {
    border-color: #DDE1D6;
}

.footer {
    text-align: center;
    padding: 35px 10px;
    color: #87968A;
    font-size: 12px;
}

.footer strong {
    color: #243D35;
    font-family: 'Playfair Display', serif;
    font-size: 22px;
}

@media(max-width:700px) {
    .hero { padding: 32px 23px; }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div style="font-family:Playfair Display,serif;
font-size:30px;font-weight:700;color:#243D35;padding-top:8px;">
Lahore Air Forecast
<div style="font-family:DM Sans,sans-serif;font-size:10px;
letter-spacing:3px;color:#8A9D88;text-transform:uppercase;">
Breathe aware · Live informed
</div></div>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* Elegant horizontal navigation */

[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: flex-start !important;
    gap: 32px !important;
    border-bottom: 1px solid #D9DFD3;
    padding: 12px 0 0 0;
    width: 100% !important;
}

[data-testid="stRadio"] label {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 10px 0 14px 0 !important;
    margin: 0 !important;
    flex: 0 0 auto !important;
    position: relative;
}

[data-testid="stRadio"] label p {
    color: #65786C !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
}

[data-testid="stRadio"] label:has(input:checked) {
    background: transparent !important;
}

[data-testid="stRadio"] label:has(input:checked) p {
    color: #243D35 !important;
    font-weight: 700 !important;
}

[data-testid="stRadio"] label:has(input:checked)::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: #A8BBA5;
    border-radius: 5px 5px 0 0;
}

[data-testid="stRadio"] input {
    display: none !important;
}

@media(max-width: 750px) {
    [data-testid="stRadio"] > div {
        gap: 16px !important;
        flex-wrap: wrap !important;
    }

    [data-testid="stRadio"] label p {
        font-size: 12px !important;
    }
}

</style>
""", unsafe_allow_html=True)

page = st.radio(
    "Navigation",
    ["Home", "Learn More", "Feedback", "Project", "Analytics", "GitHub"],
    horizontal=True,
    label_visibility="collapsed"
)

# Automatically refresh the dashboard every 5 minutes
st_autorefresh(
    interval=5 * 60 * 1000,
    key="dashboard_refresh"
)


# Automatically rerun the app every 15 minutes
st_autorefresh(
    interval=15 * 60 * 1000,
    key="lahore_forecast_auto_refresh"
)

st.markdown("---")



def hero(title, subtitle, eyebrow="AIR QUALITY • LAHORE, PAKISTAN"):
    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


COLOURS = {
    "green": "#319B76",
    "yellow": "#D3A92E",
    "orange": "#E88B43",
    "red": "#D94E55",
    "purple": "#9065B5",
    "black": "#45494D"
}

def get_forecast():
    if FORECAST_FILE.exists():
        return json.loads(
            FORECAST_FILE.read_text(encoding="utf-8")
        )
    return None


if page == "Home":

    hero(
        "Lahore Air Forecast",
        "A clearer picture of the air we breathe. Explore the next three days of predicted air quality and make informed decisions for your health."
    )

    data = get_forecast()

    if data is None:
        st.warning("Your first forecast has not been generated yet.")

        if st.button("Generate first forecast"):
            try:
                with st.spinner("Generating your Lahore forecast..."):
                    generate_forecast(force=True)
                st.rerun()
            except Exception as e:
                st.error(f"Forecast error: {e}")

    else:
        updated = datetime.fromisoformat(data["last_updated"])
        next_update = datetime.fromisoformat(data["next_update"])

        st.markdown(
            f"""<div class="updated">
            ◷ LAST UPDATED:
            <b>{updated.strftime('%d %B %Y · %I:%M %p PKT')}</b>
            &nbsp; | &nbsp;
            NEXT UPDATE:
            <b>{next_update.strftime('%d %B %Y · %I:%M %p PKT')}</b>
            </div>""",
            unsafe_allow_html=True
        )

        st.caption(
            "Experimental machine learning predictions. "
            "These are not official real-time AQI measurements "
            "and may differ from actual air quality."
        )

        forecasts = data["forecasts"]
        today = forecasts[0]

        category, risk, colour, advice = aqi_details(today["aqi"])
        accent = COLOURS[colour]

        st.markdown(
            '<div class="section-title">Today at a glance</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="card" style="border-left:8px solid {accent};">
            <div class="small-label">TODAY'S AIR QUALITY INDEX</div>
            <div class="aqi-number" style="color:{accent};">
                {today['aqi']}
            </div>
            <h2>{category}</h2>
            <p><b>Smog risk:</b> {risk}</p>
            <p>{advice}</p>
            <p class="small-label">
                PM₂.₅ CONCENTRATION: {today['pm25']} µg/m³
            </p>
        </div>
        """, unsafe_allow_html=True)


        st.markdown(
            '<div class="section-title">The days ahead</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(3)

        for i, item in enumerate(forecasts):
            category, risk, colour, advice = aqi_details(item["aqi"])
            date = datetime.strptime(item["date"], "%Y-%m-%d")

            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card"
                style="border-top:6px solid {COLOURS[colour]};">
                    <div class="small-label">DAY {i+1}</div>
                    <h3>{date.strftime('%A')}</h3>
                    <p>{date.strftime('%d %B %Y')}</p>
                    <div class="aqi-number"
                    style="color:{COLOURS[colour]};">
                    {item['aqi']}
                    </div>
                    <b>{category}</b>
                    <p>Smog risk: {risk}</p>
                    <p class="small-label">
                    PM₂.₅: {item['pm25']} µg/m³
                    </p>
                    <p>{advice}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">Three-day air quality trend</div>',
            unsafe_allow_html=True
        )

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[x["date"] for x in forecasts],
            y=[x["aqi"] for x in forecasts],
            mode="lines+markers+text",
            text=[str(x["aqi"]) for x in forecasts],
            textposition="top center",
            line=dict(color="#49685A", width=4),
            marker=dict(size=13, color="#D9A6A0")
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.7)",
            font_color="#243D35",
            yaxis_title="Air Quality Index",
            margin=dict(l=10,r=10,t=25,b=10)
        )

        st.plotly_chart(fig, use_container_width=True)


        if st.button("Refresh forecast now"):
            try:
                with st.spinner("Updating forecast..."):
                    generate_forecast(force=True)
                st.rerun()
            except Exception as e:
                st.error(str(e))

    st.markdown("""
    <div class="card">
    <div class="small-label">WHY IT MATTERS</div>
    <h2>Know your air. Protect your day.</h2>
    Lahore experiences significant air pollution, particularly during
    winter. Checking air quality before outdoor activities can help
    you make more informed decisions.
    </div>
    """, unsafe_allow_html=True)


elif page == "Learn More":

    hero(
        "Understanding AQI",
        "A little knowledge about the air can make a meaningful difference to your everyday health."
    )

    st.markdown(
        '<div class="section-title">What is AQI?</div>',
        unsafe_allow_html=True
    )

    st.write("""
    The Air Quality Index (AQI) is a standardized scale used to indicate
    how clean or polluted the air is. Higher AQI values represent poorer
    air quality and greater potential health risks. AQI is calculated
    using concentrations of common air pollutants, including particulate
    matter (PM₂.₅ and PM₁₀), ozone, nitrogen dioxide, sulfur dioxide,
    and carbon monoxide.
    """)

    st.markdown(
        '<div class="section-title">Other important terms</div>',
        unsafe_allow_html=True
    )

    with st.expander("What is Smog?"):
        st.write("""
        Smog is a type of air pollution caused by fine particles, smoke,
        dust, and harmful gases from vehicles, industries, and other sources.
        In winter, these pollutants can become trapped near the ground,
        reducing visibility and increasing health risks.
        """)

    with st.expander("What is PM₂.₅?"):
        st.write("""
        PM₂.₅ refers to tiny airborne particles with a diameter of
        2.5 micrometers or smaller. These particles are small enough to
        travel deep into the lungs and may even enter the bloodstream,
        increasing the risk of respiratory and cardiovascular diseases.
        """)


    st.markdown(
        '<div class="section-title">AQI Forecast Key</div>',
        unsafe_allow_html=True
    )

    bands = [
        ("Good", "0–50", "#319B76",
         "Enjoy outdoor activities as normal. No special precautions are needed."),

        ("Moderate", "51–100", "#D3A92E",
         "Sensitive individuals should reduce prolonged or intense outdoor activity if symptoms occur."),

        ("Unhealthy for Sensitive Groups", "101–150", "#E88B43",
         "Sensitive groups should limit outdoor activity, keep medication available if needed, and monitor symptoms."),

        ("Unhealthy", "151–200", "#D94E55",
         "Reduce prolonged outdoor activities, avoid strenuous exercise outdoors, and consider wearing a well-fitting N95 mask if spending extended time outside."),

        ("Very Unhealthy", "201–300", "#9065B5",
         "Stay indoors where possible, keep windows and doors closed, use an air purifier if available, and avoid unnecessary outdoor activities."),

        ("Hazardous", "301–500+", "#45494D",
         "Avoid outdoor activities unless absolutely necessary. Wear a high-quality mask if you must go outside and follow official public health advisories.")
    ]

    for name, value, colour, advice in bands:
        st.markdown(f"""
        <div class="card" style="border-left:7px solid {colour};">
            <h3>{name}</h3>
            <div class="small-label">AQI RANGE: {value}</div>
            <p>{advice}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">How to protect yourself</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Wear an N95 mask during heavy smog.
    - Limit outdoor activities when AQI is high.
    - Use an indoor air purifier if available.
    - Follow daily AQI forecasts before planning outdoor activities.
    """)

    st.markdown(
        '<div class="section-title">Health effects</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Eye irritation
    - Coughing
    - Difficulty breathing
    - Asthma attacks
    - Heart and cardiovascular problems
    - Higher health risks for children, older adults, and people with existing medical conditions.
    """)

    st.markdown(
        '<div class="section-title">Lahore’s air quality</div>',
        unsafe_allow_html=True
    )

    st.write("""
    Lahore frequently ranks among the world's most polluted cities,
    especially during the winter smog season. According to the World
    Air Quality Report 2024 by IQAir, Lahore recorded an annual average
    PM₂.₅ concentration of approximately 102 µg/m³, more than 20 times
    higher than the WHO annual guideline of 5 µg/m³.
    """)

    st.markdown(
        '<div class="section-title">References</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - [U.S. EPA – AQI](https://www.airnow.gov/aqi/)
    - [U.S. EPA – AQI Basics](https://www.airnow.gov/aqi/aqi-basics/)
    - [WHO – Ambient Air Pollution](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-pollution)
    - [OpenAQ](https://openaq.org/)
    - [Open-Meteo](https://open-meteo.com/)
    """)


elif page == "Feedback":

    hero(
        "Your voice matters",
        "Help make Lahore Air Forecast more useful. Your suggestions, observations and ideas are appreciated.",
        "FEEDBACK & COMMUNITY"
    )

    st.markdown(
        '<div class="section-title">Give your feedback</div>',
        unsafe_allow_html=True
    )

    st.write("""
    This section is dedicated to collecting feedback about the website
    and its air quality forecasting features. Suggestions, observations,
    and ideas can help improve how information is presented and make
    the platform more effective for users.
    """)

    feedback_url = (
        "https://docs.google.com/forms/d/e/"
        "1FAIpQLSdW7p1rDQNb8DtseIOhcRLnuEPO1aCdx6IQ1LRCUVmewuFwGA/"
        "viewform?usp=header"
    )

    st.link_button("Share your feedback ↗", feedback_url)

    st.components.v1.iframe(
        "https://docs.google.com/forms/d/e/"
        "1FAIpQLSdW7p1rDQNb8DtseIOhcRLnuEPO1aCdx6IQ1LRCUVmewuFwGA/"
        "viewform?embedded=true",
        height=850,
        scrolling=True
    )


elif page == "Project":

    hero(
        "Behind the forecast",
        "A machine learning project exploring how data can help us understand Lahore's air."
    )

    st.markdown(
        '<div class="section-title">About this project</div>',
        unsafe_allow_html=True
    )

    st.write("""
    This project was developed to demonstrate how machine learning can
    be applied to air quality forecasting. By combining historical PM₂.₅
    measurements with weather data from Lahore, Pakistan, the system
    predicts air quality for the next three days and presents the results
    through an interactive web dashboard.
    """)

    st.markdown(
        '<div class="section-title">Objectives</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Predict PM₂.₅ concentrations for the next three days.
    - Convert predictions into AQI values.
    - Provide understandable health recommendations.
    - Raise public awareness of air pollution in Lahore.
    - Demonstrate the practical application of machine learning in environmental monitoring.
    """)

    st.markdown(
        '<div class="section-title">Machine learning model</div>',
        unsafe_allow_html=True
    )

    st.write("""
    The forecasting system uses a Random Forest Regressor trained on
    historical air quality and weather data. The model predicts future
    PM₂.₅ concentrations using five input features before converting
    the results into AQI categories.
    """)

    st.markdown("""
    **Features used**
    - PM₂.₅
    - Temperature
    - Relative Humidity
    - Wind Speed
    - Wind Direction
    """)


    st.markdown(
        '<div class="section-title">Technologies used</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Python
    - Jupyter Notebook
    - Pandas
    - NumPy
    - Scikit-learn
    - Matplotlib
    - Joblib
    - Streamlit
    - Kaggle
    """)

    st.info(
        "The dataset downloaded from Kaggle for this project "
        "has been taken down by its owner and is no longer available."
    )

    st.markdown(
        '<div class="section-title">Future improvements</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    - Predict more than three days ahead.
    - Improve prediction accuracy using more advanced models.
    """)

    st.markdown(
        '<div class="section-title">Limitations</div>',
        unsafe_allow_html=True
    )

    st.write("""
    Forecast accuracy is limited, with evaluation results indicating
    that predictions may differ from actual PM2.5 levels, particularly
    over longer forecast horizons. The forecasting pipeline also needs
    validation against the original training notebooks.
    """)


elif page == "Analytics":

    hero(
        "The project in numbers",
        "A look back at the visitors and engagement recorded on the original Wix website.",
        "WEBSITE ANALYTICS"
    )

    st.caption(
        "Historical Wix statistics supplied by the project owner. "
        "These are not live Streamlit analytics."
    )

    cols = st.columns(5)

    metrics = [
        ("Page views", "143"),
        ("Site sessions", "82"),
        ("Unique visitors", "59"),
        ("Bounce rate", "62%"),
        ("Avg. duration", "2m 1s")
    ]

    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)

    rows = [
        ("25/10/2026",14,6,5,"83%","5m 50s"),
        ("20/10/2026",4,2,2,"50%","25s"),
        ("19/10/2026",1,1,1,"100%","Unknown"),
        ("18/10/2026",2,1,1,"0%","11s"),
        ("16/10/2026",1,1,1,"100%","Unknown"),
        ("13/10/2026",2,1,1,"0%","15s"),
        ("25/09/2026",3,1,1,"0%","22s"),
        ("18/09/2026",3,2,2,"100%","1s"),
        ("17/09/2026",3,1,1,"0%","3m 6s"),
        ("16/09/2026",1,1,1,"100%","Unknown"),
        ("13/09/2026",3,2,2,"50%","1m 24s"),
        ("09/09/2026",3,1,1,"0%","42s"),
        ("03/09/2026",2,1,1,"0%","5s"),
        ("02/09/2026",1,1,1,"100%","Unknown"),
        ("01/09/2026",4,2,2,"50%","9s"),
        ("31/08/2026",2,2,2,"100%","Unknown"),
        ("30/08/2026",60,41,39,"76%","3m 19s"),
        ("12/08/2026",6,2,2,"0%","1m 54s"),
        ("11/08/2026",8,6,6,"67%","18s"),
        ("10/08/2026",16,6,6,"33%","1m 6s"),
        ("09/08/2026",11,6,6,"50%","1m 18s"),
        ("08/08/2026",1,1,1,"100%","Unknown"),
        ("07/08/2026",4,1,1,"0%","2m 52s"),
        ("06/08/2026",1,1,1,"100%","Unknown"),
        ("05/08/2026",7,3,3,"33%","3m 35s"),
        ("04/08/2026",4,1,1,"0%","1m 22s")
    ]

    df = pd.DataFrame(rows, columns=[
        "Date", "Page views", "Site sessions",
        "Unique visitors", "Bounce rate", "Avg. session duration"
    ])

    st.markdown(
        '<div class="section-title">Historical visitor activity</div>',
        unsafe_allow_html=True
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = go.Figure(go.Bar(
        x=df["Date"],
        y=df["Page views"],
        marker_color="#789681"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.6)",
        font_color="#243D35",
        yaxis_title="Page views"
    )

    st.plotly_chart(fig, use_container_width=True)


elif page == "GitHub":

    hero(
        "Open source, open knowledge",
        "Explore the code, notebooks and machine learning work behind Lahore Air Forecast."
    )

    st.markdown(
        '<div class="section-title">Explore the repository</div>',
        unsafe_allow_html=True
    )

    st.write("""
    The complete source code for this project is available on GitHub!
    The repository includes machine learning models, data preprocessing,
    model training and evaluation notebooks, datasets, and the website
    implementation. It is provided to promote transparency, allow others
    to understand the project, and support future improvements or contributions.
    """)

    st.link_button(
        "Explore the GitHub repository ↗",
        "https://github.com/ImamaAhmad/lahore-air-quality-forecast-project/tree/main"
    )


st.markdown("---")

st.markdown("""
<div class="footer">
<strong>LAHORE AIR FORECAST</strong>
<br><br>
Breathe aware · Live informed
<br><br>
© 2026 by Imama Ahmad
</div>
""", unsafe_allow_html=True)

