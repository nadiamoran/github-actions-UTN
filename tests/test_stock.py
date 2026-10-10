"""POST /admin/api/productos/comprar/:id y /devolver/:id (manejo de stock)"""
import requests


def test_comprar_descuenta_la_cantidad_pedida(api_url, stock_de):
    resp = requests.post(f"{api_url}/admin/api/productos/comprar/1", json={"cantidad": 2})

    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    assert stock_de(1) == 3  # 5 - 2


def test_devolver_suma_la_cantidad_al_stock(api_url, stock_de):
    resp = requests.post(f"{api_url}/admin/api/productos/devolver/3", json={"cantidad": 2})

    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert stock_de(3) == 5  # 3 + 2


def test_comprar_y_devolver_deja_el_stock_igual(api_url, stock_de):
    requests.post(f"{api_url}/admin/api/productos/comprar/1", json={"cantidad": 4})
    requests.post(f"{api_url}/admin/api/productos/devolver/1", json={"cantidad": 4})

    assert stock_de(1) == 5


def test_comprar_mas_que_el_stock_no_deja_stock_negativo(api_url, stock_de):
    resp = requests.post(f"{api_url}/admin/api/productos/comprar/3", json={"cantidad": 10})

    assert resp.status_code != 200
    assert stock_de(3) == 3


def test_comprar_producto_inexistente_da_404(api_url):
    resp = requests.post(f"{api_url}/admin/api/productos/comprar/999", json={"cantidad": 1})

    assert resp.status_code == 404
    assert resp.json() == {"success": False, "message": "Producto no encontrado"}


def test_devolver_producto_inexistente_da_404(api_url):
    resp = requests.post(f"{api_url}/admin/api/productos/devolver/999", json={"cantidad": 1})

    assert resp.status_code == 404
    assert resp.json()["success"] is False
