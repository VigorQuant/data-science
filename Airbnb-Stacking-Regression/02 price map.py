# -*- coding: utf-8 -*-
"""
# 02 price map

@author: WEI
"""

import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import Point

def load_geojson(file_path): 
    """Load GeoJSON file."""
    return gp.read_file(file_path)

def load_csv(file_path, columns=None): 
    """Load data from a CSV file into a DataFrame.""" 
    df = pd.read_csv(file_path)
    if columns: 
        return df[columns] 
    return df

def preprocess_price(df, price_column='price'): 
    """Preprocess price column by removing special characters and converting to float.""" 
    df[price_column] = df[price_column].replace({'\$': '', ',': ''}, regex=True).astype(float) 
    return df

def filter_by_price(df, max_price=200, price_column='price'): 
    """Filter dataframe by maximum price."""
    return df[df[price_column] <= max_price]


def plot_geo_data(base_map, data_points, column_to_color, title, output_file): 
    """Plot geographical data.""" 
    plot = data_points.plot(ax=base_map, marker='o', column=column_to_color, markersize=1, legend=True)
   
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    
    divider = make_axes_locatable(plot.axes) 
    cax = divider.append_axes("right", size="5%", pad=0.5) 
    cbar = plt.colorbar(plot.get_children()[1], cax=cax) 
    cbar.set_label('Price')
    
    plt.savefig(output_file, bbox_inches='tight')
    plt.show()
    

if __name__ == '__main__': 
    folder_path = 'D:/xxx/dataset/new york/June' 
    geo_file = f"{folder_path}/neighbourhoods.geojson"
    csv_file = f"{folder_path}/Detailed Listings.csv" 
    
    # Load GeoJSON file 
    nyc_geo = load_geojson(geo_file)
    
    # Load and preprocess CSV data 
    df = load_csv(csv_file, columns=['latitude', 'longitude', 'price'])
    df = preprocess_price(df)
    df = filter_by_price(df)
    
    # Convert DataFrame to GeoDataFrame 
    df['geometry'] = gp.points_from_xy(df.longitude, df.latitude)
    gdf = gp.GeoDataFrame(df)
    
    # Plot data 
    plot_geo_data(nyc_geo.plot(color='white', edgecolor='black', linewidth=1, figsize=(10, 10)),
                  gdf, 'price', 'NYC Airbnb Data Price Range', 'Price_map.svg')
    