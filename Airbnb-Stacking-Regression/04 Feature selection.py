# -*- coding: utf-8 -*-
"""
04 Feature selection

@author: WEI
"""

import numpy as np
import pandas as pd
from sklearn import feature_selection
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt

def load_data(train_x_path, train_y_path, val_x_path, val_y_path): 
    return pd.read_csv(train_x_path), pd.read_csv(train_y_path), pd.read_csv(val_x_path), pd.read_csv(val_y_path)

def select_features(X, y, threshold=1e-20): 
    F_vals, p_vals = feature_selection.f_regression(X, y)
    p_vals = np.nan_to_num(p_vals, nan=100) 
    return X.columns[p_vals < threshold]

def train_lasso(X_train, y_train, X_val, y_val, alphas): 
    best_score = 0
    best_alpha = 0
    
    for alpha in alphas: 
        reg = Lasso(alpha=alpha, max_iter=1e5) 
        reg.fit(X_train, y_train) 
        score = reg.score(X_val, y_val)
        
        if score > best_score: 
            best_score = score 
            best_alpha = alpha
            
    return best_alpha, best_score

if __name__ == '__main__': 
    # Load Data 
    X_train, y_train, X_val, y_val = load_data('data_cleaned_train_comments_X.csv', 'data_cleaned_train_y.csv',
                                               'data_cleaned_val_comments_X.csv', 'data_cleaned_val_y.csv')
    # Feature Selection
    selected_features = select_features(X_train, y_train.values.ravel())
    X_train_selected = X_train[selected_features]
    X_val_selected = X_val[selected_features]
    
    # Train Lasso
    alphas = [0.00016, 0.00018, 0.00020, 0.00022, 0.00024, 0.00026, 0.00028, 0.00030, 0.00032]
    best_alpha, best_score = train_lasso(X_train_selected, y_train, X_val_selected, y_val, alphas)
    
    # Final Model
    final_model = Lasso(alpha=best_alpha, max_iter=1e5)
    final_model.fit(X_train_selected, y_train)
    
    # Predictions and Plots 
    y_pred_train = final_model.predict(X_train_selected)
    y_pred_val = final_model.predict(X_val_selected)
    
    plt.figure(1)
    plt.scatter(y_pred_train, y_train)
    plt.title('Training Data')
    
    plt.figure(2)
    plt.scatter(y_pred_val, y_val)
    
    plt.show()
