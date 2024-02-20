# -*- coding: utf-8 -*-
"""
01 sentiment score

@author: WEI
"""

from textblob import TextBlob
import pandas as pd
import math
import os

def load_data(file_path): 
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def filter_data_by_ids(data, listing_data, id_column='id', filter_column='listing_id'): 
    """Filter data by unique ids in listing DataFrame.""" 
    unique_ids = listing_data[id_column].unique() 
    return data[data[filter_column].isin(unique_ids)]

def compute_sentiment(text_entry): 
    """Compute sentiment score using TextBlob."""
    if pd.isna(text_entry): 
        return None 
    opinion = TextBlob(text_entry) 
    return opinion.sentiment.polarity

def apply_sentiment_analysis(data, text_column='comments', output_column='sentiment'): 
    """Apply sentiment analysis on a DataFrame.""" 
    data[output_column] = data[text_column].apply(compute_sentiment) 
    return data.dropna(subset=[output_column])

def aggregate_sentiment(data, group_by_column='listing_id', aggregate_column='sentiment'): 
    """Aggregate sentiment scores by grouping."""
    return data.groupby(group_by_column)[aggregate_column].mean()

def save_to_csv(data, output_file_path): 
    """Save DataFrame to CSV file.""" 
    data.to_csv(output_file_path)
    
    
if __name__ == '__main__': 
    # Settings
    folder_path = 'D:/.../dataset/new york/June' 
    reviews_file = os.path.join(folder_path, 'reviews.csv') 
    output_file = 'reviews_cleaned.csv' 
    
    # Load datasets
    reviews_data = load_data(reviews_file)

    # Assuming listing_data is previously loaded
    listing_data = ... # Load your listing data here

    # Filter data by unique ids
    filtered_data = filter_data_by_ids(reviews_data, listing_data)

    # Drop unnecessary columns 
    columns_to_drop = ['id', 'date', 'reviewer_id', 'reviewer_name']
    filtered_data.drop(columns=columns_to_drop, inplace=True)

    # Apply sentiment analysis 
    analyzed_data = apply_sentiment_analysis(filtered_data)
    # Aggregate sentiment scores 
    aggregated_data = aggregate_sentiment(analyzed_data)
    # Save to CSV
    save_to_csv(aggregated_data, output_file)