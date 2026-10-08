"""GET /admin/api/productos y GET /admin/producto/imagen/:id"""
import requests


def test_lista_solo_productos_activos(api_url):
    resp = requests.get(f"{api_url}/admin/api/productos")

    assert resp.status_code == 200
    cuerpo = resp.json()
    assert cuerpo["success"] is True
    assert cuerpo["count"] == 3
    nombres = {p["nombre"] for p in cuerpo["data"]}
    assert nombres == {"Batman Año Uno", "Watchmen", "Figura Spider-Man"}


def test_no_expone_la_imagen_binaria_y_agrega_url(api_url):
    productos = requests.get(f"{api_url}/admin/api/productos").json()["data"]

    for producto in productos:
        assert "imagen" not in producto
        assert producto["imagenUrl"] == f"/admin/producto/imagen/{producto['id']}"


def test_devuelve_los_campos_del_producto(api_url):
    productos = requests.get(f"{api_url}/admin/api/productos").json()["data"]
    batman = next(p for p in productos if p["id"] == 1)

    assert batman["categoria"] == "Comic"
    assert batman["stock"] == 5
    assert float(batman["precio"]) == 1500.00


def test_sirve_la_imagen_guardada_en_la_base(api_url):
    resp = requests.get(f"{api_url}/admin/producto/imagen/1")

    assert resp.status_code == 200
    assert resp.headers["Content-Type"].startswith("image/png")
    assert resp.content.startswith(b"\x89PNG")


def test_producto_sin_imagen_da_404(api_url):
    resp = requests.get(f"{api_url}/admin/producto/imagen/2")

    assert resp.status_code == 404
