# Datos de ejemplo hasta tener el modelo de proyectos (HU-25, HU-29).
SERVICIOS = [
    {
        'slug': 'construccion-desde-cero',
        'nombre': 'Construcción desde cero',
        'descripcion_corta': 'Obra nueva, desde los cimientos hasta los acabados.',
        'descripcion': (
            'Hacemos la obra nueva desde los cimientos hasta los acabados. '
            'Coordinamos el trabajo para que la construcción avance en orden '
            'y quede lista para usar.'
        ),
        'foto': 'img/servicios/construccion-desde-cero.svg',
    },
    {
        'slug': 'remodelacion',
        'nombre': 'Remodelación',
        'descripcion_corta': (
            'Renovamos espacios de tu casa o local para darles un nuevo uso '
            'o una nueva cara.'
        ),
        'descripcion': (
            'Renovamos espacios de tu casa o de tu local. Cambiamos la '
            'distribución, los materiales o el aspecto general para darle un '
            'nuevo uso o una nueva cara al espacio.'
        ),
        'foto': 'img/servicios/remodelacion.svg',
    },
    {
        'slug': 'estuco',
        'nombre': 'Estuco',
        'descripcion_corta': (
            'Preparamos y alisamos muros y techos para dejarlos listos para pintar.'
        ),
        'descripcion': (
            'Preparamos y alisamos muros y techos. Dejamos la superficie pareja '
            'para que la pintura se aplique sobre una base limpia y lista.'
        ),
        'foto': 'img/servicios/estuco.svg',
    },
    {
        'slug': 'pintura',
        'nombre': 'Pintura',
        'descripcion_corta': (
            'Pintura de interiores y exteriores con un acabado parejo y limpio.'
        ),
        'descripcion': (
            'Pintamos interiores y exteriores. Buscamos un acabado parejo y '
            'limpio, cuidando los detalles de cada superficie.'
        ),
        'foto': 'img/servicios/pintura.svg',
    },
    {
        'slug': 'pisos',
        'nombre': 'Pisos',
        'descripcion_corta': 'Instalación de pisos para interiores y exteriores.',
        'descripcion': (
            'Instalamos pisos para interiores y exteriores. Preparamos la base '
            'y colocamos el material según el uso que tendrá el espacio.'
        ),
        'foto': 'img/servicios/pisos.svg',
    },
    {
        'slug': 'carpinteria',
        'nombre': 'Carpintería',
        'descripcion_corta': 'Trabajos en madera hechos a la medida de tu espacio.',
        'descripcion': (
            'Hacemos trabajos en madera a la medida del espacio. Armamos y '
            'ajustamos las piezas para que encajen con las medidas reales del lugar.'
        ),
        'foto': 'img/servicios/carpinteria.svg',
    },
    {
        'slug': 'cerrajeria-en-aluminio',
        'nombre': 'Cerrajería en aluminio',
        'descripcion_corta': 'Ventanas, puertas y estructuras en aluminio.',
        'descripcion': (
            'Trabajamos ventanas, puertas y estructuras en aluminio. Las piezas '
            'se toman con las medidas del espacio para que queden bien ajustadas.'
        ),
        'foto': 'img/servicios/cerrajeria-en-aluminio.svg',
    },
    {
        'slug': 'divisiones-de-bano',
        'nombre': 'Divisiones de baño',
        'descripcion_corta': (
            'Divisiones para duchas y baños, a la medida del espacio.'
        ),
        'descripcion': (
            'Instalamos divisiones para duchas y baños. Cada división se hace a '
            'la medida del espacio disponible.'
        ),
        'foto': 'img/servicios/divisiones-de-bano.svg',
    },
    {
        'slug': 'asesoria-en-acabados',
        'nombre': 'Asesoría en acabados',
        'descripcion_corta': 'Te orientamos para elegir los acabados de tu obra.',
        'descripcion': (
            'Te orientamos para elegir los acabados de tu obra. Revisamos las '
            'opciones y te ayudamos a decidir según lo que necesitas.'
        ),
        'foto': 'img/servicios/asesoria-en-acabados.svg',
    },
]


def opciones_servicio():
    return [(item['slug'], item['nombre']) for item in SERVICIOS]


def nombre_servicio(slug):
    for item in SERVICIOS:
        if item['slug'] == slug:
            return item['nombre']
    return ''
