from fastapi import FastAPI, HTTPException

app = FastAPI()

# Initial products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# Root
@app.get("/")
def home():
    return {"message": "FastAPI Product API Running"}

# GET all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# POST add product
@app.post("/products", status_code=201)
def add_product(product: dict):

    for p in products:
        if p["name"].lower() == product["name"].lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    product["id"] = len(products) + 1
    products.append(product)

    return {
        "message": "Product added",
        "product": product
    }

# PUT update product
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    for p in products:

        if p["id"] == product_id:

            if price is not None:
                p["price"] = price

            if in_stock is not None:
                p["in_stock"] = in_stock

            return p

    raise HTTPException(status_code=404, detail="Product not found")

# DELETE product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {"message": f"Product '{p['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")

# ⭐ Q5 AUDIT ENDPOINT (MUST BE ABOVE product_id)
@app.get("/products/audit")
def product_audit():

    total_products = len(products)

    in_stock_items = [p for p in products if p["in_stock"]]

    in_stock_count = len(in_stock_items)

    out_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_items)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# ⭐ BONUS DISCOUNT
@app.put("/products/discount")
def category_discount(category: str, discount_percent: int):

    updated = []

    for p in products:

        if p["category"].lower() == category.lower():

            new_price = int(p["price"] * (1 - discount_percent / 100))

            p["price"] = new_price

            updated.append({
                "name": p["name"],
                "new_price": new_price
            })

    if not updated:
        return {"message": "No products found in this category"}

    return {
        "updated_products": len(updated),
        "products": updated
    }

# GET single product
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:

        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")
