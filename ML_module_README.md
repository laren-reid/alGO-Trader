# Machine Learning Module – Algorithmic Trading System

## Overview

This module is the machine learning component of an algorithmic trading system. It takes historical stock market data (provided as a Pandas DataFrame from a separate data-fetching module) and processes it to generate predictive signals for future price movement.

The module is designed to be independent from the UI, data acquisition, and trading execution layers. Its only responsibility is to transform financial data into predictions using machine learning.

---

## What the Module Does

- Receives stock market data as a Pandas DataFrame  
- Engineers technical features such as moving averages, momentum, volatility, and returns  
- Trains a supervised learning model (Random Forest Classifier)  
- Predicts whether the next-day stock price will go up or down  
- Outputs a prediction along with a confidence score  
- Includes a simple backtesting function to evaluate performance on historical data  

---

## Input Format

The module expects data in the following format:
Open, High, Low, Close, Volume

This data is provided externally by a Data Fetcher module (Yahoo Finance API component).

---

## Machine Learning Approach

The model uses a Random Forest Classifier to perform binary classification:

- `1` → Price will go up  
- `0` → Price will go down  

### Features used:
- Simple Moving Averages (SMA10, SMA20)  
- Momentum  
- Volatility  
- Daily returns  

The model is trained on historical labeled price movements.

---

## Output

The prediction output includes:

```json
{
  "prediction": 1,
  "confidence": 0.73
}
