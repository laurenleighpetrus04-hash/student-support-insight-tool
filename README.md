# Student Support Insights Tool

## Overview

This is an MVP prototype that helps programme staff analyse learner support survey data.

## Features

- Load sample synthetic learner data
- Upload learner CSV data
- Validate missing values
- Validate duplicate learner IDs
- Validate confidence scores from 1 to 5
- Validate category values
- Show dashboard visualisations
- Calculate support-risk levels
- Generate data-driven insights
- Generate practical recommendations
- Download summary report
- Download cleaned dataset

## Tech Stack

- Python
- Streamlit
- pandas
- Plotly
- CSV

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_sample_data.py
streamlit run app.py