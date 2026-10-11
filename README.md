# US Wildfires Machine Learning Project

## Overview
Machine Learning project using the "1.88 Million US Wildfires" Kaggle dataset.

## Objectives
1. Cause Classification: Predict the cause of the fire (lightning, arson, accident) based on location, date, and initial size.
2. Size Classification: Estimate the final fire size class (A to G) using only discovery data.
3. Duration Regression: Predict fire duration (discovery to containment) based on region and season.

## Structure
- `data/`: Raw dataset (ignored in git)
- `notebooks/`: EDA and modeling
- `src/`: Preprocessing and training scripts
- `requirements.txt`: Dependencies

## Setup
1. Put the Kaggle `.sqlite` file in `data/`
2. Install dependencies: `pip install -r requirements.txt`
3. to train go to src
4. to infere go to start
5. for the notebook go to notebooks