# Chapter 10 Data Files

## rucking_camping_products.xlsx

The source data for the RuckZone product enrichment pipeline.

### Structure

| Column | Description |
|--------|-------------|
| Brand Name | The product manufacturer (e.g., "GORUCK", "Osprey") |
| Product Name | The specific product (e.g., "GR1 26L", "Atmos AG 65") |

### Contents

- **~445 products** across multiple categories
- **Categories**: Backpacks, tents, sleeping bags, sleeping pads, stoves, water filters, headlamps, ruck plates
- **Brands**: GORUCK, Mystery Ranch, Osprey, Big Agnes, MSR, NEMO, Sawyer, Petzl, and more

### Usage

Load the data with pandas:

```python
import pandas as pd

df = pd.read_excel('data/rucking_camping_products.xlsx')
print(f"Loaded {len(df)} products")
```

Create search keys by combining Brand Name and Product Name:

```python
df['search_key'] = df['Brand Name'] + ' ' + df['Product Name']
```
