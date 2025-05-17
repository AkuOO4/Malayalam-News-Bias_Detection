# Malayalam News Bias Detection

## Overview

This project focuses on developing a system to automatically detect political bias in Malayalam news articles. By applying Natural Language Processing (NLP) techniques, the system classifies articles as Left, Right, or Neutral, aiming to promote media literacy and transparency.

## Motivation

The proliferation of digital media has led to an increase in biased information, impacting public opinion. There's a lack of tools to analyze bias in Malayalam news, hindering media literacy and research. This project addresses this gap by developing NLP techniques to accurately detect political bias in Malayalam news.

## Key Features

* **Data Collection and Preprocessing**: Scraped and cleaned Malayalam news articles from various sources.
* **Model Fine-tuning**: Fine-tuned Google's MURIL Base Uncased model for bias classification.
* **Evaluation**: Achieved 93% accuracy in classifying articles.
* **Bias Classification**: Classified articles into three categories: Left, Right, and Neutral.

## Methodology

1.  **Data Collection**: Collected articles from Malayalam news sources.
2.  **Preprocessing**: Cleaned data by removing HTML tags, duplicates, and non-Malayalam characters.
3.  **Model**: Fine-tuned MURIL Base Uncased model.
4.  **Training**: Trained the model with specific hyperparameters (epochs=3, batch_size=16, learning_rate=2e-5).
5.  **Evaluation**: Evaluated model performance using accuracy, precision, recall, and F1-score.

## Results

The fine-tuned MURIL model effectively classifies political bias in Malayalam news articles, achieving 93% accuracy.

## Technical Details

* **Programming Language**: Python 3.10
* **Libraries**: PyTorch, Transformers, re, nltk, BeautifulSoup, Scikit-learn, NumPy, pandas, Matplotlib/Seaborn
* **Environment**: Google Colab, Overleaf

## Future Work

* Expand the dataset with more diverse sources and timeframes.
* Hyperparameter tuning using cross-validation.
* Implement model explainability to enhance transparency and trustworthiness.

## Contributions

AKSHAYKS
