# Elecciones 29N

Guía ciudadana independiente de las elecciones generales del 29 de noviembre de 2026, monetizada con AdSense.

- Guías: mesa electoral, voto por correo, calendario, cómo votar, voto desde el extranjero, ley D'Hondt.
- Herramientas: simulador de escaños D'Hondt, test de afinidad, votación simbólica (Supabase).
- SEO local: 52 páginas de provincia. GEO: `llms.txt`, JSON-LD, cajas de respuesta directa.

## Generar la web

```
python build.py          # genera dist/
python -m http.server 8137 --directory dist
```

Datos en `data/` (resultados 2023 oficiales, escaños 2026 estimados, posiciones del test, mapa IGN), textos en `content/`, estilos y scripts en `src/assets/`. Configuración (dominio, AdSense, titular) al principio de `build.py`.

Investigación de lanzamiento (dominio, hosting, AdSense, aspectos legales): `docs/lanzamiento.md`.

Límites administrativos © Instituto Geográfico Nacional de España (CC BY 4.0), vía es-atlas (MIT).
