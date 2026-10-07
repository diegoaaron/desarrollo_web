# Coral Shop — Proyecto Final · Desarrollo Web Integrado (UTP)

Tienda virtual de ropa juvenil con estampado personalizable. El repositorio contiene
la aplicación completa (frontend + backend) y los generadores de los entregables del
curso.

```
desarrollo_web/
├─ frontend/            Tienda web: React 19 + Vite + Tailwind + React Router
├─ backend/             API REST: Spring Boot 3.5 · Java 21 · PostgreSQL · Flyway
├─ scripts/             Generadores (Python) del informe Word y la presentación
├─ clase_entregables/   Word, PPT y figuras de cada entregable (salida de scripts/)
└─ clase_referencias/   Indicaciones y material notificado por el docente
```

Esta guía explica cómo levantar el proyecto en una computadora nueva.

---

## 1. Requisitos

| Herramienta | Versión | Para qué | Comprobar con |
|---|---|---|---|
| [Git](https://git-scm.com/) | cualquiera | clonar el repositorio | `git --version` |
| [Node.js](https://nodejs.org/) | **22 LTS o superior** (incluye npm) | frontend | `node -v` |
| [Java JDK](https://adoptium.net/) | **21** | backend | `java -version` |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | cualquiera reciente | base de datos PostgreSQL | `docker --version` |

> **Maven no hace falta instalarlo**: el backend trae el *wrapper* (`mvnw`), que
> descarga la versión correcta la primera vez.
>
> **Sin Docker** también funciona: instala [PostgreSQL 16](https://www.postgresql.org/download/)
> y crea a mano la base `coralshop` con el usuario y la contraseña del paso 3.

Si `java -version` no muestra 21, revisa que la variable de entorno `JAVA_HOME`
apunte a la carpeta del JDK 21.

---

## 2. Clonar el repositorio

```bash
git clone https://github.com/diegoaaron/desarrollo_web.git
cd desarrollo_web
```

Todos los comandos que siguen parten de esta carpeta raíz.

---

## 3. Base de datos (PostgreSQL en Docker)

Con Docker Desktop abierto:

```bash
docker run -d --name coralshop-db \
  -e POSTGRES_DB=coralshop \
  -e POSTGRES_USER=coralshop \
  -e POSTGRES_PASSWORD=coralshop \
  -p 5432:5432 \
  postgres:16
```

> En PowerShell reemplaza las `\` del final de línea por un acento grave (`` ` ``) o
> escribe todo el comando en una sola línea.

No hace falta crear tablas: **el backend las crea solo al arrancar** (Flyway aplica las
migraciones de `backend/src/main/resources/db/migration/`, que también cargan roles,
categorías, tallas y colores iniciales).

Las siguientes veces basta con:

```bash
docker start coralshop-db     # encender
docker stop coralshop-db      # apagar
```

---

## 4. Backend (API en `http://localhost:8082`)

El backend lee la conexión a la base desde variables de entorno. Defínelas en la misma
terminal donde lo vas a ejecutar.

**Windows (PowerShell)**

```powershell
cd backend
$env:DB_URL = "jdbc:postgresql://localhost:5432/coralshop"
$env:DB_USER = "coralshop"
$env:DB_PASSWORD = "coralshop"
.\mvnw.cmd spring-boot:run
```

**macOS / Linux / Git Bash**

```bash
cd backend
export DB_URL=jdbc:postgresql://localhost:5432/coralshop
export DB_USER=coralshop
export DB_PASSWORD=coralshop
./mvnw spring-boot:run
```

La primera ejecución tarda unos minutos porque descarga Maven y las dependencias.
Está listo cuando aparece `Started CoralShopBackendApplication`. Compruébalo abriendo
<http://localhost:8082/api/health>.

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DB_URL` | sí | URL JDBC de PostgreSQL |
| `DB_USER` | sí | usuario de la base |
| `DB_PASSWORD` | sí | contraseña de la base |
| `CJ_API_KEY` | no | clave de CJ Dropshipping; solo la usa la importación de productos del panel admin |

Deja esta terminal abierta y usa otra para el frontend.

---

## 5. Frontend (tienda en `http://localhost:5173`)

Por defecto el frontend envía las llamadas `/api` al backend publicado en la nube. Para
que use **tu backend local**, crea el archivo `frontend/.env.local` con esta línea:

```env
API_PROXY_TARGET=http://localhost:8082
```

(`.env.local` no se sube al repositorio.) Luego:

```bash
cd frontend
npm install        # solo la primera vez o cuando cambie package.json
npm run dev
```

Abre <http://localhost:5173>.

---

## 6. Primer uso: crear un administrador

1. En la tienda, entra a **Sign up** (<http://localhost:5173/register>) y crea una cuenta. Toda cuenta nueva tiene el
   rol `ROLE_USER`.
2. Para dar acceso al panel de administración, cambia su rol a `ROLE_ADMIN` (id 1):

   ```bash
   docker exec -it coralshop-db psql -U coralshop -d coralshop \
     -c "UPDATE users SET role_id = 1 WHERE username = 'TU_USUARIO';"
   ```

3. Cierra sesión y vuelve a entrar.

> Usa siempre datos ficticios. No registres datos personales reales.

---

## 7. Comandos útiles

### Frontend (`frontend/`)

| Comando | Qué hace |
|---|---|
| `npm run dev` | servidor de desarrollo con recarga automática |
| `npm run lint` | revisa el código con ESLint |
| `npm run build` | compila para producción en `dist/` (lo que se sube a Vercel u otro hosting) |
| `npm run preview` | sirve `dist/` en local para probar el build |
| `npm run build:compilado` | genera `compilado/index.html`, un único archivo que se abre con doble clic |

El despliegue en Vercel usa `frontend/vercel.json`, que redirige `/api/*` al backend
publicado.

### Backend (`backend/`)

| Comando | Qué hace |
|---|---|
| `./mvnw spring-boot:run` | ejecuta la API |
| `./mvnw test` | ejecuta las pruebas |
| `./mvnw package` | genera el JAR desplegable en `target/` |
| `java -jar target/coral-shop-backend-0.0.1-SNAPSHOT.jar` | ejecuta el JAR (con las mismas variables de entorno) |

En Windows usa `.\mvnw.cmd` en lugar de `./mvnw`.

---

## 8. Generar los entregables (opcional)

Solo hace falta para regenerar el informe y la presentación de `clase_entregables/`.
Requiere **Python 3.12+** y, para exportar a PDF, **Microsoft Office** (Windows).

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.\scripts\generar.ps1            # figuras + informe + presentación + PDFs
.\scripts\generar.ps1 -SinPdf    # sin exportar a PDF (no necesita Office)
```

Los archivos de `clase_entregables/` se regeneran: para cambiarlos se editan los
scripts, no el Word ni la PPT.

---

## 9. Problemas frecuentes

| Síntoma | Causa probable / solución |
|---|---|
| `JAVA_HOME environment variable is not defined correctly` | No hay JDK 21 instalado o `JAVA_HOME` no apunta a él. |
| `Could not resolve placeholder 'DB_URL'` | Faltan las variables del paso 4 en esa terminal. |
| `Connection to localhost:5432 refused` | La base no está encendida: `docker start coralshop-db`. |
| `port is already allocated` al crear el contenedor | Ya hay un PostgreSQL en el puerto 5432. Usa `-p 5433:5432` y cambia `DB_URL` a `...localhost:5433/...`. |
| `Port 8082 was already in use` | Otro proceso usa el puerto; ciérralo o arranca con `--server.port=8083` (y ajusta `API_PROXY_TARGET`). |
| El frontend muestra datos pero no los tuyos | Falta `frontend/.env.local`; está usando el backend de la nube. Reinicia `npm run dev` después de crearlo. |
| `./mvnw: Permission denied` (macOS/Linux) | `chmod +x mvnw` |

---

## Equipo — Grupo 1

- Choquehuanca Marrufo, Liam Lennon
- Damián Valdivia, Diego Aarón
- Loayza Gerónimo, Juan Franco
- Villanueva Montalvo, Apolo Chris
- Campos Sulca, Jian Pier

Docente: Ronald Fernando Medina Cabrera · Universidad Tecnológica del Perú · 2026
