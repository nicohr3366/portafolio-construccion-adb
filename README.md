# Portafolio Construcción – Alexander Drada

Sitio web portafolio para **Alexander Drada, Construcciones y Remodelaciones**.
Proyecto de Ingeniería de Requisitos – Universidad de San Buenaventura Cali.

## Equipo
| Rol | Persona | Rama de trabajo |
|---|---|---|
| Product Owner | Valeria Drada | (no programa) |
| Scrum Master | Nicolás Hernández | `dev/nicolas` |
| Developer | Camilo Piedrahita | `dev/camilo` |
| Developer | Juan Felipe Vergara | `dev/juan-felipe` |

## Qué hay en el repositorio
- `docs/` – documento de requisitos, presupuesto, Planning Poker y prototipo.
- `specs/` – una especificación por historia de usuario (HU) con sus criterios de aceptación. Se escribe **antes** de programar (Spec Development).
- `CONTRIBUTING.md` – cómo trabajar con las ramas.

## Cómo ejecutar el proyecto
Requisitos: Python 3.13 y Git. Los comandos son para PowerShell en Windows.

1. Clonar el repositorio y entrar a tu rama personal:
   ```powershell
   git clone <URL-del-repositorio>
   cd portafolio-construccion-adb
   git checkout dev/tu-nombre
   ```
2. Crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   Si PowerShell bloquea el script, ejecutar una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repetir la activación.
3. Instalar las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Crear tu archivo `.env` a partir del ejemplo:
   ```powershell
   Copy-Item .env.example .env
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Copiar la clave que imprime el comando y pegarla en `.env` después de `SECRET_KEY=`.
5. Crear la base de datos local y un usuario administrador:
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. Iniciar el servidor y abrir http://127.0.0.1:8000/ (el panel del propietario está en `/panel/`):
   ```powershell
   python manage.py runserver
   ```

Para correr las pruebas:
```powershell
python manage.py test
```

Si `requirements.txt` cambia después de un `git pull`, volver a ejecutar `pip install -r requirements.txt` con el entorno virtual activado.

## Panel del propietario
El propietario agrega y organiza los proyectos de la galería desde un panel, sin tocar el código. Usa el administrador de Django porque ya trae inicio de sesión seguro, sesiones, protección CSRF y permisos.

- **Dirección:** http://127.0.0.1:8000/panel/ (la dirección `/admin/` no existe). El menú público no enlaza al panel.
- **Quién entra:** solo usuarios con usuario y contraseña. Sin iniciar sesión no se ve nada del panel.
- **Crear el usuario del propietario** (una vez en cada equipo, con el entorno virtual activado):
  ```powershell
  python manage.py migrate
  python manage.py createsuperuser
  ```
  El comando pide un usuario y una contraseña. Elige los tuyos en el momento: **nunca** se guardan en el código, en los specs, en el `.env` ni en un Pull Request.
- **Cargar los proyectos de ejemplo** (fotos marcador provisionales, para ver la galería llena):
  ```powershell
  python manage.py cargar_proyectos_ejemplo
  ```
  Si ya existen y quieres volver a crearlos: `python manage.py cargar_proyectos_ejemplo --reiniciar`.
- **Agregar un proyecto:** en el panel, `Proyectos` → `Añadir proyecto`. Se escribe el nombre, se escoge el servicio de la lista y se escribe la descripción. La dirección web se llena sola. Cada foto se marca como «Antes», «Proceso» o «Después»; hace falta al menos una foto (JPG, PNG o WEBP, de hasta 5 MB) y solo una puede ser la foto principal.
- **Comprobar que quedó publicado:** después de guardar, el proyecto aparece en `/galeria/`. Dentro del proyecto, en el panel, el botón «Ver en el sitio» abre su página pública.

Las fotos subidas se guardan en `media/`, que no se sube a Git.

## Estructura del proyecto
```
config/       configuración de Django (settings, urls principales)
sitio/        app principal: vistas, rutas, modelos y pruebas
templates/    plantillas compartidas (base.html y partials/)
static/       archivos estáticos del proyecto (css, js, imágenes del sitio)
media/        imágenes subidas desde el panel (no se sube a Git)
docs/         documentación del proyecto
specs/        especificaciones de las historias de usuario
```

## Plan de sprints (fechas por confirmar)
| Sprint | Historias de usuario | Horas |
|---|---|---|
| 1 | HU-01, 02, 03, 04, 05, 06, 09, 10 | 40 |
| 2 | HU-11, 12, 13, 14, 15, 16, 24, 25, 26, 30 | 70 |
| 3 | HU-17 a HU-23 | 32 |
| 4 | HU-27, 28, 29, 31, 32, 33 | 30 |
| 5 | HU-07, 08, 34 a 38 | 42 |

El detalle de cada HU está en el tablero de Trello **Sprints**.
