#test_integ_cat_prod.py
from fastapi.testclient import TestClient
from app.main import app
from app import crud
import json

client = TestClient(app)

#restaurar datos de prueba antes de cada prueba

def setup_function():
    data_inicial = {
        "categorias": [{"id": 1, 
                        "nombre": "Electrónica"}],
        "productos": [{"id": 1, 
                       "nombre": "Smartphone", 
                          "categoria_id": 1}]
        
    }
    crud._save_db(data_inicial)
    print("\nBase de datos restaurada a estado inicial para la prueba.\n")
    print(json.dumps(data_inicial, indent=4))
    print("--------------------------------------------------- \n")
    
def test_integration_create_cat_and_product ():
    response_cat = client.post(
        "/categorias",
        params={"nombre": "Celulares"})
    assert response_cat.status_code == 200
    categoria_creada = response_cat.json()
    categoria_id = categoria_creada["id"]
    response_prod = client.post(
        "/productos",
        params={"nombre": "iPhone", "categoria_id": categoria_id})
    assert response_prod.status_code == 200
    producto_creado = response_prod.json()
    final_categoria = client.get("/categorias").json()
    assert any(cat["id"] == categoria_id for cat in final_categoria)
    
    final_data_db = crud._load_db()
    print("\nEstado final de la base de datos después de la prueba de integración:\n")
    print(json.dumps(final_data_db, indent=4))
    print("--------------------------------------------------- \n")
    
    assert producto_creado ["nombre"] == "iPhone"
    assert producto_creado ["categoria_id"] == categoria_id
    