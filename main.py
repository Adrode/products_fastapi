from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum

class NotFoundError(Exception):
  def __init__(self, id: int):
    self.id = id

api = FastAPI()

class ProductCategory(str, Enum):
  vegetables = "vegetables"
  fruits = "fruits"

class PatchStock(BaseModel):
  stock: int

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

@api.exception_handler(NotFoundError)
def not_found_error_handler(request: Request, exc: NotFoundError):
  return JSONResponse(
    status_code=404,
    content={"message": f"Product with ID: {exc.id} not found!"}
  )

@api.post("/products")
def post_product(product: CreateProduct):
  product_id = max([item["id"] for item in products]) + 1 if products else 1
  
  new_product = {
    "id": product_id,
    "category": product.category,
    "name": product.name,
    "available": product.stock > 0, 
    "stock": product.stock
  }

  products.append(new_product)
  return new_product

@api.put("/products/{id}")
def put_product(id: int, product: CreateProduct):
  for item in products:
    if item["id"] == id:
      item["category"] = product.category
      item["name"] = product.name
      item["stock"] = product.stock
      item["available"] = product.stock > 0
      return item
  raise NotFoundError(id=id)

@api.patch("/products/{id}/stock")
def patch_product_stock(id: int, update: PatchStock):
  for item in products:
    if item["id"] == id:
      item["stock"] = update.stock
      item["available"] = update.stock > 0
      return item
  raise NotFoundError(id=id)
    
@api.delete("/products/{id}")
def delete_product(id: int):
  for item in products:
    if item["id"] == id:
      products.remove(item)
      return {"message": f"Deleted product with ID: {id} - {item["name"]}"}
  raise NotFoundError(id=id)

@api.get("/products/{id}")
def get_product(id: int):
  for item in products:
    if item["id"] == id:
      return item
  raise NotFoundError(id=id)
    
@api.get("/products")
def get_all_products(category: ProductCategory | None = None):
  if category:
    return [item for item in products if item["category"] == category]
  return products