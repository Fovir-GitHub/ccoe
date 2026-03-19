import pandas as pd

from src.ccoe_ai.services.build_embeddings import build_embeddings
from src.ccoe_ai.utils.xlsx import read_xlsx
from src.ccoe_ai.normalization.normalization import normalization

input_path = "data/dummy.xlsx"
output_path = "data/dummy.parquet"

df_init = read_xlsx(input_path)
df_clean = normalization(df_init)
# transfer all non-embedding columns -> str
for col in df_clean.columns:
    df_clean[col] = df_clean[col].astype(str)
df_clean.to_excel(input_path, index=False)

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