import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# データの読み込み
gyro_bias_df = pd.read_csv("gyro_bias.csv")
speed_actual_df = pd.read_csv("speed_actual.csv")

# JSTに変換
gyro_bias_df['timestamp'] = pd.to_datetime(gyro_bias_df['timestamp'], unit='s', utc=True).dt.tz_convert('Asia/Tokyo')
speed_actual_df['timestamp'] = pd.to_datetime(speed_actual_df['timestamp'], unit='s', utc=True).dt.tz_convert('Asia/Tokyo')

# サブプロット作成（2行1列）
fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True,
    subplot_titles=("Gyro Bias (x, y, z)", "Speed Actual"),
    vertical_spacing=0.15
)

# Gyro Biasの各軸を上段に描画
colors = {'x': 'red', 'y': 'green', 'z': 'blue'}  # 各軸の色を定義
for axis in ['x', 'y', 'z']:
    col_name = f'gyro_bias_{axis}'
    if col_name in gyro_bias_df.columns:
        fig.add_trace(go.Scatter(
            x=gyro_bias_df['timestamp'], y=gyro_bias_df[col_name],
            mode='lines', name=f'{col_name}',  # (raw)の表記を削除してすっきりと
            line=dict(color=colors[axis], width=1.5),  # 線の太さを少し太くし、透明度を削除
        ), row=1, col=1)

# Speed Actualを下段に描画（紫）
fig.add_trace(go.Scatter(
    x=speed_actual_df['timestamp'], y=speed_actual_df['speed_actual'],
    mode='lines', name='speed_actual',
    line=dict(color='purple')
), row=2, col=1)

# レイアウト設定
fig.update_layout(
    title="/sensing/imu/gyro_bias (x, y, z) and /g30esli/status.status.speed.actual",
    legend=dict(x=0, y=1),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(  # これは xaxis1 に対応（上段）
        title="Timestamp (JST)",
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black'),
        showticklabels=True  # ← これが必要
    ),
    xaxis2=dict(  # 下段
        title="Timestamp (JST)",
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black')
    ),
    yaxis=dict(
        title="Gyro Bias (rad/s)",
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black')
    ),
    yaxis2=dict(
        title="Speed Actual (m/s)",
        showline=True,
        linecolor='black',
        linewidth=1.5,
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(color='black')
    )
)

# 表示と保存
fig.show()
fig.write_html("gyro_bias_and_speed_actual.html")
print("Saved plot to 'gyro_bias_and_speed_actual.html'")
