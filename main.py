from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import session, engine
import database_models
from models import Product

# create table
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


products = [
    Product(id=1, name="Phone", description="Budget Phone", price=6999, quantity=10),
    Product(id=2, name="Laptop", description="Gaming Laptop", price=70000, quantity=20),
    Product(id=3, name="Table", description="Wooden Table", price=799, quantity=7),
]


@app.get("/")
def greet():
    return {"message": "hello fastapi"}


# ---------------- GET (UNCHANGED LOGIC STYLE) ----------------
@app.get("/products")
def get_all_product(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


# @app.get("/products/{id}")
# def get_product_by_id(id: int, db: Session = Depends(get_db)):
#     for product in products:
#         if product.id == id:
#             return product
#     return "not found"
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    return db_product


# @app.get("/products/by-name/{name}")
# def get_by_name(name: str):
#     for product in products:
#         if product.name.lower() == name.lower():
#             return product
#     return "not found"
@app.get("/products/by-name/{name}")
def get_by_name(name: str, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.name == name).first()
    return db_product


# ---------------- POST (UNCHANGED STYLE) ----------------
# @app.post("/product")
# def add_new_product(product: Product):
#     products.append(product)
#     return product
@app.post("/products")
def add_new_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


# ---------------- PUT (UNCHANGED STYLE) ----------------
# @app.put("/product")
# def update_product(id: int, product: Product):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i] = product
#             return "Bingo"
#     return "update product unsuccessful"
@app.put("/products/{id}")
def update_product(id: int, product: Product,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "Product Not Found"
# ---------------- DELETE (UNCHANGED STYLE) ----------------
# @app.delete("/product")
# def delete_product(id: int):
#     for i in range(len(products)):
#         if products[i].id == id:
#             del products[i]
#             return "Delete product successful"
#     return "Product Not Deleted"
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    else:
        return "Product Not Found"

   