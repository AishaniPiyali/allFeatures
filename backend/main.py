import random
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# -----------------------------
# 📦 Pydantic Schemas
# -----------------------------
class Category(BaseModel):
    id: int
    name: str
    description: str

class CategoryInDB(Category):
    _id: str  # used for internal inspection/debugging if needed

class Product(BaseModel):
    id: int
    name: str
    brand: str
    description: str
    price: float
    stock: int
    quantity: int = 1  # default quantity for orders
    features: List[str]
    category: Category

class Order(BaseModel):
    id: Optional[int] = None
    customer_name: str
    customer_address: str
    items: List[Product] = []  # list of products in the order
    total_price: float = 0.0  # can be calculated in API
    order_date: datetime = Field(default_factory=datetime.now)
    # status: str = "pending"  # default status
# -----------------------------
# 🚀 FastAPI App Setup
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 🧪 DB Ping Route
# -----------------------------
@app.get("/ping-db")
def ping_db():
    try:
        db = get_db()
        db.command("ping")
        return {"status": "MongoDB connection successful"}
    except PyMongoError as e:
        return {"status": "MongoDB connection failed", "error": str(e)}


# -----------------------------
# 📄 List All Categorys
# -----------------------------
@app.get("/myFirstCollection", response_model=List[Category])
def list_catagories():
    db = get_db()
    catagories_cursor = db["myFirstCollection"].find()
    catagories = []

    for p in catagories_cursor:
        catagories.append({
            "id": p["id"],
            "name": p["name"],
            "description": p["description"]
        })

    return catagories


# -----------------------------
# ➕ Add a New Category
# -----------------------------
# @app.post("/myFirstCollection", status_code=201)
# def add_category(category: Category = Body(...)):
#     db = get_db()

#     # Ensure custom ID is unique
#     if db["myFirstCollection"].find_one({"id": category.id}):
#         raise HTTPException(status_code=400, detail="Category with this ID already exists")

#     result = db["myFirstCollection"].insert_one(category.dict())
#     return {"message": "Category added", "inserted_id": str(result.inserted_id)}


# -----------------------------
# ➕ Add a New Order
# -----------------------------
def generate_unique_order_id(db):
    while True:
        new_id = random.randint(100000, 999999)  # 6-digit integer
        if not db["orders"].find_one({"id": new_id}):
            return new_id

@app.post("/orders", status_code=201)
def add_order(order: Order = Body(...)):
    db = get_db()

    # Generate unique integer order ID
    unique_id = generate_unique_order_id(db)
    order.id = unique_id
    order.order_date = datetime.now()

    # Calculate total price
    total = sum(item.quantity * item.price for item in order.items)
    order.total_price = total

    # Insert into MongoDB
    result = db["orders"].insert_one(order.dict())

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "inserted_id": str(result.inserted_id),
        "total_price": total
    }
# -----------------------------
# 🔍 Get Category by Business ID
# -----------------------------
# @app.get("/myFirstCollection/{category_id}", response_model=Category)
# def get_category(category_id: int):
#     db = get_db()
#     category = db["myFirstCollection"].find_one({"id": category_id})

#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return {
#         "id": category["id"],
#         "name": category["name"],
#         "description": category["description"]
#     }

# -----------------------------
# 🔍 Get Category items/products by Business ID
# -----------------------------
@app.get("/myFirstCollection/{category_id}/products", response_model=List[Product])
def get_products_by_category(category_id: int):
    db = get_db()

    # 1. Get the category name from the ID
    category_doc = db["myFirstCollection"].find_one({"id": category_id})
    if not category_doc:
        raise HTTPException(status_code=404, detail="Category not found")

    category_name = category_doc["name"]

    # 2. Match either embedded object or string category
    products_cursor = db["products"].find({"category.id": category_id})
    # 3. Find all products in that category
    products = []

    for product in products_cursor:
        products.append({
            "id": product.get("id"),
            "name": product.get("name"),
            "brand": product.get("brand"),
            "description": product.get("description"),
            "price": product.get("price"),
            "stock": product.get("stock"),
            "features": product.get("features"),
            "category": product.get("category")  # This can be a string or an object
        })

    return products

# -----------------------------
# 🔁 Update Category by Business ID
# -----------------------------
# @app.put("/myFirstCollection/{category_id}")
# def update_category(category_id: int, updated_data: Category):
#     db = get_db()
#     result = db["myFirstCollection"].update_one(
#         {"id": category_id},
#         {"$set": updated_data.dict()}
#     )

#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return {"message": "Category updated successfully"}


# -----------------------------
# ❌ Delete Category by Business ID
# -----------------------------
# @app.delete("/myFirstCollection/{category_id}")
# def delete_category(category_id: int):
#     db = get_db()
#     result = db["myFirstCollection"].delete_one({"id": category_id})

#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return {"message": "Category deleted successfully"}
