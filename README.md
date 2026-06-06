# DataMind AI - Multi-Agent Data Analysis System

## Overview

DataMind AI is an intelligent multi-agent data analysis platform built using Python, Streamlit, Pandas, Plotly, and Scikit-Learn.

The system automatically processes datasets, cleans data, performs statistical analysis, generates insights, and creates interactive visualizations through a coordinated team of specialized AI agents.

## Features

*  Supports multiple file formats

  * CSV
  * Excel (XLS/XLSX)
  * JSON
  * PDF
  * DOCX
  * TXT

* Multi-Agent Architecture

  * File Detection Agent
  * Extraction Agent
  * Loading Agent
  * Understanding Agent
  * Cleaning Agent
  * Analysis Agent
  * Insight Agent
  * Visualization Agent

* Automatic Statistical Analysis

  * Descriptive statistics
  * Correlation analysis
  * Category frequency analysis
  * Trend detection

* Interactive Visualizations

  * Bar Charts
  * Line Charts
  * Pie Charts
  * Scatter Plots
  * Histograms
  * Area Charts
  * Box Plots
  * Correlation Heatmaps

* AI-Generated Insights

* Automated Data Cleaning

* Download Cleaned Dataset

---

## System Architecture

File Upload
↓
File Detection Agent
↓
Extraction Agent
↓
Loading Agent
↓
Understanding Agent
↓
Cleaning Agent
↓
Analysis Agent
↓
Insight Agent
↓
Visualization Agent
↓
Interactive Dashboard

---

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Scikit-Learn
* PDFPlumber
* Python-Docx
* OpenPyXL

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/datamind-ai.git
cd datamind-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

---

## Project Structure

```text
data-analysis-agents/
│
├── agents/
│   ├── file_detection_agent.py
│   ├── extraction_agent.py
│   ├── loading_agent.py
│   ├── understanding_agent.py
│   ├── cleaning_agent.py
│   ├── analysis_agent.py
│   ├── insight_agent.py
│   ├── visualization_agent.py
│   └── manager_agent.py
│
├── ui/
│   └── styles.py
│
├── utils/
│   └── helpers.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Key Capabilities

### Data Cleaning

* Missing value handling
* Duplicate removal
* Data type correction
* Column standardization

### Statistical Analysis

* Mean
* Median
* Standard Deviation
* Correlation Analysis
* Category Distribution

### Trend Analysis

* Time-series aggregation
* Monthly trend detection
* Performance monitoring

### Visualization

* Automatic chart generation
* Custom chart builder
* Correlation heatmaps
* Interactive dashboards

---

## Future Enhancements

* Machine Learning Predictions
* Natural Language Querying
* Advanced Forecasting Models
* Database Integration
* Cloud Deployment

---

## Author

Bhupathi Geeth Praneeth

Developed during a Hackathon as an AI-powered Multi-Agent Data Analysis Platform.
