# Listing 12.8 Running the full pipeline on a batch
import pandas as pd

products = [  #A
    ProductInput(brand_name="GORUCK", product_name="GR1 26L"),
    ProductInput(brand_name="GORUCK", product_name="Rucker 4.0 20L"),
    ProductInput(brand_name="Osprey", product_name="Atmos AG 65"),
    ProductInput(brand_name="Petzl", product_name="Actik Core"),
    ProductInput(brand_name="Sawyer", product_name="Squeeze"),
]

configure_logging()  #B
outcome = run_pipeline(products)  #C

rows = []  #D
for record in outcome["results"]:
    enriched = record.enriched
    rows.append({
        "search_key": record.search_key,
        "status": record.status,
        "stage": record.stage,
        "price_usd": enriched.price_usd if enriched else None,
        "category": enriched.category if enriched else None,
        "issues": ", ".join(record.notes) or None,
    })

df = pd.DataFrame(rows)  #E
print("\nPipeline results:\n")
display(df)

counts = df["status"].value_counts().to_dict()  #F
print(f"\nSummary: {counts}")
print(f"Review queue: {len(outcome['review_queue'])} record(s)")

#A The batch of RuckZone products to enrich end to end
#B Turn on logging so we can watch each record progress
#C Run the whole batch through the orchestrated pipeline
#D Flatten each PipelineRecord into a row for inspection
#E Build a DataFrame so the results are easy to scan
#F Tally how many succeeded, need review, or failed
