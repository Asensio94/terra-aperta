# Terra Aperta

La página de entrada a los proyectos hermanos de datos abiertos sobre naturaleza en España y Francia: qué
pregunta responde cada uno, cómo lo hace, su cifra del día y dónde está su web. No mide nada por sí misma:
cada día lee lo que ya publica cada proyecto. Web: <https://asensio94.github.io/naturaleza/> · en francés:
<https://asensio94.github.io/naturaleza/fr/>

*Terra aperta* es latín: «tierra abierta», el territorio con sus datos a la vista.

> **Estado: activo.** Se actualiza solo y sigue en desarrollo.

## Cómo funciona

1. **Registro.** `terra/projects.py` describe cada proyecto en español y en francés: nombre, pregunta que
   responde, cómo lo hace, qué cifra enseña y qué páginas tiene su web (`PAGES`). `MENU` fija la barra
   superior y su orden: Sub Nocte, Incendios, Centinela, IBA, Tendidos, Alegaciones (observatorio y grafo) y
   Agua (humedales, caudal, acuíferos, depuración y zona inundable). Una entrada con más de una página abre un
   desplegable; si una página está en otro idioma, lo marca (ES / FR). Todo lo que se lee está escrito ahí; el
   robot solo añade lo que cambia por sí mismo.
2. **Lectura diaria.** `terra/collect.py` pide, para cada proyecto, tres cosas públicas:
   - la línea de estado de su README (`Estado: activo / mantenimiento / aparcado`);
   - si tiene página en francés (`fr/`, `index.fr.html` o `france.html` que responda con `lang="fr"`);
   - su `signals.json` (contrato en [estado-iba/CONTRATO.md](https://github.com/Asensio94/estado-iba/blob/main/CONTRATO.md)),
     del que salen la cifra y la fecha. Si el proyecto no publica señales, la fecha es la del último cambio
     en su repositorio (API de GitHub).
3. **Cifras.** Cada cifra es una regla fija sobre las señales, escrita en `terra/projects.py`: por ejemplo,
   cuántos incendios de la vigía tocan un espacio Natura 2000 (`sites` no vacío), o cuántos puntos de aforo
   están por debajo del caudal mínimo (`details.below_now`). Las de los proyectos con datos de los dos países
   se dan por país. Nunca se suman entre proyectos.
4. **Antigüedad.** Si un proyecto lleva más días de los normales sin actualizarse (3 para los diarios, 40 para
   los mensuales, 400 para los anuales), la ficha lo dice.
5. **Páginas.** `terra/web.py` escribe la portada, corta: la barra, Sub Nocte en grande y una ficha por
   proyecto con su pregunta, su cifra y su fecha (`docs/index.html`, `docs/fr/index.html`). Todo lo que la
   explica —cómo leerla, qué hace cada proyecto, qué no es, cómo se hace y el glosario— va en la página de
   método (`docs/metodo.html`, `docs/fr/methode.html`). Además, `docs/estado.json` guarda todo lo leído. Si no se puede leer más de la mitad de los proyectos,
   el fallo es de la red y no de ellos: se deja la página que ya estaba.

## Límites

- Las cifras son tan buenas como las de cada proyecto; aquí no se vuelven a comprobar. Cada ficha enlaza a la
  web que explica su método, su validación y sus errores conocidos.
- El estado es el que declara cada README. Un proyecto sin línea de estado se enseña sin etiqueta.
- La actualización es diaria: una cifra puede ir hasta un día por detrás de la web del proyecto.

## Uso

```
python -m terra          # lee todos los proyectos y escribe docs/
python -m unittest       # pruebas, sin red
```

Solo usa la biblioteca estándar de Python (3.11 o posterior). El flujo `.github/workflows/daily.yml` lo lanza
cada día a las 07:40 UTC y publica `docs/` con GitHub Pages.

## Datos que se guardan

| Fichero | Contenido |
|---|---|
| `docs/index.html`, `docs/fr/index.html` | La portada, en español y en francés. |
| `docs/metodo.html`, `docs/fr/methode.html` | Cómo leerla, qué hace cada proyecto, qué no es, método y glosario. |
| `docs/estado.json` | Lo leído de cada proyecto: estado, página francesa, número de señales, cifras, fecha y fallos. |

## Fuentes y licencias

Los datos son de los proyectos hermanos, cada uno con sus fuentes y licencias en su README. Código bajo
licencia MIT; `docs/estado.json`, CC BY 4.0.

Forma parte de un conjunto de proyectos hermanos: [sub-nocte](https://github.com/Asensio94/sub-nocte),
[vigia-incendios](https://github.com/Asensio94/vigia-incendios), [centinela-natura](https://github.com/Asensio94/centinela-natura),
[estado-iba](https://github.com/Asensio94/estado-iba), [riesgo-tendidos-aves](https://github.com/Asensio94/riesgo-tendidos-aves),
[observatorio-alegaciones](https://github.com/Asensio94/observatorio-alegaciones), [grafo-promotores](https://github.com/Asensio94/grafo-promotores),
[vigilancia-humedales](https://github.com/Asensio94/vigilancia-humedales), [caudal-ecologico](https://github.com/Asensio94/caudal-ecologico),
[acuiferos-francia](https://github.com/Asensio94/acuiferos-francia), [depuracion-y-bano](https://github.com/Asensio94/depuracion-y-bano) y
[zona-inundable](https://github.com/Asensio94/zona-inundable).
