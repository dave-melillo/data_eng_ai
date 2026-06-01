# Listing 12.9 Working the review queue and saving results
import pandas as pd


def show_review_queue(outcome):  #A
    """Print why each flagged record needs a human."""
    queue = outcome["review_queue"]
    if not queue:
        print("Nothing to review.")
        return
    for record in queue:
        print(f"\n{record.search_key}  ({record.confidence} conf.)")
        print(f"  url:    {record.url}")
        print(f"  issues: {', '.join(record.notes) or 'low confidence'}")


def save_results(outcome, path="enriched_products.csv"):  #B
    """Persist only the trusted records to a CSV catalog."""
    good = [
        r.enriched.model_dump()  #C
        for r in outcome["results"]
        if r.status == "success" and r.enriched
    ]
    df = pd.DataFrame(good)
    df.to_csv(path, index=False)  #D
    print(f"Saved {len(df)} trusted records to {path}")
    return df


show_review_queue(outcome)  #E
catalog = save_results(outcome)

#A A quick triage view of everything routed to human review
#B Only success records are written; review/failed are held back
#C model_dump turns each Pydantic record into a plain dict
#D Write the catalog RuckZone can load into a database
#E Inspect the queue, then save the clean catalog
