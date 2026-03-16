from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Product Data
# -----------------------------
products = [
    {"product_id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"product_id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"product_id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"product_id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []
order_counter = 1


# -----------------------------
# Order Model
# -----------------------------
class Order(BaseModel):
    customer_name: str
    product_id: int


# -----------------------------
# Create Order
# -----------------------------
@app.post("/orders")
def create_order(order: Order):
    global order_counter

    product = next((p for p in products if p["product_id"] == order.product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product": product["name"],
        "price": product["price"]
    }

    orders.append(new_order)
    order_counter += 1

    return {"message": "Order placed", "order": new_order}


# -----------------------------
# Q1 — Search Products
# -----------------------------
@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }


# -----------------------------
# Q2 — Sort Products
# -----------------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# -----------------------------
# Q3 — Pagination
# -----------------------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    paged = products[start:end]

    total_pages = (len(products) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paged
    }


# -----------------------------
# Q4 — Search Orders by Customer
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# -----------------------------
# Q5 — Sort by Category then Price
# -----------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(products, key=lambda x: (x["category"], x["price"]))

    return {"products": sorted_products}


# -----------------------------
# Q6 — Browse (Search + Sort + Pagination)
# -----------------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    total_found = len(result)

    start = (page - 1) * limit
    end = start + limit

    paged = result[start:end]

    total_pages = (total_found + limit - 1) // limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paged
    }


# -----------------------------
# Bonus — Paginate Orders
# -----------------------------
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    start = (page - 1) * limit
    end = start + limit

    paged = orders[start:end]

    total_pages = (len(orders) + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "orders": paged
    }


# -----------------------------
# Product by ID
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    product = next((p for p in products if p["product_id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
