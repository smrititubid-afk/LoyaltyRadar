# LoyaltyRadar: Recovery-Potential Driven Airline Loyalty Retention System

## Project Overview

LoyaltyRadar is an end-to-end customer retention analytics project built on airline loyalty data.
The project identifies behaviorally inactive customers, estimates loyalty value at risk, segments customers into actionable business groups, and recommends next-best retention actions.

Instead of only predicting churn, this project focuses on answering business questions:

* Which customers are at risk?
* How much loyalty value is at risk?
* Which customers should be prioritized?
* What action should the business take next?
* What is the estimated ROI of targeted retention campaigns?

## Business Problem

Airline loyalty programs often have thousands of customers, but not every inactive customer should receive the same campaign.
Some customers are high value and need personalized win-back offers, while others are better suited for low-cost automated campaigns.

The goal of this project is to build a practical retention system that helps a loyalty team prioritize customers based on risk, value, recovery potential, and recommended action.

## Dataset

The project uses airline loyalty and customer flight activity data.

Main data sources:

* Customer Loyalty History
* Customer Flight Activity
* Calendar Data
* Data Dictionary

The analysis is performed at customer-month and customer-level granularity.

## Project Pipeline

### 01 - Data Check and Cleaning

* Loaded raw loyalty, flight activity, and calendar data.
* Checked shapes, missing values, duplicates, and date ranges.
* Created a clean merged base dataset.
* Found that loyalty history starts earlier, but behavioral activity is available for 2017–2018.

### 02 - Basic EDA and Customer Behavior

* Aggregated duplicate customer-month records.
* Analyzed monthly flight activity, inactivity, redemption behavior, CLV, geography, and loyalty cards.
* Identified important customer behavior patterns:

  * Many customers have inactive months.
  * Recent 6-month inactivity is a strong churn signal.
  * Premium customers have high value but are not always more likely to churn.
  * Some customers collect points but redeem very little.

### 03 - Churn Label and Feature Engineering

* Created customer-level behavioral features.
* Built a behavioral churn label based on recent inactivity.
* Created business features such as:

  * CLV tier
  * Loyalty Value at Risk
  * Premium Drifter flag
  * Silent Risk group
  * Travel Break Risk
  * Seasonal Risk
  * Points Collector flag
* Created a retention priority score and priority bands.

### 04 - Leakage-Safe Model Training and Trust Layer

* Initially found near-perfect model performance, which indicated data leakage.
* Redesigned the modelling setup using a temporal split:

  * Observation period: Jan 2017 to Jun 2018
  * Target period: Jul 2018 to Dec 2018
* Trained leakage-safe Logistic Regression and Random Forest models.
* Selected Random Forest as the champion model because it achieved strong recall for churn detection.

Champion model results:

* Accuracy: 0.825
* Precision: 0.452
* Recall: 0.893
* F1-score: 0.600
* ROC-AUC: 0.897
* PR-AUC: 0.536

The top 20% highest-risk customers captured around 72.9% of churners.

### 05 - Segments, Recovery Scoring, and Next Best Actions

* Created interpretable customer segments:

  * Premium Drifter
  * Silent Risk
  * Travel Break Risk
  * Seasonal Risk
  * Points Collector at Risk
  * Healthy / Monitor
* Built a recovery potential score.
* Created recovery potential bands.
* Built a rule-based Next Best Action Engine.

Recommended actions include:

* Personalized premium win-back offer
* Early retention call or targeted offer
* Gentle re-engagement reminder
* Low-cost automated reactivation
* Travel pattern break alert with limited-time offer
* Seasonal timing reminder
* Points redemption nudge
* Monitor only

### 06 - Dashboard Data Prep and ROI Simulation

* Prepared dashboard-ready KPI tables.
* Created segment, action, geography, and province summaries.
* Built an assumption-based ROI simulator.
* Compared three strategies:

  * Do Nothing
  * Random Targeting
  * LoyaltyRadar Targeting

## Key Results

Total customers analyzed:

```text
16,737
```

Total CLV:

```text
133.71 million
```

Total Loyalty Value at Risk:

```text
20.06 million
```

Value at Risk Share:

```text
15%
```

Behaviorally churned customers:

```text
2,469
```

Premium Drifters:

```text
613 customers
10.57 million value at risk
52.67% of total value at risk
```

Silent Risk customers:

```text
727 customers
```

## Campaign ROI Simulation

The ROI simulation is assumption-based and should not be interpreted as actual campaign performance.

Under the current assumptions:

```text
Campaign customers: 2,469
Total campaign cost: 106,409
Expected recovered value: 2.59 million
Expected net value: 2.49 million
Overall ROI multiple: 24.37x
```

## Strategy Comparison

| Strategy               | Targeted Customers | Value at Risk Targeted | Expected Net Value | ROI Multiple |
| ---------------------- | -----------------: | ---------------------: | -----------------: | -----------: |
| Do Nothing             |                  0 |                      0 |                  0 |            0 |
| Random Targeting       |              2,469 |           2.92 million |       0.18 million |        4.73x |
| LoyaltyRadar Targeting |              2,469 |          20.06 million |       2.49 million |       24.37x |

LoyaltyRadar targets the same number of customers as random targeting but captures much more value at risk.

## Main Business Insights

* Premium Drifters are the most valuable retention segment.
* Silent Risk customers are useful for proactive retention because they are behaviorally inactive but not formally churned.
* Random targeting misses most of the high-value risk.
* Behavior-based targeting can produce stronger simulated ROI than random outreach.
* A retention system should not only predict churn but also recommend what action should be taken.

## Project Structure

```text
LoyaltyRadar/
│
├── notebooks/
│   ├── 01_data_check_and_cleaning.ipynb
│   ├── 02_basic_eda_and_customer_behavior.ipynb
│   ├── 03_churn_label_and_feature_engineering.ipynb
│   ├── 04_model_training_and_trust_layer.ipynb
│   ├── 05_segments_recovery_and_actions.ipynb
│   └── 06_dashboard_data_prep_and_roi.ipynb
│
├── dashboard/
│   └── data/
│
├── reports/
│   └── figures/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
│
└── README.md
```

## Important Note

The data files, processed outputs, and model files are not uploaded to GitHub because they may be large or private.
The repository focuses on the notebook workflow, methodology, analysis, and business results.

## Tools and Libraries

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Google Colab
* GitHub

## Final Outcome

LoyaltyRadar is a complete retention analytics workflow that moves from raw airline loyalty data to business-ready customer prioritization, campaign recommendations, and ROI simulation.

The project demonstrates:

* Data cleaning
* Exploratory data analysis
* Feature engineering
* Leakage-safe machine learning
* Customer segmentation
* Business rule design
* Dashboard data preparation
* ROI simulation

  ## Prototype

A Streamlit dashboard prototype is included in the `dashboard/` folder.

To run locally:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
