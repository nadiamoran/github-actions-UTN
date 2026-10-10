"""Login del backoffice y protección de rutas de administración"""
import requests

# Usuario admin que crea el backend al arrancar (backend/bin/www)
ADMIN = {"email": "admin@admin.com", "password": "1234"}


def test_dashboard_sin_sesion_redirige_al_login(api_url):
    resp = requests.get(f"{api_url}/admin/dashboard", allow_redirects=False)

    assert resp.status_code == 302
    assert resp.headers["Location"] == "/admin/login"


def test_crear_producto_sin_sesion_redirige_al_login(api_url):
    resp = requests.get(f"{api_url}/admin/productos/crear", allow_redirects=False)

    assert resp.status_code == 302
    assert resp.headers["Location"] == "/admin/login"


def test_login_correcto_da_acceso_al_dashboard(api_url):
    sesion = requests.Session()

    resp = sesion.post(f"{api_url}/admin/login", data=ADMIN, allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/admin/dashboard"

    # Con la cookie de sesión ya se puede entrar al dashboard
    dashboard = sesion.get(f"{api_url}/admin/dashboard", allow_redirects=False)
    assert dashboard.status_code == 200
    assert "Batman Año Uno" in dashboard.text


def test_login_con_password_incorrecta_muestra_error(api_url):
    resp = requests.post(
        f"{api_url}/admin/login",
        data={"email": ADMIN["email"], "password": "incorrecta"},
        allow_redirects=False,
    )

    assert resp.status_code == 200
    assert "Usuario o contraseña incorrectos" in resp.text


def test_login_con_usuario_inexistente_muestra_error(api_url):
    resp = requests.post(
        f"{api_url}/admin/login",
        data={"email": "nadie@test.com", "password": "1234"},
        allow_redirects=False,
    )

    assert "Usuario o contraseña incorrectos" in resp.text


def test_sesion_de_cliente_por_defecto_es_invitado(api_url):
    resp = requests.get(f"{api_url}/admin/api/session")

    assert resp.json() == {"nombre": "Invitado"}
