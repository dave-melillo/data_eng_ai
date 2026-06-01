# Listing 12.1 The pipeline data contract
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductInput(BaseModel):  #A
    """What goes into the pipeline: brand + product name."""
    brand_name: str
    product_name: str


class ProductExtraction(BaseModel):  #B
    """Raw fields the LLM pulls from a page (from Chapter 11)."""
    product_name: str
    brand_name: str
    description: Optional[str] = None
    price: Optional[str] = None
    weight: Optional[str] = None
    primary_image_url: Optional[str] = None
    category: Optional[str] = None


class EnrichedProduct(BaseModel):  #C
    """The validated, normalized record (pipeline Stage 6)."""
    brand_name: str
    product_name: str
    product_url: Optional[str] = None
    description: Optional[str] = None
    price_usd: Optional[float] = None
    weight_value: Optional[float] = None
    weight_unit: Optional[str] = None
    primary_image_url: Optional[str] = None
    category: Optional[str] = None


class PipelineRecord(BaseModel):  #D
    """The unit of work that flows through every agent."""
    search_key: str
    status: str = "pending"  #E
    stage: str = "start"  #F
    url: Optional[str] = None
    confidence: Optional[str] = None
    enriched: Optional[EnrichedProduct] = None
    notes: List[str] = Field(default_factory=list)  #G
    error: Optional[str] = None

#A The pipeline input: exactly what RuckZone gave us in Chapter 10
#B The unstructured fields an LLM returns; same schema as Chapter 11
#C The clean, typed record we actually want to store
#D One PipelineRecord per product carries state across all stages
#E Lifecycle status: pending, success, needs_review, or failed
#F The last stage that touched this record, for debugging
#G Validation issues collected along the way, for the review queue
