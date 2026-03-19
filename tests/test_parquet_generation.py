import pandas as pd

from src.ccoe_ai.services.build_embeddings import build_embeddings

input_path = "data/dummy.xlsx"
output_path = "data/dummy.parquet"

build_embeddings(input_path, output_path)

df_read = pd.read_parquet(output_path)

print("\n" + "="*50)
print(f"[+] Eventually total lines is {len(df_read)}")
print(f"[+] Data column name: {df_read.columns.tolist()}")

print("\n---Data Preview(first 5 lines)---\n")
preview_df = df_read.copy()

if 'embedding' in preview_df.columns:
    preview_df['embedding'] = preview_df['embedding'].apply(lambda x: x[:3] + ["..."])

print(preview_df.head())