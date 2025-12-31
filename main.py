from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

api = FastAPI()

class ProductCategory(str, Enum):
  vegetables = "vegetables"
  fruits = "fruits"

class CreateProduct(BaseModel):
  category: ProductCategory
  name: str
  stock: int

class Product(BaseModel):
  id: int
  category: ProductCategory
  name: str
  available: bool
  stock: int

products = [
  {
    "id": 1,
    "category": "vegetables",
    "name": "tomato",
    "available": True,
    "stock": 125
  },
  {
    "id": 2,
    "category": "vegetables",
    "name": "red beans",
    "available": True,
    "stock": 56
  },
  {
    "id": 3,
    "category": "fruits",
    "name": "apple",
    "available": True,
    "stock": 150
  },
  {
    "id": 4,
    "category": "fruits",
    "name": "banana",
    "available": True,
    "stock": 100
  },
  {
    "id": 5,
    "category": "vegetables",
    "name": "cabbage",
    "available": True,
    "stock": 10
  },
  {
    "id": 6,
    "category": "fruits",
    "name": "dragonfriut",
    "available": False,
    "stock": 0
  },
  {
    "id": 7,
    "category": "fruits",
    "name": "orange",
    "available": True,
    "stock": 63
  },
  {
    "id": 8,
    "category": "vegetables",
    "name": "cucumber",
    "available": True,
    "stock": 120
  },
  {
    "id": 9,
    "category": "vegetables",
    "name": "pepper",
    "available": True,
    "stock": 38
  },
  {
    "id": 10,
    "category": "vegetables",
    "name": "onion",
    "available": True,
    "stock": 92
  },
  {
    "id": 11,
    "category": "fruits",
    "name": "kiwi",
    "available": True,
    "stock": 2
  },
  {
    "id": 12,
    "category": "vegetables",
    "name": "potatoes",
    "available": True,
    "stock": 320
  },
]

@api.post("/products")
def post_product(product: CreateProduct):
  product_id = max([item["id"] for item in products]) + 1 if products else 1
  
  new_product = {
    "id": product_id,
    "category": product.category,
    "name": product.name,
    "available": True if product.stock else False, 
    "stock": product.stock
  }

  products.append(new_product)
  return new_product

@api.get("/products/{id}")
def get_product(id: int):
  for item in products:
    if item["id"] == id:
      return item
    
@api.get("/products")
def get_all_products(category: ProductCategory | None = None):
  if category:
    return [item for item in products if item["category"] == category]
  return products