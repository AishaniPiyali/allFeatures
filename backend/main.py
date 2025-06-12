from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from pydantic import BaseModel
from typing import List

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
    features: List[str]

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
@app.post("/myFirstCollection", status_code=201)
def add_category(category: Category = Body(...)):
    db = get_db()

    # Ensure custom ID is unique
    if db["myFirstCollection"].find_one({"id": category.id}):
        raise HTTPException(status_code=400, detail="Category with this ID already exists")

    result = db["myFirstCollection"].insert_one(category.dict())
    return {"message": "Category added", "inserted_id": str(result.inserted_id)}


# -----------------------------
# 🔍 Get Category by Business ID
# -----------------------------
@app.get("/myFirstCollection/{category_id}", response_model=Category)
def get_category(category_id: int):
    db = get_db()
    category = db["myFirstCollection"].find_one({"id": category_id})

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return {
        "id": category["id"],
        "name": category["name"],
        "description": category["description"]
    }

@app.get("/myFirstCollection/{category_id}/products", response_model=List[Product])
def get_products_by_category(category_id: int):
    db = get_db()

    # 1. Get the category name from the ID
    category_doc = db["myFirstCollection"].find_one({"id": category_id})
    if not category_doc:
        raise HTTPException(status_code=404, detail="Category not found")

    category_name = category_doc["name"]

    # 2. Find all products in that category
    products_cursor = db["products"].find({"category": category_name})
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
        })

    return products

# -----------------------------
# 🔁 Update Category by Business ID
# -----------------------------
@app.put("/myFirstCollection/{category_id}")
def update_category(category_id: int, updated_data: Category):
    db = get_db()
    result = db["myFirstCollection"].update_one(
        {"id": category_id},
        {"$set": updated_data.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category updated successfully"}


# -----------------------------
# ❌ Delete Category by Business ID
# -----------------------------
@app.delete("/myFirstCollection/{category_id}")
def delete_category(category_id: int):
    db = get_db()
    result = db["myFirstCollection"].delete_one({"id": category_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}
