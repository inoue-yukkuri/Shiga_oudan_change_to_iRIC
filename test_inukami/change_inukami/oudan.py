import os
import pandas as pd

# ファイルパスを指定
input_file_path = '../犬上川/oudan.csv'
output_dir = 'csv_files'

# 出力ディレクトリを作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# CSVファイルを読み込みます
with open(input_file_path, 'r', encoding='shift_jis') as file:
    lines = file.readlines()

# データセットの分割を行う
datasets = []
current_dataset = []

def is_header(line):
    # 行をカンマで分割し、最後の要素が空でないかを確認
    return line.strip().split(',')[-1] != ''

for line in lines:
    if is_header(line):
        if current_dataset:
            datasets.append(current_dataset)
        current_dataset = [line.strip()]
    else:
        current_dataset.append(line.strip())

# 最後のデータセットを追加
if current_dataset:
    datasets.append(current_dataset)

# 分割されたデータセットを個別のCSVファイルに保存
for index, dataset in enumerate(datasets):
    header = dataset[0]
    file_number = header.split(',')[0].strip()
    data_rows = dataset[1:]

    # 各データセットをデータフレームに変換
    df = pd.DataFrame([x.split(',') for x in data_rows])
    # 無駄なカンマを削除
    df = df.replace(r'^\s*$', pd.NA, regex=True).dropna(axis=1, how='all')

    # 連番の数値を生成（4桁）
    sequence_number = f'{index + 1:04d}'

    # ファイル名を指定して保存
    output_file_path = os.path.join(output_dir, f'{file_number}_{sequence_number}.csv')
    with open(output_file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(header + '\n')  # ヘッダー行を書き込む
        df.to_csv(f, index=False, header=False)

    print(f'Saved {output_file_path}')

print('All datasets have been split and saved.')
