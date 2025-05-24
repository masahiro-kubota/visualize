#! /usr/bin/env python3

"""
Usage:
    python3 plot_angular_velocity.py [axis]
    
    axis: x, y, or z (default: z)

Description:
    - This script reads 'angular_velocity.csv' which must contain 'timestamp' column as index
      (UNIX time in seconds) and 'angular_velocity_{axis}' columns with angular velocity data.
    - It applies a 400-sample moving median filter to reduce noise.
    - The script converts the UNIX timestamps to JST (Japan Standard Time).
    - An interactive plot is displayed using Plotly and also saved to 'angular_velocity_plot.html'.

Requirements:
    pip install pandas plotly
"""

import pandas as pd
import plotly.graph_objects as go
import sys

# Get axis from command line argument
axis = 'z'  # default
if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['x', 'y', 'z']:
        axis = sys.argv[1].lower()
    else:
        print("Invalid axis. Please specify 'x', 'y', or 'z'")
        sys.exit(1)

# Load the CSV
df = pd.read_csv("angular_velocity.csv", index_col="timestamp")

# Convert UNIX timestamp to JST
df.index = pd.to_datetime(df.index, unit='s', utc=True).tz_convert('Asia/Tokyo')

# Apply 400-sample moving median
column_name = f"angular_velocity_{axis}"
df[f"{column_name}_median"] = df[column_name].rolling(window=400, center=True).median()

# Create figure
fig = go.Figure()

# Raw data trace (gray with opacity)
fig.add_trace(go.Scatter(
    x=df.index, 
    y=df[column_name], 
    mode='lines', 
    name=f'/sensing/imu/imu_data.angular_velocity.{axis}',
    line=dict(color='gray'),
    opacity=0.3
))

# Filtered data trace (blue and bold)
fig.add_trace(go.Scatter(
    x=df.index, 
    y=df[f"{column_name}_median"], 
    mode='lines', 
    name='400-sample Median',
    line=dict(color='blue', width=2)
))

# Threshold lines (red dashed)
fig.add_trace(go.Scatter(
    x=df.index,
    y=[0.0025] * len(df.index),
    mode='lines',
    name='Upper threshold (+0.0025 rad/s)',
    line=dict(color="red", dash="dash")
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=[-0.0025] * len(df.index),
    mode='lines',
    name='Lower threshold (-0.0025 rad/s)',
    line=dict(color="red", dash="dash")
))

# Layout settings
fig.update_layout(
    title=f"/sensing/imu/imu_data.angular_velocity.{axis} with 400-sample Moving Median",
    xaxis_title="Timestamp (JST)",
    yaxis_title=f"angular_velocity.{axis} (rad/s)",
    legend=dict(x=0, y=1),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black')
    )
)

# Show and save
fig.show()
fig.write_html(f"angular_velocity_{axis}_plot.html")
print(f"Saved interactive plot to angular_velocity_{axis}_plot.html")
