# tests/test_e2e_product_lifecycle.py
from fastapi.testclient import TestClient
from app.main import app
import time
import json

client = TestClient(app)

def test_e2e_full_producto_lifecycle():
    # 🔹 Paso 0: crear una categoría de apoyo para el producto
    cat_nombre = f"E2E Categoria Prod {int(time.time())}"
    response_cat = client.post("/categorias", params={"nombre": cat_nombre})
    assert response_cat.status_code == 200
    categoria_creada = response_cat.json()
    categoria_id = categoria_creada["id"]

    print("\n[E2E PROD] Categoría creada para asociar productos:\n")
    print(json.dumps(categoria_creada, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    # 🔹 Paso 1: obtener lista inicial de productos
    response_get_initial = client.get("/productos")
    initial_list = response_get_initial.json()
    initial_count = len(initial_list)

    print("[E2E PROD] Lista inicial de productos:\n")
    print(json.dumps(initial_list, ensure_ascii=False, indent=4))
    print(f"Número de productos iniciales: {initial_count}")
    print("--------------------------------------------------- \n")

    # 🔹 Paso 2: crear un nuevo producto
    prod_nombre = f"E2E Producto {int(time.time())}"
    response_create = client.post(
        "/productos",
        params={"nombre": prod_nombre, "categoria_id": categoria_id},
    )
    assert response_create.status_code == 200
    producto_creado = response_create.json()
    producto_id = producto_creado["id"]

    print("[E2E PROD] Producto creado:\n")
    print(json.dumps(producto_creado, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    # 🔹 Paso 3: verificar que se incrementó la cantidad de productos
    response_get_after_create = client.get("/productos")
    list_after_create = response_get_after_create.json()

    print("[E2E PROD] Lista de productos después de crear:\n")
    print(json.dumps(list_after_create, ensure_ascii=False, indent=4))
    print(f"Número de productos después de crear: {len(list_after_create)}")
    print("--------------------------------------------------- \n")

    assert len(list_after_create) == initial_count + 1
    assert any(p["id"] == producto_id for p in list_after_create)

    # 🔹 Paso 4: actualizar el producto
    nuevo_nombre = prod_nombre + " ACTUALIZADO"
    response_update = client.put(
        f"/productos/{producto_id}",
        params={"nombre": nuevo_nombre, "categoria_id": categoria_id},
    )
    assert response_update.status_code == 200
    producto_actualizado = response_update.json()

    print("[E2E PROD] Producto actualizado:\n")
    print(json.dumps(producto_actualizado, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    assert producto_actualizado["id"] == producto_id
    assert producto_actualizado["nombre"] == nuevo_nombre
    assert producto_actualizado["categoria_id"] == categoria_id

    # 🔹 Paso 5: verificar en la lista que el nombre esté actualizado
    response_get_after_update = client.get("/productos")
    list_after_update = response_get_after_update.json()

    print("[E2E PROD] Lista de productos después de actualizar:\n")
    print(json.dumps(list_after_update, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    assert any(
        p["id"] == producto_id and p["nombre"] == nuevo_nombre
        for p in list_after_update
    )

    # 🔹 Paso 6: eliminar el producto
    response_delete = client.delete(f"/productos/{producto_id}")
    assert response_delete.status_code == 200
    delete_result = response_delete.json()

    print("[E2E PROD] Resultado de eliminar producto:\n")
    print(json.dumps(delete_result, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    assert delete_result["message"] == "Producto eliminado"
    assert delete_result["producto"]["id"] == producto_id

    # 🔹 Paso 7: verificar que ya no esté en la lista
    response_get_final = client.get("/productos")
    final_list = response_get_final.json()

    print("[E2E PROD] Lista final de productos después de eliminar:\n")
    print(json.dumps(final_list, ensure_ascii=False, indent=4))
    print(f"Número de productos final: {len(final_list)}")
    print("--------------------------------------------------- \n")

    assert not any(p["id"] == producto_id for p in final_list)
