# Listing 12.7 The orchestrator: chaining the agents
import time
from typing import Dict, List


def run_one(product: ProductInput) -> PipelineRecord:  #A
    """Run a single product through every agent, tracking state."""
    key = f"{product.brand_name} {product.product_name}"
    record = PipelineRecord(search_key=key)
    try:
        record.stage = "discover"  #B
        ranking = discover_url(key)
        if ranking is None:
            record.status = "failed"
            record.error = "no candidate URLs"
            return record
        record.url = ranking.best_url
        record.confidence = ranking.confidence

        record.stage = "fetch"  #C
        cleaned = fetch_and_clean(record.url)

        record.stage = "extract"  #D
        extraction = extract_product(cleaned)

        record.stage = "validate"  #E
        enriched, issues = validate_and_map(
            extraction, record.url, product
        )
        record.enriched = enriched
        record.notes = issues

        if issues or ranking.confidence.lower() == "low":  #F
            record.status = "needs_review"
        else:
            record.status = "success"
    except Exception as exc:  #G
        record.status = "failed"
        record.error = f"{type(exc).__name__}: {exc}"
        logger.warning(
            "%s failed at %s: %s", key, record.stage, exc
        )
    return record


def run_pipeline(products: List[ProductInput]) -> Dict:  #H
    """Run every product and split results from the review queue."""
    results, review_queue = [], []
    for product in products:
        record = run_one(product)  #I
        results.append(record)
        if record.status == "needs_review":
            review_queue.append(record)
        logger.info("%s -> %s", record.search_key, record.status)
        time.sleep(1)  #J
    return {"results": results, "review_queue": review_queue}

#A One product, one record, threaded through the four agents in order
#B Stage 2 (Ch11): discover the best URL, or fail fast if none
#C Stage 3: fetch and clean, with retries inside the agent
#D Stage 5: AI extraction into the ProductExtraction schema
#E Stage 6: normalize and validate into an EnrichedProduct
#F Low confidence or any issue routes the record to human review
#G One catch-all: a failure in any stage is recorded, never fatal
#H The orchestrator over a batch of products
#I Each record is independent, so one failure never stops the batch
#J A short pause keeps us from hammering sites and APIs
