# -*- coding: utf-8 -*-
"""
05 Running models

@author: WEI
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, metrics, svm
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.linear_model import Ridge
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import StackingRegressor
import multiprocessing

# Load data 
def load_data(): 
    X_train = pd.read_csv('data_cleaned_train_comments_X.csv')
    y_train = pd.read_csv('data_cleaned_train_y.csv')
    X_val = pd.read_csv('data_cleaned_val_comments_X.csv')
    y_val = pd.read_csv('data_cleaned_val_y.csv')
    X_test = pd.read_csv('data_cleaned_test_comments_X.csv')
    y_test = pd.read_csv('data_cleaned_test_y.csv') 
    return X_train, y_train, X_val, y_val, X_test, y_test

# Print Evaluation Metrics 
def print_metrics(model, model_name, X, y, data_type='Test'): 
    print(f'--------- For Model: {model_name} --------- ({data_type} Data)\n')
    preds = model.predict(X)
    print("Mean absolute error:", mean_absolute_error(y, preds))
    print("Mean squared error:", mean_squared_error(y, preds))
    print("R2:", r2_score(y, preds))
    
# Linear Models 
def train_linear_model(X_train, y_train, X_val, y_val): 
    model = linear_model.LinearRegression() 
    model.fit(X_train, y_train)
    print_metrics(model, 'Linear Model', X_val, y_val)
    
# Ridge Regression
def train_ridge(X_train, y_train, X_val, y_val): 
    model = Ridge(alpha=13) 
    model.fit(X_train, y_train)
    print_metrics(model, 'Ridge Model', X_val, y_val)
    
# Gradient Boosting
def train_gb(X_train, y_train, X_val, y_val): 
    model = GradientBoostingRegressor(n_estimators=30, random_state=42, loss='huber', learning_rate=0.12, max_depth=9) 
    model.fit(X_train, y_train)
    print_metrics(model, 'Gradient Boosting', X_val, y_val)

# Support Vector Machine 
def train_svm(X_train, y_train, X_val, y_val): 
    model = SVR(gamma=0.2, C=0.5) 
    model.fit(X_train, y_train)
    print_metrics(model, 'SVM', X_val, y_val)

# Stacked Model
def train_stacked_model(X_train, y_train, X_val, y_val): 
    base_models = [
        ('Linear Regression', linear_model.LinearRegression()), 
        ('Ridge Regression', Ridge(alpha=13)), 
        ('Gradient Boosting Regressor', GradientBoostingRegressor(n_estimators=30, random_state=42,loss='huber', learning_rate=0.12, max_depth=9)), 
        ('SVM', SVR(gamma=0.2, C=0.5))]
    stacked_model = StackingRegressor(estimators=base_models, final_estimator=linear_model.LinearRegression())

    stacked_model.fit(X_train, y_train)
    print_metrics(stacked_model, 'Stacked Model', X_val, y_val)

if __name__ == "__main__":
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    print("--------------------Linear Model--------------------")
    train_linear_model(X_train, y_train, X_val, y_val)
    print("--------------------Ridge Model--------------------")
    train_ridge(X_train, y_train, X_val, y_val)
    print("--------------------Gradient Boosting Model--------------------")
    train_gb(X_train, y_train, X_val, y_val)
    print("--------------------SVM Model--------------------")
    train_svm(X_train, y_train, X_val, y_val)
    print("--------------------Stacked Model--------------------")
    train_stacked_model(X_train, y_train, X_val, y_val)        





