# -*- coding: utf-8 -*-
"""
06 Visualize model training

@author: WEI
"""

import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.svm import SVR

# Iterative Ridge Regression to find optimal alpha 
def iterative_ridge_regression(X_train, y_train, X_val, y_val): 
    best_alpha, best_val_score = None, float('-inf') 
    val_scores, train_scores, alphas = [], [], list(range(1, 20))

    for alpha in alphas: 
        model = Ridge(alpha=alpha) 
        model.fit(X_train, y_train) 
        
        val_score = model.score(X_val, y_val)
        train_score = model.score(X_train, y_train)
        
        if val_score > best_val_score: 
            best_val_score = val_score 
            best_alpha = alpha
        
        val_scores.append(val_score)
        train_scores.append(train_score)
            
    plot_scores(alphas, train_scores, val_scores, "Alpha Value", "R^2 Score", "Ridge Regression Performance")
    
    print(f"Optimal alpha: {best_alpha}")
    print(f"Best validation score: {best_val_score}")


# Plot for Training vs Validation errors for Gradient Boosting
def plot_gb_errors(train_errors, val_errors): 
    plt.figure(figsize=(12, 6))
    plt.plot(train_errors, "b-", linewidth=2, label="Training Set")
    plt.plot(val_errors, "r-", linewidth=3, label="Validation Set")
    plt.legend(loc="upper right", fontsize=14)
    plt.xlabel("Boosting Iterations", fontsize=14)
    plt.ylabel("Mean Squared Error", fontsize=14)
    plt.title("Training vs. Validation Error", fontsize=16)
    plt.show()
    
# Iterative SVM to find optimal gamma and C
def iterative_svm(X_train, y_train, X_val, y_val): 
    best_params, best_val_score = None, float('-inf') 
    val_scores, train_scores = [], []
    gamma_values, C_values = [0.05, 0.1, 0.2, 0.3, 0.4], [0.5, 1, 1.5, 2]
    
    for gamma in gamma_values:
        for C in C_values: model = SVR(gamma=gamma, C=C) 
        model.fit(X_train, y_train) 
        
        val_score = model.score(X_val, y_val)
        train_score = model.score(X_train, y_train)

    if val_score > best_val_score: 
        best_val_score = val_score 
        best_params = {'gamma': gamma, 'C': C} 
        
    val_scores.append(val_score)
    train_scores.append(train_score)
    
    plot_scores(range(len(val_scores)), train_scores, val_scores, "Iteration", "Performance Metric", "SVM Performance")
    print(f"Optimal parameters: {best_params}")
    print(f"Best validation score: {best_val_score}")
    
# Helper function to plot scores 
def plot_scores(x_values, train_scores, val_scores, x_label, y_label, title): 
    plt.plot(x_values, train_scores, 'x-', label='Training Score')
    plt.plot(x_values, val_scores, 'o-', label='Validation Score')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.show()
    
# Your code to load data and call these functions will go here. 
# For example: 
# X_train, y_train, X_val, y_val = load_your_data()
# iterative_ridge_regression(X_train, y_train, X_val, y_val)
# iterative_svm(X_train, y_train, X_val, y_val)