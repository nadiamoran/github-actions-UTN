"""
Fixtures compartidas de la suite.

Los tests son de caja negra: le pegan por HTTP al backend Express ya levantado
(API_URL) y usan una conexión directa a MySQL para preparar datos y verificar
el estado de la base después de cada request.
"""
import os
import time
from pathlib import Path

import pymysql
import pytest
import requests
from dotenv import load_dotenv

# En local se reutiliza el .env del proyecto; en CI las variables vienen del workflow
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_URL = os.getenv("API_URL", f"http://localhost:{os.getenv('PORT', '3000')}")

# Imagen PNG de 1x1 px para probar el endpoint de imágenes
PNG_1PX = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000d49444154789c63000100000500010d0a2db40000000049454e44ae426082"
)

# Productos que se cargan antes de cada test:
# (id, nombre, descripcion, precio, stock, activo, categoria, imagen, mimetype)
PRODUCTOS_SEED = [
    (1, "Batman Año Uno", "Cómic clásico", 1500.00, 5, True, "Comic", PNG_1PX, "image/png"),
    (2, "Watchmen", "Novela gráfica", 2500.50, 0, True, "Comic", None, None),
    (3, "Figura Spider-Man", "Figura articulada", 8000.00, 3, True, "Figura", None, None),
    (4, "Producto dado de baja", "Baja lógica", 100.00, 10, False, "Figura", None, None),
]


@pytest.fixture(scope="session")
def api_url():
    """Espera a que el backend responda antes de empezar la suite."""
    limite = time.time() + 60
    while time.time() < limite:
        try:
            if requests.get(f"{API_URL}/admin/api/productos", timeout=2).ok:
                return API_URL
        except requests.ConnectionError:
            pass
        time.sleep(1)
    pytest.exit(f"El backend no respondió en {API_URL}", returncode=1)


@pytest.fixture(scope="session")
def db():
    conexion = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield conexion
    conexion.close()


@pytest.fixture(autouse=True)
def productos_seed(api_url, db):
    """Deja la tabla productos en un estado conocido antes de cada test."""
    with db.cursor() as cur:
        cur.execute("DELETE FROM productos")
        cur.executemany(
            "INSERT INTO productos "
            "(id, nombre, descripcion, precio, stock, activo, categoria, imagen, mimetype, createdAt, updatedAt) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())",
            PRODUCTOS_SEED,
        )


@pytest.fixture
def stock_de(db):
    """Devuelve una función que lee el stock actual de un producto en la base."""
    def leer(producto_id):
        with db.cursor() as cur:
            cur.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
            return cur.fetchone()["stock"]
    return leer
