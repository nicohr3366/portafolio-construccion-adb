# Herramientas de Ingeniería de Requisitos

Comparación de tres herramientas y evaluación práctica de ReqView.

**Curso:** Ingeniería de Requisitos · Universidad de San Buenaventura Cali
**Equipo:** Valeria Drada, Nicolás Hernández, Camilo Piedrahita, Juan Felipe Vergara
**Base:** *Requirements Engineering Tools*, IEEE Software, julio/agosto 2011 (Carrillo de Gea et al.)
**Fecha:** noviembre de 2026

---

## 0. Qué pide la actividad y dónde está resuelto

| Lo que pide el profesor | Dónde está en este documento |
|---|---|
| Elegir tres herramientas del paper (o una nueva) | Sección 3 |
| Analizar cada una en todas las actividades de RE | Sección 4 |
| Comparar costos | Sección 5 |
| Comparar facilidad de uso | Sección 6 |
| Elegir una y evaluarla en la práctica | Sección 7 |
| Instalarla y probarla | Sección 7.1 y 7.2 |
| Hacer una demostración | Sección 10 |
| Recomendar o no su uso | Sección 8 |
| Concluir ventajas y desventajas | Sección 9 |

Lo único que no está aquí son las diapositivas.

---

## 1. Resumen para quien tiene cinco minutos

Se compararon **Visure Requirements ALM**, **Jama Connect** y **ReqView**. Las tres cubren el ciclo de vida de los requisitos, pero apuntan a clientes distintos:

- **Visure** es una plataforma ALM para industrias reguladas (aeroespacial, médico, automotriz). Cubre requisitos, riesgos, pruebas, MBSE y cumplimiento normativo. Se cotiza, no tiene precio público.
- **Jama Connect** es una plataforma SaaS de colaboración y trazabilidad en vivo, con revisión formal y firma electrónica. Tampoco publica precios.
- **ReqView** es una aplicación de escritorio, liviana y barata, que guarda el proyecto en un archivo de texto versionable con Git.

Se eligió **ReqView** para la evaluación práctica porque es la única que se puede instalar y probar sin tarjeta de crédito, sin servidor y sin cotización. Se instaló la versión **2.22.5**, se construyó un proyecto con las **38 historias reales** del portafolio de Alexander Drada y se verificó su comportamiento en el plan gratuito.

**Recomendación:** sí se recomienda ReqView para equipos pequeños y proyectos como el nuestro. No se recomienda para organizaciones que necesiten auditoría, cumplimiento normativo o colaboración web.

---

## 2. Marco de comparación

La Ingeniería de Requisitos es el proceso sistemático de **elicitar, especificar, analizar, validar y gestionar** requisitos a lo largo de todo el ciclo de vida. El paper de 2011 evalúa las herramientas con el cuestionario de la norma **ISO/IEC TR 24766** y las califica en estas categorías: elicitación, análisis, especificación, modelado, verificación y validación, gestión, trazabilidad, otras capacidades y precio global.

Para esta exposición se usan esas mismas categorías, más cuatro que el uso real volvió necesarias: **colaboración y revisión, integraciones, reportes y exportación, y facilidad de uso**.

### Advertencia sobre el paper

El paper tiene dos limitaciones que conviene decir en voz alta:

1. **Es de 2011.** Varias herramientas que aparecen ya no existen o cambiaron de nombre (Rational RequisitePro, Caliber RM, MKS Integrity). Los precios de su Tabla 3 están en dólares de 2011 y con una escala que hoy no aplica (por ejemplo, `$$$$` significa "más de US$1.000").
2. **Los datos los reportaron los propios fabricantes.** Los autores lo reconocen: "the responses could contain bias because representatives tend to rank their own tools positively". Además, varios fabricantes importantes no respondieron secciones completas del cuestionario, entre ellos **IRqA**, que es el nombre con el que aparecía **Visure** en 2011.

Por eso el paper se usa como **punto de partida histórico**, y los datos de funcionalidad y precio se verificaron en los sitios oficiales de cada fabricante en noviembre de 2026.

### Cómo se califica

| Valor | Significado |
|---|---|
| Alta | La herramienta lo hace de forma nativa y es una función central |
| Media | Lo hace, pero con limitaciones, con un complemento de pago o solo por integración |
| Baja | No lo hace, o lo hace de forma muy parcial |
| N/A | No aplica a ese tipo de herramienta |

Las calificaciones de ReqView están respaldadas con la prueba práctica de la sección 7. Las de Visure y Jama salen de la documentación oficial de cada fabricante, no de una prueba propia: eso se indica donde corresponde.

---

## 3. Las tres herramientas

### 3.1 Visure Requirements ALM

- **Fabricante:** Visure Solutions, Inc. (San Francisco, EE. UU.)
- **Nombre en el paper:** IRqA
- **Despliegue:** nube (AWS, Azure) o instalación en servidor propio, incluido modo *air-gapped* sin conexión a internet
- **Tipo:** plataforma ALM de requisitos para industrias reguladas

Cubre gestión de requisitos, trazabilidad, gestión de riesgos, gestión de pruebas, desarrollo guiado por especificación, MBSE y "digital thread". Trae paquetes de cumplimiento para normas concretas: DO-178C y DO-254 (aeroespacial), ISO 26262 y ASPICE (automotriz), IEC 62304, ISO 14971 e ISO 13485 (dispositivos médicos), entre otras. Se integra con Jira, IBM DOORS, Azure DevOps, GitLab, MATLAB/Simulink, Cameo, VectorCAST y ReqIF. Ofrece complementos de pago para análisis de calidad, listas de verificación automáticas, informes y calificación de herramientas.

**En el paper:** su fila es `n/a, n/a, n/a, n/a, ++, ++, ++, +, n/a, n/a`. Es decir, no respondió las secciones de elicitación, análisis, especificación ni modelado, pero se destacó en **verificación y validación, gestión y trazabilidad**. Los autores la mencionan explícitamente como uno de los fabricantes importantes que dejaron secciones sin responder.

**Para quién es:** empresas grandes con auditorías, trazabilidad regulatoria y equipos multidisciplinarios.

### 3.2 Jama Connect

- **Fabricante:** Jama Software (Portland, EE. UU.)
- **Despliegue:** SaaS, con opción on-premise
- **Tipo:** plataforma de gestión de requisitos y trazabilidad en vivo

Su función insignia es **Live Traceability**: las relaciones entre requisitos, pruebas, riesgos y decisiones se actualizan en tiempo real y se pueden recorrer en ambos sentidos. Tiene **Review Center** para ciclos formales de revisión con firma electrónica, gestión de pruebas con ejecución y registro de defectos, paneles de indicadores y API. La licencia se divide en cuatro tipos de usuario: **Creator** (crea y edita), **Stakeholder** (lee y comenta), **Reviewer** (revisa y firma) y **Test Runner** (ejecuta pruebas). El alojamiento y las licencias de revisor no se cobran aparte.

**En el paper:** no aparece. Se incluyó como tercera herramienta porque es el competidor SaaS más citado del mercado actual y porque cubre el extremo de "colaboración" que el paper no alcanzó a recoger.

**Para quién es:** equipos distribuidos de tamaño medio y grande que necesitan revisión formal y trazabilidad compartida.

### 3.3 ReqView

- **Fabricante:** Eccam s.r.o. (República Checa)
- **Despliegue:** aplicación de escritorio para Windows, sin servidor ni base de datos
- **Tipo:** herramienta liviana de gestión de requisitos

El proyecto completo es **un archivo** (`.reqw`, formato JSON abierto) que se puede guardar en Git, Subversion o una carpeta compartida. Trae plantillas de documentos basadas en ISO/IEC/IEEE 29148, Volere, historias de usuario, FMEA y OWASP ASVS. Maneja atributos personalizados, matrices de trazabilidad, verificación y validación, riesgos, historial de cambios, comparación de proyectos, líneas base, enlaces sospechosos (*suspect links*) y exportación a Word, Excel, PDF, HTML, CSV y ReqIF. Se integra con Jira Cloud, Azure DevOps y Sparx Enterprise Architect.

**En el paper:** no aparece. Se incluyó porque representa el extremo económico y liviano del mercado, que es justamente el perfil de nuestro proyecto.

**Para quién es:** equipos pequeños, proyectos académicos, consultores y quienes quieren versionar los requisitos como si fueran código.

---

## 4. Comparación por actividad de Ingeniería de Requisitos

| Actividad | Visure | Jama Connect | ReqView |
|---|---|---|---|
| **Elicitación** | Media | Media | Baja |
| **Análisis** | Alta | Alta | Media |
| **Especificación** | Alta | Alta | Alta |
| **Modelado** | Alta | Media | Baja |
| **Gestión de cambios** | Alta | Alta | Alta |
| **Verificación y validación** | Alta | Alta | Media |
| **Trazabilidad** | Alta | Alta | Alta |
| **Colaboración y revisión** | Alta | Alta | Baja |
| **Integraciones** | Alta | Alta | Media |
| **Reportes y exportación** | Alta | Alta | Alta |

### Por qué cada calificación

**Elicitación.** Ninguna de las tres hace elicitación: eso es trabajo humano (entrevistas, talleres, observación). Lo que hace una herramienta es *capturar* y *organizar* lo elicitado. Visure y Jama permiten importar desde Word, Excel y ReqIF y tienen flujos de revisión con stakeholders; ReqView también importa, pero no tiene portal ni revisión colaborativa, así que queda en Baja.

**Análisis.** Visure tiene análisis de impacto y un complemento de análisis de calidad que detecta requisitos ambiguos o incompletos. Jama tiene trazabilidad en vivo y detección de riesgos. ReqView calcula columnas, detecta enlaces sospechosos y permite comparar versiones, pero no analiza la calidad del texto.

**Especificación.** Las tres son fuertes. Visure y Jama trabajan con ítems tipificados y campos personalizados; ReqView trabaja con documentos con formato de procesador de texto, lo que para un proyecto académico es más natural. En Jama hay una queja recurrente en reseñas: para analizar en serio conviene exportar a hoja de cálculo porque las vistas de trazabilidad se quedan cortas en formato.

**Modelado.** Solo Visure tiene MBSE nativo y se conecta con Cameo y Simulink. Jama lo resuelve por integración. ReqView no modela: solo documentos.

**Gestión de cambios.** Las tres tienen historial, comparación y líneas base. Visure y Jama agregan flujos de aprobación y firma electrónica; ReqView usa Git o Subversion para las líneas base, lo que es más simple pero exige saber Git.

**Verificación y validación.** Visure y Jama gestionan el ciclo completo de pruebas, incluida la ejecución y el registro de defectos. ReqView enlaza requisitos con casos de prueba y muestra la matriz, pero no ejecuta pruebas ni registra resultados.

**Trazabilidad.** Es el punto fuerte de las tres. Jama la hace en vivo y en ambos sentidos; Visure la lleva hasta normas y riesgos; ReqView la resuelve con matriz y enlaces tipificados. En ReqView esto se comprobó en la práctica (sección 7).

**Colaboración.** Aquí está la diferencia más grande. Visure y Jama son multiusuario por diseño, con roles, comentarios y revisión en línea. ReqView es un archivo: para trabajar en equipo hay que compartir carpeta, usar Git o mandarse el archivo. No tiene portal web para stakeholders.

**Integraciones.** Visure tiene el catálogo más amplio (DOORS, Jira, Azure DevOps, Simulink, Cameo, VectorCAST). Jama ofrece API y las integraciones habituales. ReqView se limita a Jira Cloud, Azure DevOps, Sparx EA y ReqIF, y solo en el plan TEAM.

**Reportes y exportación.** Las tres exportan. ReqView exporta a Word, Excel, PDF, HTML, CSV y ReqIF con plantillas configurables; Visure tiene un complemento de informes; Jama tiene paneles e informes nativos.

---

## 5. Costos

### 5.1 Precios publicados (noviembre de 2026)

| Herramienta | Precio | Nivel de confianza |
|---|---|---|
| **ReqView FREE** | Gratis, sin límite de tiempo | Alto (sitio oficial) |
| **ReqView PRO** | €440 / año por usuario | Alto (sitio oficial) |
| **ReqView TEAM** | €600 / año por usuario | Alto (sitio oficial) |
| **ReqView ENTERPRISE** | €1.800 / año por cliente flotante; mínimo 3 clientes = €5.400 / año | Alto (sitio oficial) |
| **ReqView EDUCATIONAL** | Gratis para universidades públicas, previa solicitud | Alto (sitio oficial) |
| **Visure** | Sin precio público. Licencia perpetua o suscripción anual; mantenimiento opcional al 20 % del valor de la licencia perpetua por año | Alto (sitio oficial) |
| **Jama Connect** | Sin precio público. Cuatro tipos de licencia; alojamiento y licencias de revisor incluidas | Alto (sitio oficial) |

Ninguno de los tres publica un precio de lista completo salvo ReqView. Visure y Jama obligan a pedir cotización, y la cotización depende del número de usuarios, del tipo de licencia y del despliegue.

### 5.2 Qué incluye el plan gratuito de ReqView

Es importante porque fue el que se usó en la prueba:

| Límite | Valor |
|---|---|
| Documentos por proyecto | 1 |
| Objetos por documento | 150 |
| Atributos personalizados | 1 |
| Exportación (Word, Excel, PDF, HTML, CSV, ReqIF) | Bloqueada |
| Edición | Solo si el proyecto respeta los tres límites anteriores |
| Lectura, filtros, búsqueda, trazabilidad, impresión | Disponible sin límite |

La propia documentación lo confirma: con el plan FREE se puede "abrir cualquier proyecto en modo de solo lectura, navegar los documentos, filtrar y ordenar, o imprimir la vista de tabla, pero no se puede editar".

### 5.3 Escenario: equipo de 5 personas, un año

Estimación para dimensionar, no cotización real.

| Herramienta | Cálculo | Costo anual estimado |
|---|---|---|
| ReqView PRO | €440 × 5 | **€2.200** |
| ReqView TEAM | €600 × 5 | **€3.000** |
| ReqView ENTERPRISE | €1.800 × 3 (mínimo) | **€5.400** |
| Visure | ~US$3.000 por licencia perpetua × 5 + 20 % de mantenimiento | **~US$15.000** de entrada + ~US$3.000 / año |
| Jama Connect | Cotización; referencias de terceros ubican compras reales en decenas de miles de dólares al año | **Decenas de miles de US$ / año** |

Las cifras de Visure y Jama son **estimaciones de terceros** (Capterra, G2), no precios oficiales. Se incluyen solo para mostrar el orden de magnitud: la diferencia entre ReqView y las otras dos es de **un orden de magnitud, no de un porcentaje**.

### 5.4 Lectura de los costos

- ReqView es entre **5 y 10 veces más barato** que las alternativas empresariales.
- Visure cambia el modelo: se puede comprar y quedar con la licencia, lo que a cinco años puede salir más barato que una suscripción, pero exige una inversión inicial grande.
- Jama no cobra por revisores ni por alojamiento, lo que abarata la participación de stakeholders, pero el costo por creador es alto.
- Para un proyecto académico, ReqView tiene una ventaja decisiva: **licencia educativa gratuita** para universidades públicas.

---

## 6. Facilidad de uso

| Criterio | Visure | Jama Connect | ReqView |
|---|---|---|---|
| Instalación | Servidor o nube; requiere administrador | SaaS: solo navegador | Instalador de Windows, sin servidor |
| Tiempo de puesta en marcha | Días o semanas | Días | Minutos |
| Dependencia de infraestructura | Alta | Media | Ninguna |
| Idioma de la interfaz | Inglés | Inglés | Inglés |
| Curva de aprendizaje | Media | Media | Alta |
| Curso de capacitación | Recomendado | Recomendado | Autoservicio |
| Documentación | Extensa | Extensa | Buena, con tutoriales |
| Requisito técnico | Servidor, base de datos, SSO | Navegador | Windows 11 o superior |

Datos de apoyo:

- **Jama:** G2 reporta un tiempo medio de implementación de **4 meses** y un retorno de inversión de 15 meses. Es un dato de usuarios, no del fabricante.
- **ReqView:** la instalación completa se midió en esta práctica. El instalador pesa **180 MB**, no pide servidor ni base de datos, y la aplicación quedó lista en menos de cinco minutos.
- **Visure:** la propia página de precios habla de "implementation & deployment" como un servicio aparte, lo que da una idea de que no es una herramienta que se instale y ya.

En reseñas de usuarios, Jama tiene 4,03 sobre 5 en facilidad de uso y 3,86 en soporte. ReqView no tiene volumen suficiente de reseñas para una comparación estadística; la evaluación de esta sección se basa en el uso directo.

---

## 7. Herramienta elegida y evaluación práctica

### 7.1 Por qué ReqView

Se eligió ReqView por cuatro razones concretas:

1. **Se puede instalar y probar sin negociar con un vendedor.** Visure y Jama exigen cotización o demo guiada para ver el producto completo.
2. **No necesita infraestructura.** Un instalador y listo; no hay servidor que montar ni base de datos que administrar.
3. **Tiene plan gratuito real.** No es una prueba de 14 días: es un plan sin vencimiento, con límites.
4. **Es la más barata con diferencia**, y tiene licencia educativa gratuita.

La contrapartida, que se dice en la demo: el plan gratuito no sirve para trabajar en serio, solo para leer.

### 7.2 Instalación realizada

| Dato | Valor |
|---|---|
| Versión | 2.22.5 |
| Fabricante | Eccam s.r.o. |
| Instalador | `ReqViewSetup.exe`, 180 MB, firma digital válida |
| Ruta | `%LOCALAPPDATA%\ReqView\app-2.22.5\ReqView.exe` |
| Requisito | Windows 11 |
| Licencia | Plan FREE, sin archivo de licencia y sin cuenta |
| Tiempo de instalación | Menos de 5 minutos |

No se solicitó la prueba de 14 días ni la licencia educativa. Se trabajó deliberadamente con el plan FREE para que la demostración muestre el producto tal como lo recibiría alguien sin presupuesto.

### 7.3 Proyecto de prueba construido

Para que la demo no fuera un proyecto vacío, se construyó un proyecto de ReqView con los datos reales del portafolio de Alexander Drada, extraídos de `docs/Requisitos_Portafolio_Construccion.pdf` y `docs/Planning_Poker_ADB.pdf`:

| Elemento | Cantidad |
|---|---|
| Documentos | 2 (Requisitos y Pruebas) |
| Historias de usuario | 38 |
| Épicas | 5 |
| Puntos de Planning Poker | 214 |
| Prioridad Must / Should / Could | 17 / 16 / 5 |
| Criterios de aceptación | 38 |
| Casos de prueba enlazados | 4 |
| Objetos totales | 45 |

Atributos personalizados creados: tipo, épica, prioridad MoSCoW, sprint, puntos y criterio de aceptación.

El proyecto pasó la validación oficial de la herramienta:

```
> ReqView.exe validate -p "Portafolio_ADB.reqw"
Running command 'Validate' ...
Finished - OK
(código de salida 0)
```

### 7.4 Qué se pudo comprobar y qué no

| Función | Resultado en plan FREE | Evidencia |
|---|---|---|
| Abrir un proyecto de 2 documentos y 45 objetos | Sí | El proyecto abre sin errores |
| Navegar la estructura por épicas | Sí | Árbol de documentos |
| Ver atributos personalizados | Sí | 6 atributos visibles |
| Filtrar por sprint y por prioridad | Sí | Sprint 1 deja 8 historias; Must deja 17 |
| Ver la matriz de trazabilidad | Sí | 4 enlaces requisito-prueba |
| Imprimir | Sí | Documentación oficial |
| Editar el proyecto completo | **No** | FREE permite 1 documento, 150 objetos y 1 atributo |
| Exportar a Excel | **No** | Ver mensaje abajo |
| Exportar a Word, PDF, HTML, CSV o ReqIF | **No** | Misma restricción de plan |
| Gestionar pruebas y ejecutarlas | No | ReqView no ejecuta pruebas en ningún plan |

El bloqueo de exportación se comprobó con la línea de comandos y devolvió el mensaje exacto:

```
> ReqView.exe export xlsx -p "Portafolio_ADB.reqw" -o salida.xlsx
Command 'Export XLSX' is not available in FREE plan.
(código de salida 1)
```

Esto es una limitación del **plan**, no un error de instalación ni de configuración. Es un dato importante para la exposición: demuestra que el límite existe y que se probó.

### 7.5 Limitaciones adicionales encontradas

- **Idioma.** Toda la interfaz está en inglés; no hay traducción al español.
- **Edición en FREE.** Al abrir el proyecto completo, la aplicación avisa que el proyecto excede los límites del plan y queda en solo lectura.
- **Sin colaboración.** No hay portal web ni comentarios para stakeholders; el trabajo en equipo se resuelve con Git o carpeta compartida.
- **Sin ejecución de pruebas.** Enlaza requisitos con pruebas, pero no las ejecuta ni guarda resultados.
- **Dependencia de Windows.** No hay versión para macOS ni Linux; la aplicación es Electron para Windows.

Para poder mostrar edición en vivo dentro del plan FREE, se creó un segundo proyecto mínimo (`Demo_Editable.reqw`) con un documento, un atributo y tres objetos, que sí respeta los límites.

---

## 8. Recomendación

**Sí se recomienda ReqView**, con condiciones.

### Cuándo sí

- Equipos de 1 a 9 personas.
- Proyectos académicos o de consultoría con presupuesto limitado.
- Equipos que ya usan Git y quieren versionar los requisitos junto con el código.
- Organizaciones que necesitan especificaciones en formato de documento (Word/PDF) más que una plataforma web.
- Universidades públicas: la licencia educativa es gratuita.

### Cuándo no

- Empresas reguladas que necesiten evidencia de cumplimiento (DO-178C, ISO 26262, IEC 62304, ISO 13485).
- Equipos que necesiten revisión formal con firma electrónica y auditoría.
- Organizaciones con stakeholders externos que deban entrar por navegador sin instalar nada.
- Proyectos que requieran modelado SysML o MBSE.
- Equipos que necesiten ejecutar y registrar pruebas dentro de la misma herramienta.

### Veredicto en una frase

> Para el proyecto de Alexander Drada, ReqView es la opción correcta: cubre especificación, gestión y trazabilidad, cuesta una fracción de las alternativas y se instala en minutos. Para una empresa grande con auditoría, no alcanza.

---

## 9. Ventajas y desventajas

### 9.1 ReqView (la evaluada)

**Ventajas**

- Instalación local en minutos, sin servidor ni base de datos.
- Precio bajo: PRO €440/año por usuario, TEAM €600/año, licencia educativa gratuita.
- El proyecto es un archivo de texto JSON: se versiona con Git, se compara y se respalda como cualquier archivo.
- Plantillas de documentos basadas en ISO/IEC/IEEE 29148, Volere, historias de usuario, FMEA y OWASP ASVS.
- Trazabilidad, líneas base, historial, comparación de proyectos y enlaces sospechosos.
- Exportación a Word, Excel, PDF, HTML, CSV y ReqIF con plantillas configurables.
- Curva de aprendizaje corta: en una sesión se entiende el modelo de trabajo.

**Desventajas**

- El plan gratuito es de solo lectura y bloquea la exportación.
- No tiene colaboración web ni portal para stakeholders.
- No ejecuta pruebas ni gestiona su ciclo de vida.
- No modela (nada de UML, SysML ni MBSE).
- Interfaz solo en inglés y solo para Windows.
- Las integraciones (Jira, Azure DevOps, Sparx EA) requieren el plan TEAM.

### 9.2 Visure

**Ventajas**

- Cobertura completa: requisitos, riesgos, pruebas, MBSE y trazabilidad en una sola plataforma.
- Paquetes de cumplimiento para normas de industrias reguladas.
- Despliegue flexible: nube, on-premise o air-gapped.
- Modelo de licencia perpetua disponible, además de suscripción.
- Catálogo amplio de integraciones.

**Desventajas**

- Sin precio público: obliga a cotizar.
- Costo alto: inversión inicial de varios miles de dólares por licencia.
- Implementación lenta y con servicio de despliegue aparte.
- Sobredimensionada para proyectos pequeños.
- En el paper no respondió varias secciones del cuestionario, lo que dificulta compararla con datos de 2011.

### 9.3 Jama Connect

**Ventajas**

- Trazabilidad en vivo en ambos sentidos, su función más fuerte.
- Review Center con firma electrónica y auditoría.
- Cuatro tipos de licencia según el rol, con revisores y alojamiento incluidos.
- Gestión de pruebas con ejecución y registro de defectos.
- Colaboración en tiempo real pensada para equipos distribuidos.
- API para integraciones.

**Desventajas**

- Sin precio público; costo de nivel empresarial.
- Tiempo de implementación reportado de 4 meses.
- En reseñas, usuarios reportan que para análisis conviene exportar a hoja de cálculo.
- Sobredimensionada para un equipo de cuatro personas.
- Depende de la nube y de la conexión.

---

## 10. Guion de la demostración (6 minutos)

Los dos proyectos están en `exposicion/proyectos/`:

- `Portafolio_ADB.reqw` — proyecto completo con las 38 historias. En FREE se abre en modo lectura.
- `Demo_Editable.reqw` — proyecto mínimo que sí permite crear y editar en FREE.

### Antes de empezar

1. Abrir `Portafolio_ADB.reqw`.
2. Cerrar cualquier ventana de licencia; el plan FREE no pide nada.
3. Tener a mano el PDF de requisitos por si preguntan de dónde salen las historias.

### Paso 1 — Presentar la herramienta (30 s)

> "ReqView es una herramienta de gestión de requisitos de escritorio. Se instala como cualquier programa de Windows, no necesita servidor ni base de datos, y guarda el proyecto en un archivo JSON que se puede versionar con Git. Es la más liviana de las tres que comparamos."

### Paso 2 — Mostrar la estructura (1 min)

Abrir el documento **Requisitos - Portafolio ADB**.

> "Las 38 historias están agrupadas en las 5 épicas del proyecto. Cada historia conserva el texto original, su criterio de aceptación y los datos de planificación: épica, prioridad MoSCoW, sprint y puntos del Planning Poker."

Señalar **HU-04** y mostrar texto y criterio en el panel de detalle.

### Paso 3 — Mostrar la tabla y los filtros (1 min)

Cambiar a la vista de tabla.

> "Aquí se ve el proyecto como una hoja de cálculo, pero con validación. Los 214 puntos suman exactamente lo que dice el Planning Poker, y puedo filtrar por sprint o por prioridad."

Filtrar **Sprint 1** (quedan 8 historias) y **Must** (quedan 17).

### Paso 4 — Mostrar trazabilidad (1 min)

Abrir el documento **Pruebas - Portafolio ADB**.

> "Cada prueba está enlazada con la historia que verifica. Esto es lo que el paper llama trazabilidad: si cambia un requisito, la herramienta muestra qué pruebas se ven afectadas."

Abrir la matriz de trazabilidad o el enlace de una prueba hacia su historia.

### Paso 5 — Mostrar una limitación real (30 s)

Intentar exportar a Excel desde el menú.

> "En el plan gratuito la exportación está bloqueada. Lo comprobamos: la herramienta responde 'Command Export XLSX is not available in FREE plan'. Es una limitación del plan, no un error de instalación."

### Paso 6 — Crear un requisito en vivo (1,5 min)

Abrir `Demo_Editable.reqw`.

> "Este proyecto pequeño sí se puede editar en FREE porque tiene un solo documento, un solo atributo y menos de 150 objetos."

1. Clic derecho sobre la sección e insertar un requisito.
2. Escribir: `HU-39 Aviso de privacidad en el pie de página`.
3. Texto: `Como visitante quiero ver el aviso de privacidad en el pie para saber cómo se usan mis datos.`
4. Tipo: `Historia de usuario`.
5. Guardar con Ctrl+S.

> "Eso es crear, clasificar y guardar un requisito. En la versión de pago se agregan atributos ilimitados, exportación a Word, Excel y PDF, líneas base e historial de cambios."

### Paso 7 — Cierre y recomendación (1 min)

> "¿La recomendamos? Sí, para equipos pequeños y proyectos como este: cuesta €440 al año por usuario en PRO, se instala en minutos y cubre elicitación, especificación, gestión y trazabilidad. No la recomendamos para una empresa grande con auditoría: ahí se queda corta frente a Jama o Visure. Y el plan gratuito no sirve para trabajar, solo para leer."

### Si preguntan por qué no se usó el plan de pago

> "Porque la tarea era evaluar la herramienta, no comprarla. Con el plan gratuito pudimos abrir un proyecto real, recorrer las 38 historias y comprobar la trazabilidad. La edición y la exportación las verificamos en el proyecto pequeño y en la documentación oficial de precios."

---

## 11. Cómo reproducir la demo

Requiere Windows 11.

```powershell
# 1. Descargar el instalador desde https://www.reqview.com/download/
# 2. Instalar con doble clic. Queda en:
#    %LOCALAPPDATA%\ReqView\app-2.22.5\ReqView.exe

# 3. Abrir el proyecto
& "$env:LOCALAPPDATA\ReqView\app-2.22.5\ReqView.exe" open -p ".\exposicion\proyectos\Portafolio_ADB.reqw"

# 4. Validar el proyecto desde la línea de comandos
#    (la aplicación debe estar cerrada, si no, solo enfoca la ventana)
& "$env:LOCALAPPDATA\ReqView\app-2.22.5\ReqView.exe" validate -p ".\exposicion\proyectos\Portafolio_ADB.reqw"
```

Resultado esperado de la validación: `Finished - OK`.

---

## 12. Fuentes

Consultadas en noviembre de 2026.

| Fuente | Uso |
|---|---|
| Carrillo de Gea, J. M.; Nicolás, J.; Fernández Alemán, J. L.; Toval, A.; Ebert, C.; Vizcaíno, A. *Requirements Engineering Tools*. IEEE Software, julio/agosto 2011, pp. 86-91 | Marco de comparación, Tabla 3, categorías ISO/IEC TR 24766 |
| https://www.reqview.com/pricing/ | Precios, planes y límites de ReqView |
| https://www.reqview.com/doc/install-desktop-app/ | Requisitos de instalación |
| https://www.reqview.com/doc/command-line-interface/ | Comandos `validate`, `export`, `open` |
| https://visuresolutions.com/pricing/ | Modelo de licencias y prueba de Visure |
| https://www.jamasoftware.com/platform/pricing/ | Tipos de licencia de Jama |
| https://www.jamasoftware.com/platform/jama-connect/trial/ | Prueba de 30 días |
| Capterra y G2 | Estimaciones de precio y facilidad de uso |
| `docs/Requisitos_Portafolio_Construccion.pdf` | 38 historias, prioridades y sprints |
| `docs/Planning_Poker_ADB.pdf` | 114 actividades y 214 puntos |

---

## 13. Estado y pendientes

**Listo**

- Tres herramientas elegidas y justificadas.
- Comparación en diez actividades de RE.
- Costos verificados y escenario para cinco usuarios.
- Facilidad de uso comparada.
- ReqView instalado y probado con datos reales.
- Recomendación y conclusiones.
- Guion de demo y proyectos listos para ejecutar.

**Pendiente**

- Diapositivas para la exposición.
- Reparto de quién presenta cada bloque.
