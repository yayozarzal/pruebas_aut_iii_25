from fastapi.testclient import TestClient
from app.main import app

import time
import json
client = TestClient(app)

def test_e2e_full_categoria_lifecycle():
        # paso 1 obtener la lista inicial de categorías
    cat_nombre = f"E2E Categoria {int(time.time())}"
    respones_get_initial = client.get("/categorias")
    initial_list = respones_get_initial.json()
    initial_count = len(initial_list)
    print ("\nLista inicial de las categorías:\n")
    print (json.dumps (initial_list, indent=4))
    print ("--------------------------------------------------- \n")
    
    print (f"Numero de categorías iniciales: {initial_count}")
    # paso 2 crear una nueva categoría
    response_post = client.post(
        "/categorias", params = {"nombre": cat_nombre})
    assert response_post.status_code == 200
    categoria_creada = response_post.json()
    
    print (f"\n E2E Categoría creada:\n")
    print (json.dumps (categoria_creada, indent=4))
    print ("--------------------------------------------------- \n")
    
    #paso 3 verificar que la categoría creada esté en la lista despues del post
    response_get_final = client.get ("/categorias")
    lista_final = response_get_final.json()
    
    print ("\n E2ELista final de las categorías después de la creación:\n")
    print (json.dumps (lista_final, indent=4))
    print (f"numero de categorías finales: {len(lista_final)}")
    assert len (lista_final) == initial_count + 1
    assert any (cat["id"] == categoria_creada["id"] for cat in lista_final)
    


       