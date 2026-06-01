# Listing 12.6 Agent 4: validate and map (Stage 6)
import re
from typing import List, Optional, Tuple

REQUIRED_FIELDS = ["product_name", "brand_name", "price_usd"]  #A


def _parse_price(price: Optional[str]) -> Optional[float]:  #B
    if not price:
        return None
    match = re.search(r"[\d,]+\.?\d*", price.replace(",", ""))
    return float(match.group()) if match else None


def _parse_weight(weight: Optional[str]
                  ) -> Tuple[Optional[float], Optional[str]]:  #C
    if not weight:
        return None, None
    match = re.search(r"([\d.]+)\s*(lbs?|oz|kg|g)\b", weight, re.I)
    if not match:
        return None, None
    return float(match.group(1)), match.group(2).lower()


def validate_and_map(
    extraction: ProductExtraction,
    url: Optional[str],
    fallback: ProductInput,
) -> Tuple[EnrichedProduct, List[str]]:  #D
    """Agent: normalize values into the final schema and check them."""
    issues: List[str] = []
    price = _parse_price(extraction.price)  #E
    weight_value, weight_unit = _parse_weight(extraction.weight)
    record = EnrichedProduct(  #F
        brand_name=extraction.brand_name or fallback.brand_name,
        product_name=extraction.product_name or fallback.product_name,
        product_url=url,
        description=extraction.description,
        price_usd=price,
        weight_value=weight_value,
        weight_unit=weight_unit,
        primary_image_url=extraction.primary_image_url,
        category=extraction.category,
    )
    for field in REQUIRED_FIELDS:  #G
        if getattr(record, field) in (None, ""):
            issues.append(f"missing {field}")
    if price is not None and not (0 < price < 100000):  #H
        issues.append(f"price out of range: {price}")
    return record, issues

#A The fields a record must have to be trusted without review
#B Turn a messy price string like "$395.00" into a float
#C Split "4.21 lbs" into a numeric value and a unit string
#D The agent: raw extraction in, a clean record plus issue list out
#E Deterministic normalization, no LLM needed here
#F Build the typed record, falling back to the known input fields
#G Flag any required field that came back empty
#H Sanity-check the price; obvious outliers go to review, not the DB
