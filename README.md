# Sistema de Autoservicio - Tienda Los Vigilantes

[![CI](https://github.com/nadiamoran/github-actions-UTN/actions/workflows/ci.yml/badge.svg)](https://github.com/nadiamoran/github-actions-UTN/actions/workflows/ci.yml)

## 🧪 Actividad 6: GitHub Actions (Gestión y Desarrollo de Software)

> **Nota:** esta sección la agregó nuestro equipo para la materia **Gestión y Desarrollo de Software**. Todo lo que está más abajo de la línea divisoria es el README original del equipo que desarrolló el proyecto, y se conserva sin cambios.

### Objetivo

La consigna de la Actividad 6 es tomar un repositorio desarrollado por **otro equipo** y aplicarle **integración continua con GitHub Actions**: escribir tests automatizados sobre su código y configurar un workflow que los ejecute en cada pull request, de modo que solo se pueda mergear a `main` código que pasa los tests (*quality gate*).

Elegimos el proyecto **Tienda Los Vigilantes** (Actividad 2 de sus autores): un backend Node.js + Express + Sequelize con base MySQL.

### Integrantes del equipo (Actividad 6)

* [@acostaamericonicolas](https://github.com/acostaamericonicolas)
* [@nadiamoran](https://github.com/nadiamoran)

### Qué hicimos

| Entregable | Archivo(s) | Descripción |
|---|---|---|
| Suite de tests | [`tests/`](tests/) | 17 tests con **pytest** de caja negra sobre la API del backend: le pegan por HTTP al servidor levantado y verifican el estado de MySQL con una conexión directa. |
| Workflow de CI | [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Corre en cada PR contra `main`, en cada push a `main` y de forma manual. |
| Dependencias de test | [`requirements-test.txt`](requirements-test.txt), [`pytest.ini`](pytest.ini) | Versiones fijas de pytest, pytest-html, requests, PyMySQL y python-dotenv. |
| Configuración | [`.env.example`](.env.example), [`.gitignore`](.gitignore) | Variables de entorno de ejemplo para correr local; se ignoran `.env`, `node_modules/` y los reportes. |
| Badge de estado | Este README | Muestra si el último CI de `main` pasó o falló. |
| Corrección de un bug | `backend/controllers/ControllerAdmin.js`, `backend/views/login.ejs` | Bug del proyecto original que encontraron nuestros tests (ver abajo). |

#### Tests incluidos

| Archivo | Qué cubre |
|---|---|
| [`tests/test_auth.py`](tests/test_auth.py) | Rutas de admin protegidas (redirigen al login sin sesión), login correcto, login con contraseña incorrecta o usuario inexistente, sesión de cliente por defecto. |
| [`tests/test_productos_api.py`](tests/test_productos_api.py) | `GET /admin/api/productos` lista solo productos activos, no expone la imagen binaria, agrega `imagenUrl`; `GET /admin/producto/imagen/:id` sirve la imagen o da 404. |
| [`tests/test_stock.py`](tests/test_stock.py) | Compra y devolución de stock (`/comprar/:id`, `/devolver/:id`), que el stock no quede negativo y 404 para productos inexistentes. |

Antes de cada test una fixture (`tests/conftest.py`) vacía y recarga la tabla `productos` con datos conocidos, así cada test es independiente del anterior.

#### Cómo funciona el workflow

1. **Disparadores:** `pull_request` contra `main`, `push` a `main` y `workflow_dispatch` (ejecución manual).
2. **Service container:** levanta **MySQL 8** con *healthcheck*; los steps no arrancan hasta que la base responde.
3. **Node 20 + cache de npm:** instala el backend con `npm ci` y lo arranca en segundo plano (Sequelize crea las tablas y los usuarios de prueba).
4. **Python 3.11 + cache de pip:** instala las dependencias de pytest.
5. Espera a que la API responda y **ejecuta pytest**. Si falla un test, el job termina en rojo y el check del PR falla.
6. **Publica artifacts** (`pytest-report`): reporte HTML, JUnit XML y log del backend. Se suben siempre (`if: always()`), aunque fallen los tests.

Buenas prácticas aplicadas: `concurrency` para cancelar corridas viejas del mismo PR, `permissions: contents: read` (permisos mínimos del token), `timeout-minutes` y credenciales descartables solo para la base efímera del CI.

#### Quality gate

La rama `main` tiene una *branch protection rule* que exige que el check **Tests API (pytest)** pase para habilitar el merge de un PR.

#### Bug encontrado gracias al CI

La primera corrida del workflow ([run #1](https://github.com/nadiamoran/github-actions-UTN/actions/runs/37722354305)) dio **15 tests OK y 2 fallidos**: un login con contraseña incorrecta o con un usuario inexistente devolvía **HTTP 500** en lugar de volver al login con un mensaje de error. La causa era que el controlador renderizaba `login.ejs` sin las variables `title`, `emailTester` y `passwordTester` que la vista necesita, y además la vista nunca mostraba el mensaje de error. Lo corregimos y ahora pasan los 17 tests. Es justamente lo que busca la actividad: que el CI detecte un error antes de que llegue a `main`.

### Cómo correr los tests en local

> ⚠️ Los tests vacían la tabla `productos`: usar siempre una base de **prueba**.

```bash
cp .env.example .env              # completar con los datos de la base de prueba
cd backend && npm ci && npm start # en otra terminal
pip install -r requirements-test.txt
pytest --html=reports/pytest-report.html --self-contained-html
```

---

Originalmente este proyecto era el proyecto final de programación 3 consiste en una aplicación de **Autoservicio** (Kiosco digital) intuitivo donde el usuario no deba escribir ningúna ruta a mano. Contando tambíen con un panel de administración (Backoffice) para la gestión de productos y ventas. 

## 📋 Integrantes del Grupo
* Cristian Iván Collante
    * Github: [@deltron9](https://github.com/deltron9)
    * Linkedin: [Cristian Iván Collante](https://www.linkedin.com/in/cristian-collante-171b04294/)
* Alan Joel Monzón
    * Github: [@kalcifer27](https://github.com/kalcifer27)
    * Linkedin: [Alan Joel Monzón](https://www.linkedin.com/in/alan-joel-monz%C3%B3n-7013a8340/)

## 🚀 Tecnologías Utilizadas

**Backend (backoffice y servidor) y Base de datos:**
* **Node.js & Express**
* **MVC** como patrón de arquitectura
* **Sequelize** como ORM para base de datos
* **MySQL** como base de datos
* **EJS** Motor de plantillas (para el panel de administración)

**Frontend (Cliente):**
* HTML5
* CSS3
* JavaScript

## ⚙️ Funcionalidades

### Cliente (Autoservicio)
* **Logeo mediante teclado virtual:** Teclado virtual en registro de nombre para no tener necesidad de utilizar el teclado.
* **Alojamiento de nombre de cliente y carrito de compras** en Localstorage.
* **Navegación intuitiva:** Selección de productos por tanto por categorías como general.
* **Carrito de compras:** Agregar, eliminar y modificar cantidades en tiempo real.
* **Generación de Ticket:** Al finalizar la compra, se genera un ticket con el detalle (opción de descarga en PDF).
* **Modo Oscuro/Claro:** Persistencia de preferencia de tema.

### 🛠️ Administrador (Backoffice)
* **Acceso oculto:** Botón de acceso oculto mediante combinación de teclas.
* **Login seguro:** Acceso restringido con encriptación de contraseñas.
* **Botón de Acceso Rápido:** Autocompletado de credenciales para testing agil.
* **Dashboard:**
    * CRUD completo de Productos (Alta, Baja lógica, Modificación).
    * Gestión de imágenes de productos.
    * Reactivación de productos eliminados.
* **API:** Endpoints JSON para alimentar la vista del cliente.

## Descarga de imágenes:
* **docker pull deltron9/vigilantes_backend:latest** para la imagen del backend.
* **docker pull deltron9/los-vigilantes-frontend** para la imagen del frontend.
* **docker pull deltron9/bd-app-web** para la base de datos.


## Acceso a sector empleados:
En la pagina de index apretar **CTRL + I** para activar el boton en la navbar que lleva al login de empleados.

## Credenciales de Prueba (Testing):
Para facilitar el acceso, el login en sector de gestión cuenta con una combinacion de **"Modo Tester (CTRL + R)"** que permite el logeo rápido activando una card con credenciales pre-cargadas.
