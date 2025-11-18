# app/main.py
from fastapi import FastAPI, HTTPException
from . import crud

app = FastAPI()

@app.get("/categorias")
def get_all_categorias_route():
    return crud.get_categorias()

@app.post("/categorias")
def create_categoria_route(nombre: str):
    return crud.create_categoria_db(nombre)

@app.get("/productos")
def get_all_productos_route():
    return crud.get_productos()

@app.post("/productos")
def create_producto_route(nombre: str, categoria_id: int):
    producto = crud.create_producto_db(nombre, categoria_id)
    if "error" in producto:
        raise HTTPException(status_code=404, detail=producto["error"])
    return producto

@app.put("/productos/{producto_id}")
def update_producto_route(producto_id: int, nombre: str, categoria_id: int):
    producto = crud.update_producto_db(producto_id, nombre, categoria_id)
    if "error" in producto:
        raise HTTPException(status_code=404, detail=producto["error"])
    return producto

@app.delete("/productos/{producto_id}")
def delete_producto_route(producto_id: int):
    resultado = crud.delete_producto_db(producto_id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado
