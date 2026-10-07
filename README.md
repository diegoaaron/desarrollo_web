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

Esta guía explica cómo levantar el proyecto en una computadora **sin nada instalado**,
usando **IntelliJ IDEA** para manejar backend y frontend desde un solo lugar. Si
prefieres la terminal, mira la [sección 4](#4-alternativa-levantar-todo-desde-la-terminal).

---

## 1. Paso 0 — Instalar las herramientas

Instala todo esto una sola vez. Al terminar, **reinicia la computadora**.

| Herramienta | Versión | Para qué | Comprobar con |
|---|---|---|---|
| [Git](https://git-scm.com/download/win) | cualquiera | clonar el repositorio | `git --version` |
| [Node.js](https://nodejs.org/) | **22 LTS o superior** (incluye npm) | frontend | `node -v` y `npm -v` |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | cualquiera reciente | base de datos PostgreSQL | `docker --version` |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/download/) | 2025.2 o superior | IDE para backend y frontend | — |

**Node.js.** Descarga el instalador *LTS* (`.msi`) y acepta las opciones por defecto.
No hace falta marcar "Tools for Native Modules".

**Docker Desktop.** En Windows necesita **WSL 2**. Si el instalador lo pide o Docker no
arranca, abre PowerShell **como administrador**, ejecuta `wsl --install` y reinicia.
Después abre Docker Desktop y espera a que diga *Engine running*: **tiene que estar
abierto cada vez que trabajes** en el proyecto.

**IntelliJ IDEA y licencia de estudiante.** El soporte de React y Spring Boot es de la
edición de pago, que es gratis para estudiantes:

1. Pide la licencia en <https://www.jetbrains.com/student/> con tu **correo de la UTP**.
   Queda asociada a tu cuenta de JetBrains, no a una computadora.
2. Instala IntelliJ IDEA (la versión normal, **no** la antigua *Community Edition*, que
   es otro programa y no acepta licencias).
3. Al abrirlo: **Help → Register…** (o *Manage Licenses* en la pantalla de bienvenida) →
   **Activate IntelliJ IDEA** → **JetBrains Account** → **Log In…**. Entra en el navegador
   con tu cuenta, vuelve al IDE, elige *JetBrains Student License* y **Activate**.

> **Java y Maven no hace falta instalarlos aparte.** IntelliJ descarga el JDK 21 (paso 2)
> y el backend trae el *wrapper* de Maven (`mvnw`).

Comprueba en una terminal nueva que `git --version`, `node -v` y `docker --version`
responden.

---

## 2. Levantar el proyecto con IntelliJ

### Paso 1 — Clonar y abrir el proyecto

En la pantalla de bienvenida de IntelliJ: **Clone Repository** (o **File → New →
Project from Version Control**) con la URL:

```
https://github.com/diegoaaron/desarrollo_web.git
```

Si ya lo clonaste con `git clone`, usa **File → Open…** y elige la carpeta
`desarrollo_web`.

> **Abre siempre la carpeta raíz** `desarrollo_web`, no `backend/` ni `frontend/` por
> separado. Cuando pregunte, elige **Trust Project**.

### Paso 2 — JDK 21

**File → Project Structure… → Project → SDK → Download JDK…** → versión **21**,
proveedor *Eclipse Temurin* → **Download** → **OK**.

### Paso 3 — Cargar el backend como proyecto Maven

IntelliJ suele detectar el backend solo: en el árbol aparece como
`backend [coral-shop-backend]`. En ese caso:

clic derecho en `backend/pom.xml` → **Maven → Sync Project**

Descarga las dependencias (barra de progreso abajo a la derecha). Al terminar,
`backend/src/main/java` se pinta de azul y en `CoralShopBackendApplication.java` no
hay nada en rojo.

> Si en el menú no aparece **Maven**, sino **Add as Maven Project**, es que no lo
> detectó: elige esa opción.
>
> Si sale todo en rojo o un error tipo *release version 21 not supported*, falta el
> JDK del paso 2. Descárgalo y repite **Sync Project**.

### Paso 4 — Levantar la base de datos

Con Docker Desktop abierto, en la terminal de IntelliJ (**View → Tool Windows →
Terminal**) ejecuta, **en una sola línea**:

```powershell
docker run -d --name coralshop-db -e POSTGRES_DB=coralshop -e POSTGRES_USER=coralshop -e POSTGRES_PASSWORD=coralshop -p 5432:5432 postgres:16
```

Eso se hace **una sola vez**: crea el contenedor. Las siguientes veces basta con:

```bash
docker start coralshop-db     # encender
docker stop coralshop-db      # apagar
```

No hace falta crear tablas: **el backend las crea solo al arrancar** (Flyway aplica las
migraciones de `backend/src/main/resources/db/migration/`, que también cargan roles,
categorías, tallas y colores iniciales).

### Paso 5 — Ejecutar el backend (API en `http://localhost:8082`)

1. Abre `backend/src/main/java/com/coralshop/CoralShopBackendApplication.java` y dale al
   **▶ verde** junto a `main`. **La primera vez falla** con
   `Could not resolve placeholder 'DB_URL'`: es normal, faltan las variables de entorno.
2. Arriba a la derecha, haz clic en el desplegable **CoralShopBackendApplication ⌄**
   (a la izquierda del ▶; **no** en el engranaje) → **Edit Configurations…**.
3. El campo de variables viene oculto: **Modify options** → sección *Operating System* →
   **Environment variables** (atajo **Alt+E**). Aparece un campo nuevo; pega:

   ```
   DB_URL=jdbc:postgresql://localhost:5432/coralshop;DB_USER=coralshop;DB_PASSWORD=coralshop
   ```

4. Deja **sin marcar** *Store as project file* (guardaría la contraseña en `.idea/`).
   **Apply → OK** y dale otra vez al **▶**.

Está listo cuando el log dice `Started CoralShopBackendApplication`. Compruébalo en
<http://localhost:8082/api/health>.

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DB_URL` | sí | URL JDBC de PostgreSQL |
| `DB_USER` | sí | usuario de la base |
| `DB_PASSWORD` | sí | contraseña de la base |
| `CJ_API_KEY` | no | clave de CJ Dropshipping; solo la usa la importación de productos del panel admin (se agrega al mismo campo separada por `;`) |

### Paso 6 — Ejecutar el frontend (tienda en `http://localhost:5173`)

1. Por defecto el frontend envía las llamadas `/api` al backend publicado en la nube.
   Para que use **tu backend local**, crea el archivo `frontend/.env.local` (clic
   derecho en `frontend` → **New → File**) con esta línea:

   ```env
   API_PROXY_TARGET=http://localhost:8082
   ```

   (`.env.local` no se sube al repositorio.)
2. Instala las dependencias, **solo la primera vez** o cuando cambie `package.json`. En
   la terminal de IntelliJ:

   ```bash
   cd frontend
   npm install
   ```

3. Abre `frontend/package.json` y dale al **▶** que aparece junto al script `"dev"`.
4. Abre <http://localhost:5173>.

> Si creas o cambias `.env.local` con el frontend corriendo, detenlo (■) y vuelve a
> darle al ▶: Vite solo lee ese archivo al arrancar.

### Paso 7 — (Opcional) Ver la base de datos desde IntelliJ

Ventana **Database** (barra derecha) → **+ → Data Source → PostgreSQL**:

| Campo | Valor |
|---|---|
| Host / Port | `localhost` / `5432` |
| Database | `coralshop` |
| User / Password | `coralshop` / `coralshop` |

Si avisa que falta el driver, **Download Driver Files** → **Test Connection** → **OK**.
Desde ahí puedes ver las tablas y ejecutar SQL (por ejemplo, el `UPDATE` de la
sección 3).

### Resumen del día a día

Una vez configurado, cada vez que trabajes: abrir Docker Desktop →
`docker start coralshop-db` → ▶ del backend → ▶ del frontend.

---

## 3. Primer uso: crear un administrador

1. En la tienda, entra a **Sign up** (<http://localhost:5173/register>) y crea una
   cuenta. Toda cuenta nueva tiene el rol `ROLE_USER`.
2. Para dar acceso al panel de administración, cambia su rol a `ROLE_ADMIN` (id 1),
   desde la ventana *Database* de IntelliJ o con:

   ```powershell
   docker exec -it coralshop-db psql -U coralshop -d coralshop -c "UPDATE users SET role_id = 1 WHERE username = 'TU_USUARIO';"
   ```

3. Cierra sesión y vuelve a entrar.

> Usa siempre datos ficticios. No registres datos personales reales.

---

## 4. Alternativa: levantar todo desde la terminal

Requiere además el [JDK 21](https://adoptium.net/) instalado, con `JAVA_HOME` apuntando
a él (`java -version` debe mostrar 21). La base de datos se levanta igual que en el
paso 4.

**Backend — Windows (PowerShell)**

```powershell
cd backend
$env:DB_URL = "jdbc:postgresql://localhost:5432/coralshop"
$env:DB_USER = "coralshop"
$env:DB_PASSWORD = "coralshop"
.\mvnw.cmd spring-boot:run
```

**Backend — macOS / Linux / Git Bash**

```bash
cd backend
export DB_URL=jdbc:postgresql://localhost:5432/coralshop
export DB_USER=coralshop
export DB_PASSWORD=coralshop
./mvnw spring-boot:run
```

**Frontend** (en otra terminal, con `frontend/.env.local` creado como en el paso 6)

```bash
cd frontend
npm install        # solo la primera vez
npm run dev
```

> **Sin Docker** también funciona: instala [PostgreSQL 16](https://www.postgresql.org/download/)
> y crea a mano la base `coralshop` con usuario y contraseña `coralshop`.

---

## 5. Comandos útiles

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

En Windows usa `.\mvnw.cmd` en lugar de `./mvnw`. En IntelliJ, estos mismos objetivos
están en la ventana **Maven** (barra derecha) → *Lifecycle*.

---

## 6. Generar los entregables (opcional)

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

## 7. Problemas frecuentes

| Síntoma | Causa probable / solución |
|---|---|
| IntelliJ no ofrece activar licencia | Está instalada la *Community Edition*. Instala la versión normal de IntelliJ IDEA (paso 0). |
| En el menú de `pom.xml` no está *Add as Maven Project* | Ya está enlazado (se ve `backend [coral-shop-backend]`). Usa **Maven → Sync Project** (paso 3). |
| Código del backend en rojo / *release version 21 not supported* | Falta el JDK 21: paso 2 y luego **Sync Project**. |
| No aparece el campo *Environment variables* | Está oculto: **Modify options → Environment variables** (Alt+E) en *Edit Configurations* (paso 5). |
| `Could not resolve placeholder 'DB_URL'` | Faltan las variables de entorno del paso 5. |
| `JAVA_HOME environment variable is not defined correctly` | Solo en terminal: no hay JDK 21 o `JAVA_HOME` no apunta a él. |
| `Connection to localhost:5432 refused` | La base no está encendida: abre Docker Desktop y `docker start coralshop-db`. |
| `docker: error during connect` / *cannot find the file specified* | Docker Desktop está cerrado o no terminó de arrancar. |
| Docker Desktop no arranca / pide WSL | `wsl --install` en PowerShell como administrador y reinicia. |
| `port is already allocated` al crear el contenedor | Ya hay un PostgreSQL en el puerto 5432. Usa `-p 5433:5432` y cambia `DB_URL` a `...localhost:5433/...`. |
| `Conflict. The container name "/coralshop-db" is already in use` | El contenedor ya existe: no repitas `docker run`, usa `docker start coralshop-db`. |
| `Port 8082 was already in use` | El backend ya está corriendo (otra pestaña de *Run*) u otro proceso usa el puerto. |
| El comando `docker run` falla en PowerShell con varias líneas | Escríbelo en una sola línea, como en el paso 4. |
| `npm` no se reconoce | Node.js no está instalado o falta reiniciar IntelliJ/la PC tras instalarlo. |
| El frontend muestra datos pero no los tuyos | Falta `frontend/.env.local`; está usando el backend de la nube. Reinicia el frontend después de crearlo. |
| `./mvnw: Permission denied` (macOS/Linux) | `chmod +x mvnw` |

---

## Equipo — Grupo 1

- Choquehuanca Marrufo, Liam Lennon
- Damián Valdivia, Diego Aarón
- Loayza Gerónimo, Juan Franco
- Villanueva Montalvo, Apolo Chris
- Campos Sulca, Jian Pier

Docente: Ronald Fernando Medina Cabrera · Universidad Tecnológica del Perú · 2026
