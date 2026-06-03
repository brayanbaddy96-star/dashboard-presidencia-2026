# Dashboard Presidencia 2026 | MMV final

Esta versión fue actualizada con el archivo:

```text
PRE_MMV_MAX_TODOS 2.csv
```

## Resumen de datos

- Total MMV: 23.978.304 votos
- Votos válidos: 23.685.329
- Filas procesadas del MMV: 1.479.506
- Bogotá reorganizada por localidades DIVIPOL: sí

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app_dashboard_presidencia_2026.py
```

## Publicación en Streamlit Community Cloud

Archivo principal:

```text
app_dashboard_presidencia_2026.py
```

La carpeta `data/` ya contiene todos los CSV procesados.


## Nota V9

Se reactivó la barra superior nativa de Streamlit para que el usuario pueda volver a abrir el panel lateral si lo cierra.


## Actualización V10

- Se agregó el módulo **Proyección votación 2ª vuelta** antes del simulador.
- Se incorporó el voto en blanco como destino explícito en la transferencia de votos.
- Se actualizó el modelo de transferencias para distinguir: Abelardo, Cepeda, voto en blanco y fuga/no conversión.
- Se incorporó el archivo `PROYECCIONES PRESIDENCIA.xlsx` como fuente metodológica para la proyección agregada.


## Nota V11

- Se incorporó gráfico de líneas de serie histórica 2006-2026 en el módulo de proyección.
- El simulador de segunda vuelta queda normalizado contra la proyección macro: Abelardo + Cepeda = votos por candidatos proyectados y voto blanco = voto blanco proyectado.
- El voto en blanco se conserva como destino político explícito de transferencia.


## Nota V12

Se corrigió la pestaña de serie histórica para mostrar todas las elecciones del archivo de proyecciones desde marzo de 2006 hasta junio de 2026, no solo mayo/junio de 2026.


## Nota V15

Se corrigió la visualización del mapa de fuerzas y se reordenaron las pestañas para mostrar primero el ranking del territorio.


## Nota V16

Se reemplazó el mapa de geometrías externas por un mapa estable de centroides territoriales construido con coordenadas de puestos de votación. Se conserva color morado para Cepeda y naranja para Abelardo.


## Nota V17

Se incorporó mapa poligonal para departamentos y municipios usando GeoJSON. Si la geometría remota no carga, el tablero conserva un respaldo por centroides.


## Nota V18

Se corrigió el error `NameError: name 're' is not defined` en el módulo de mapa poligonal.


## Nota V19

Se corrigió el color del mapa poligonal, se mejoró el cruce por códigos DANE/nombres normalizados y se intentó habilitar croquis de Bogotá por localidades cuando la geometría externa esté disponible.


## Nota V20

Se agregó fuente GeoJSON de localidades de Bogotá desde servicio ArcGIS/IDECA-CAR y se ajustó el cruce para localidades sin exigir nombre de departamento en la geometría.
