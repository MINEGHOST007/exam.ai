import pandas as pd

product_df = pd.read_csv("data/shl_product_details.csv")
irt_df = pd.read_csv("data/adaptive_irt.csv")
for df in [product_df, irt_df]:
    df['name'] = df['name'].str.strip()
    df['url'] = df['url'].str.strip()
product_df = product_df.drop_duplicates(subset=['name', 'url'])
irt_df = irt_df.drop_duplicates(subset=['name', 'url'])

merged_df = pd.merge(product_df, irt_df, on=['name', 'url'], how='left')

if 'test_types_x' in merged_df.columns and 'test_types_y' in merged_df.columns:
    merged_df['test_types'] = merged_df['test_types_x'].combine_first(merged_df['test_types_y'])
    merged_df = merged_df.drop(columns=['test_types_x', 'test_types_y'])
merged_df = merged_df.drop_duplicates(subset=['name', 'url'])
merged_df.to_csv("data/combined_product_data.csv", index=False)
print("✅ Combined deduplicated CSV saved to: data/combined_product_data.csv")
