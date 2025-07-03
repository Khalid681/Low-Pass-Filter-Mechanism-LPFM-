import pandas as pd
import numpy as np
import os

main_dataset_path = r'C:\Users\khalid usman\Desktop\New Folder\main_data.csv'
output_folder = r'C:\Users\khalid usman\Desktop\New Folder\processed_datasets'
bandwidths = [125, 250, 500]
spreading_factors = [10, 11, 12]


os.makedirs(output_folder, exist_ok=True)


def preprocess_dataset(path):
    df = pd.read_csv(path)


    df.dropna(how='all', inplace=True)
    
    required_cols = ['snr', 'bandwidth', 'spreading_factor', 'frequency']
    df = df[[col for col in df.columns if col in required_cols]]


    df.dropna(inplace=True)


    df['snr'] = pd.to_numeric(df['snr'], errors='coerce')
    df['bandwidth'] = pd.to_numeric(df['bandwidth'], errors='coerce')
    df['spreading_factor'] = pd.to_numeric(df['spreading_factor'], errors='coerce')
    df['frequency'] = pd.to_numeric(df['frequency'], errors='coerce')

    df.dropna(inplace=True)


    z_scores = np.abs((df['snr'] - df['snr'].mean()) / df['snr'].std())
    df = df[z_scores < 3]

    return df


clean_df = preprocess_dataset(main_dataset_path)


for bw in bandwidths:
    bw_df = clean_df[clean_df['bandwidth'] == bw]
    
    for sf in spreading_factors:
        subset_df = bw_df[bw_df['spreading_factor'] == sf]

        if not subset_df.empty:
            file_name = f'data_bw{bw}_sf{sf}.csv'
            save_path = os.path.join(output_folder, file_name)
            subset_df.to_csv(save_path, index=False)
            print(f" Saved: {file_name} with {len(subset_df)} rows.")
        else:
            print(f" No data for BW={bw}, SF={sf} — skipping...")

print(f"\n All processing done. Files saved in: {output_folder}")
