
# Dashboard Presidencia 2026 | Sin MySQL

Este paquete contiene un dashboard de inteligencia territorial construido únicamente con archivos CSV preprocesados. No requiere MySQL, ni servidor de base de datos.

## Instalación rápida

1. Descomprime el paquete.
2. Abre la terminal dentro de la carpeta descomprimida.
3. Ejecuta:

```bash
pip install -r requirements.txt
streamlit run app_dashboard_presidencia_2026.py
```

## Módulos

- Comando nacional
- Dominio territorial
- Municipios bisagra
- Bolsa por definir
- Puestos críticos
- Simulador de segunda vuelta
- Fuentes y metodología

## Datos incluidos

La carpeta `data/` contiene agregados nacionales, departamentales, municipales y por puesto. El MMV original no es necesario para ejecutar el dashboard.

## Nota metodológica

La abstención se estima como `potencial DIVIPOL - total de votos MMV`. Esta medida depende de la consistencia entre DIVIPOL y MMV.

Los supuestos de transferencia de segunda vuelta son editables en el dashboard. No deben leerse como predicción cerrada, sino como motor de escenarios.


## Versión explicada

Esta versión mejora los textos del módulo Simulador 2ª vuelta: aclara que las métricas municipales son proyecciones bajo escenarios, no resultados oficiales, y añade un semáforo de competitividad territorial.
