from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel
from app.core.closest_product import find_closest
from app.core.brand_extractor import BrandExtractor
from app.core.unit_extractor import extract_units
from app.db.filter import filter_products

app = FastAPI()

brandExtractor = None

@app.on_event("startup")
def startup():
    print("Startup")
    global brandExtractor
    brandExtractor = BrandExtractor()


@app.get("/recommended")
def get_recommended_product(product: str):
    brand = brandExtractor.extract(product)
    unit = extract_units(product)[0]
    number = extract_units(product)[1]
    data = filter_products(brand, unit, number)
    closest_product = find_closest(data, product)

    return {
        "product": closest_product[0],
        "cosine_similarity": closest_product[1],
    }