# lahore-air-quality-forecast-project
# Lahore Air Forecast

<p align="center">

### **Predicting Lahore's Air. Understanding Tomorrow.**

An end-to-end machine learning project that forecasts **Lahore's PM2.5 air pollution for the next 3 days** and translates predictions into understandable **AQI categories and health guidance**.

<br>

[![Live Website](https://img.shields.io/badge/Live_Website-Lahore_Air_Forecast-00C896?style=for-the-badge)](https://lahoreairforecast.wixstudio.com/dashboard)
[![Machine Learning](https://img.shields.io/badge/Machine_Learning-Random_Forest-3776AB?style=for-the-badge)](https://scikit-learn.org/)
[![Built With](https://img.shields.io/badge/Built_With-Python-FFD43B?style=for-the-badge\&logo=python\&logoColor=3776AB)](https://www.python.org/)
[![Website](https://img.shields.io/badge/Website-Wix_Studio-0C6EFC?style=for-the-badge)](https://www.wix.com/studio)

</p>

---

## What is Lahore Air Forecast?

**Lahore Air Forecast** is a machine learning powered air quality forecasting project built around one simple question:

> **What might Lahore's air look like over the next few days?**

Air pollution is not just a number on a monitoring station. It can influence whether someone goes for a morning run, sends their children outside to play, opens their windows, commutes through the city, or decides to stay indoors.

This project uses historical **PM2.5 concentrations** and weather conditions to predict upcoming air quality.

The predictions are then converted into familiar **AQI categories**, making the results easier to understand for people who do not have a technical background.

### The goal

**Turn environmental data into predictions, and predictions into information people can actually use.**

---

## Live Website

### [Lahore Air Forecast](https://lahoreairforecast.wixstudio.com/dashboard)

The website provides:

* Current and forecast air quality information
* 3 day air quality predictions
* PM2.5 based air quality interpretation
* AQI categories
* Health recommendations
* Information about Lahore's air pollution
* An accessible interface designed for everyday users

---

# How It Works

The project follows a complete machine learning pipeline:

```text
                 HISTORICAL DATA
                        |
                        v
              +-------------------+
              |   Data Cleaning   |
              |   & Preparation   |
              +---------+---------+
                        |
                        v
              +-------------------+
              | Feature Selection |
              |                   |
              | PM2.5             |
              | Temperature       |
              | Relative Humidity |
              | Wind Speed        |
              | Wind Direction    |
              +---------+---------+
                        |
                        v
              +-------------------+
              |   Random Forest   |
              |     Regression    |
              +---------+---------+
                        |
                        v
                PM2.5 PREDICTIONS
                   Day 1 to Day 3
                        |
                        v
              +-------------------+
              |    AQI Mapping    |
              |                   |
              | PM2.5 -> AQI      |
              +---------+---------+
                        |
                        v
              +-------------------+
              |  Health Guidance  |
              +---------+---------+
                        |
                        v
                    WEBSITE
```

---

# Machine Learning

The forecasting system uses a **Random Forest Regressor**.

Random Forest was selected because it can model nonlinear relationships between environmental variables while remaining relatively robust and practical for this type of project.

## Input Features

The model uses five environmental variables:

| Feature            | Description                 |
| ------------------ | --------------------------- |
| `pm25`             | Current PM2.5 concentration |
| `temperature`      | Temperature                 |
| `relativehumidity` | Relative humidity           |
| `wind_speed`       | Wind speed                  |
| `wind_direction`   | Wind direction              |

The project intentionally keeps the feature set compact rather than using every available variable.

---

## Model Configuration

```python
RandomForestRegressor(
    n_estimators=50,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
```

### Why Random Forest?

* Handles nonlinear relationships
* Combines multiple decision trees
* Relatively robust to noisy environmental data
* Reasonably fast to train
* Provides a strong baseline for future experimentation
* Works well with environmental features

---

# Forecast Horizon

The system produces forecasts for three future days:

```text
Tomorrow
   |
   v
Day 2
   |
   v
Day 3
```

Each predicted PM2.5 value is interpreted through an AQI framework so users receive a meaningful category rather than only a raw numerical prediction.

---

# Model Evaluation

The final models were evaluated independently across the three forecast horizons.

| Forecast Day |       MAE |      RMSE |         R2 |
| ------------ | --------: | --------: | ---------: |
| Day 1        | **16.06** | **21.89** | **-0.049** |
| Day 2        | **18.70** | **24.12** | **-0.273** |
| Day 3        | **18.57** | **23.90** | **-0.255** |

## What do these numbers mean?

### MAE

**Mean Absolute Error** measures the average absolute difference between predicted and actual PM2.5 values.

### RMSE

**Root Mean Squared Error** gives greater weight to larger prediction errors.

### R2

**R2, or the coefficient of determination**, measures how well the model explains variation in the target compared with a baseline.

The evaluation highlights an important characteristic of environmental forecasting:

> **Predicting air pollution several days into the future is inherently difficult.**

Weather changes, emissions, atmospheric conditions, seasonal effects, and other factors can cause pollution levels to shift rapidly.

Rather than hiding these limitations, this project treats them as part of the forecasting problem and as opportunities for future improvement.

---

# Why PM2.5?

PM2.5 refers to fine particulate matter with a diameter of 2.5 micrometers or smaller.

These particles are small enough to penetrate deep into the respiratory system, making PM2.5 one of the most important indicators when discussing air pollution and human exposure.

For Lahore, PM2.5 is particularly relevant during periods of severe smog.

The project therefore uses PM2.5 as its primary forecasting target and translates the predictions into AQI categories to make the results easier to understand.

---

# Why Lahore?

Lahore experiences significant air pollution, particularly during the winter smog season.

Air quality can be influenced by a combination of factors including:

* Vehicle emissions
* Industrial activity
* Construction dust
* Crop residue burning
* Wind conditions
* Temperature
* Atmospheric conditions

This makes Lahore a meaningful real world environment for exploring short term air quality forecasting.

The project is intended to demonstrate how machine learning can be applied to an environmental issue that directly affects a local population.

---

# AQI Interpretation

The website translates predicted air quality into understandable categories.

|             AQI | Category                       | General Meaning                        |
| --------------: | ------------------------------ | -------------------------------------- |
|     **0 to 50** | Good                           | Little or no health risk               |
|   **51 to 100** | Moderate                       | Generally acceptable                   |
|  **101 to 150** | Unhealthy for Sensitive Groups | Sensitive individuals may be affected  |
|  **151 to 200** | Unhealthy                      | Everyone may experience health effects |
|  **201 to 300** | Very Unhealthy                 | Health effects become more widespread  |
| **300 to 500+** | Hazardous                      | Emergency level pollution              |

The website pairs these categories with practical recommendations so users do not have to interpret raw pollution measurements themselves.

---

# From Prediction to Action

The project is designed to go beyond producing a number.

Instead of simply showing:

```text
PM2.5 = 87.4
```

the system aims to communicate:

```text
UNHEALTHY FOR SENSITIVE GROUPS

Smog Risk: Moderate

Sensitive individuals should consider
reducing prolonged outdoor activity.
```

The overall process is:

```text
Prediction
    |
    v
PM2.5 concentration
    |
    v
AQI calculation
    |
    v
AQI category
    |
    v
Smog risk
    |
    v
Health recommendation
```

This turns a machine learning prediction into information that can be understood by a non technical audience.

---

# The Website

The frontend was created using **Wix Studio** with the goal of making the project approachable rather than presenting users with a wall of technical charts.

## Main Sections

### Home

An overview of Lahore's predicted air quality.

### AQI Forecast

The primary forecasting interface.

### Learn More

Background information about air pollution and the project.

### AQI Forecast Key

A visual interpretation of AQI ranges and recommended actions.

### Feedback

A place for users to provide feedback about the project.

---

# Project Structure

A simplified representation of the project workflow:

```text
Lahore-Air-Forecast/
|
+-- notebooks/
|   |
|   +-- 01_data_preparation
|   +-- 02_exploratory_analysis
|   +-- 03_model_training
|   +-- 04_model_evaluation
|
+-- models/
|   |
|   +-- day_1_model
|   +-- day_2_model
|   +-- day_3_model
|
+-- data/
|   |
|   +-- historical_air_quality_weather_data
|
+-- website/
|   |
|   +-- Wix Studio application
|
+-- README.md
```

---

# Development Journey

This project was built as an end to end machine learning workflow rather than simply training a model and stopping there.

### 01. Data

Historical air quality and weather information was collected and prepared.

### 02. Exploration

The data was explored to understand distributions, patterns, relationships, and potential predictive signals.

### 03. Feature Selection

A compact set of environmental variables was selected for the forecasting models.

### 04. Model Training

Separate Random Forest regression models were trained for the different forecast horizons.

### 05. Evaluation

The models were evaluated using:

* MAE
* RMSE
* R2

### 06. AQI Translation

Predicted pollution levels were converted into understandable AQI categories.

### 07. Website

The results were transformed into a public facing web experience.

---

# Limitations

No environmental forecasting model is perfect.

This project should be considered an **experimental forecasting and awareness tool**, not an official air quality monitoring or medical system.

Important limitations include:

* Forecast accuracy decreases as the prediction horizon increases.
* Air pollution can change rapidly because of weather and emission events.
* The model uses a relatively small feature set.
* Unexpected events may not be captured by historical patterns.
* Predictions should not replace official air quality measurements or public health guidance.

The negative R2 values for the longer forecast horizons also demonstrate that there is substantial room for improvement.

And that is part of the value of the project.

**A model does not have to be perfect to be useful, but it does have to be honest about its limitations.**

---

# Future Improvements

This project is designed to evolve.

## Possible Next Steps

* [ ] Incorporate more historical data
* [ ] Add additional meteorological variables
* [ ] Experiment with XGBoost and Gradient Boosting
* [ ] Explore time series architectures
* [ ] Add lagged pollution measurements
* [ ] Introduce rolling statistics
* [ ] Improve multi day forecasting
* [ ] Add confidence intervals
* [ ] Add real time data ingestion
* [ ] Automate model retraining
* [ ] Track predictions against actual pollution
* [ ] Add historical AQI visualizations
* [ ] Improve mobile experience
* [ ] Expand beyond Lahore

## Long Term Vision

With enough data and iteration, Lahore Air Forecast could evolve from a machine learning project into a more sophisticated **local environmental intelligence platform**.

The long term goal would be to make localized air quality information more accessible, understandable, and useful.

---

# Tech Stack

| Technology           | Purpose                           |
| -------------------- | --------------------------------- |
| **Python**           | Data science and machine learning |
| **Pandas**           | Data manipulation                 |
| **NumPy**            | Numerical computation             |
| **Matplotlib**       | Data visualization                |
| **Seaborn**          | Statistical visualization         |
| **Scikit-learn**     | Machine learning                  |
| **Random Forest**    | PM2.5 regression                  |
| **Jupyter Notebook** | Experimentation and analysis      |
| **Wix Studio**       | Public facing website             |

---

# Learning Outcomes

Building this project involved more than training a model.

It provided hands on experience with the complete machine learning workflow:

```text
Data
  |
  v
Cleaning
  |
  v
Exploration
  |
  v
Feature Selection
  |
  v
Model Training
  |
  v
Evaluation
  |
  v
Interpretation
  |
  v
Deployment
```

More importantly, the project demonstrated an important principle:

> **A model's job is not finished when it produces a prediction.**

The prediction needs to be evaluated, understood, communicated, and turned into something useful.

---

# Why This Project Matters

Air pollution is often discussed using numbers that can be difficult for everyday people to interpret.

This project attempts to bridge that gap.

Instead of asking users to understand:

```text
PM2.5 = 108.3 µg/m³
```

the system can communicate:

```text
UNHEALTHY

Smog Risk: Elevated

Consider reducing prolonged outdoor
activity and monitoring air quality.
```

That difference, from **data to understanding**, is at the heart of this project.

---

# Try It

## Lahore Air Forecast

### [Open the Live Website](https://lahoreairforecast.wixstudio.com/dashboard)

Explore the forecast, learn about Lahore's air quality, and see how machine learning can be applied to a real environmental problem.

---

# Disclaimer

**Lahore Air Forecast is an educational and experimental machine learning project.**

Predictions are estimates generated by a statistical model and should not be treated as official air quality measurements, emergency warnings, or medical advice.

For health related decisions, users should consult official air quality and public health sources.

---

# Author

### Imama Ahmad

Built as a machine learning and environmental awareness project focused on Lahore.


