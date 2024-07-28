import os
import pandas as pd
from pyproj import Transformer

# ファイルパスを指定
input_file_path = '../犬上川/kui.csv'

# ファイルの存在を確認
if not os.path.exists(input_file_path):
    raise FileNotFoundError(f"File not found: {input_file_path}")

# CSVファイルを読み込みます
df = pd.read_csv(input_file_path, encoding='shift_jis')

# EPSG:4612からEPSG:2448への変換を行うTransformerを作成します
transformer = Transformer.from_crs("EPSG:4612", "EPSG:2448", always_xy=True)

# 緯度経度を変換します
def transform_coordinates(lat, lon):
    x, y = transformer.transform(lat, lon)  # 緯度と経度の順序を正しく修正
    return x, y

# 左岸と右岸の座標を分けるためのデータフレームを準備
left_bank = df[df['左右岸'] == '左岸']
right_bank = df[df['左右岸'] == '右岸']

# 左岸と右岸の座標を変換
left_bank[['LX', 'LY']] = left_bank.apply(lambda row: pd.Series(transform_coordinates(row['緯度'], row['経度'])), axis=1)
right_bank[['RX', 'RY']] = right_bank.apply(lambda row: pd.Series(transform_coordinates(row['緯度'], row['経度'])), axis=1)

# 左岸と右岸のデータフレームをマージ
merged_df = pd.merge(left_bank[['距離標名', 'LX', 'LY']], right_bank[['距離標名', 'RX', 'RY']], on='距離標名')

# カラム名を変更
merged_df.rename(columns={'距離標名': 'KP'}, inplace=True)

# KPの最小値と最大値を取得
min_kp = merged_df['KP'].min()
max_kp = merged_df['KP'].max()

# 出力ファイル名を設定
output_file_path = f'sect_{min_kp}-{max_kp}.csv'

# 指定された形式で出力
output_df = merged_df[['KP', 'LX', 'LY', 'RX', 'RY']]
output_df.to_csv(output_file_path, index=False, encoding='utf-8')

# 結果を表示
print(output_df)
print(f'Saved {output_file_path}')
