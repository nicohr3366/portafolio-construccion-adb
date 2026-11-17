# Cómo trabajamos con Git

## Ramas
- `main`: versión estable. **Nadie sube directo.** Solo se actualiza al cerrar un sprint.
- `develop`: donde se junta el trabajo de todos.
- `dev/<nombre>`: rama personal de cada integrante (`dev/nicolas`, `dev/camilo`, `dev/juan-felipe`).

## Pasos para empezar (una sola vez)
```bash
git clone <URL-del-repositorio>
cd portafolio-construccion-adb
git checkout dev/tu-nombre        # tu rama personal
```

## Día a día
```bash
git checkout dev/tu-nombre
git pull origin develop           # traer lo último de los demás
# ... trabajas en tu HU ...
git add .
git commit -m "HU-01: encabezado con logo y menú"
git push origin dev/tu-nombre
```

## Entregar una HU
1. En GitHub abre un **Pull Request** de `dev/tu-nombre` hacia `develop`.
2. Otra persona del equipo lo revisa (revisa contra los criterios de aceptación de la HU).
3. Al aprobarse, se une a `develop` y se mueve la tarjeta en Trello a "Hecho".

## Reglas
- Un commit por avance claro, con el número de la HU al inicio del mensaje.
- Antes de programar una HU, su archivo en `specs/` debe existir.
- No subir contraseñas, claves ni el archivo `.env`.

## Base de datos y migraciones
- `db.sqlite3` y `.env` nunca se suben: cada persona tiene los suyos.
- Las migraciones (`sitio/migrations/`) sí se suben al repositorio.
- Después de cada `git pull`, ejecutar `python manage.py migrate`.
- Si dos personas cambian modelos, avisar al equipo antes de unir las ramas para evitar migraciones en conflicto.
- Los mensajes de commit empiezan con el número de la HU cuando aplique (ejemplo: `HU-01: encabezado del inicio`). Para tareas de base del proyecto usar `Base:` (ejemplo: `Base: configuración de plantillas`).
