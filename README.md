# dataleak-pipeline-ej

Mini data lake local en Python con un pipeline por capas (**raw → bronze → silver → gold**), usando datos sintéticos de ventas.

## ¿Qué hace?

Simula, de forma simplificada, un data lake real:

1. **Genera** eventos de venta sintéticos (producto, categoría, cantidad, precio, país, fecha), incluyendo a propósito algunas filas "sucias" (cantidades negativas, pedidos duplicados).
2. **Ingesta** esos datos crudos tal cual llegan y los tipa/convierte a Parquet (bronze).
3. **Limpia** el bronze: elimina duplicados y filas inválidas, y calcula campos derivados como el importe total (silver).
4. **Agrega** el silver en tablas de negocio listas para consumir, como ingresos por categoría o por día (gold).

Todo el pipeline se ejecuta localmente sobre el filesystem (sin bases de datos ni servicios externos) y es completamente reproducible: se puede borrar `data_lake/` y regenerarlo desde cero con un solo comando.

## Capas

- **raw**: CSV generados sintéticamente, particionados por día (`data_lake/raw/sales/dt=YYYY-MM-DD/sales.csv`).
- **bronze**: ingesta tipada de todo lo que haya en raw, en Parquet.
- **silver**: datos limpios (sin duplicados, sin filas inválidas) con campos derivados (`total_amount`).
- **gold**: tablas agregadas listas para consumo (`revenue_by_category`, `daily_revenue`).

## Uso

```bash
pip install -r requirements.txt

# generar datos sintéticos y correr el pipeline completo
python main.py all --days 5 --rows-per-day 300

# o paso a paso
python main.py generate --days 5 --rows-per-day 300
python main.py run

# inspeccionar una capa
python main.py show gold
python main.py show silver --rows 20
```

Los datos generados viven en `data_lake/` (ignorado por git) y se pueden regenerar en cualquier momento.
