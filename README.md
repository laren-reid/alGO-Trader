# ML Module

## Overview

This module provides stock market prediction functionality for the Algorithmic Trading System.

Features:
- Feature engineering
- Model training
- Prediction generation
- Backtesting

## Dataset Format

CSV files should be stored in:

data/

Example:

Date,Open,High,Low,Close,Volume

## Usage

Train model:

```python
from ml_pipeline import MLPipeline

ml = MLPipeline()
ml.train_model("AAPL")
