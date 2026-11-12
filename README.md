# Análisis de temperaturas desde CSV

Procesa tus mediciones localmente y genera gráficas de temperatura frente a su
derivada, con un ajuste lineal para cada serie. El proyecto se distribuye sin
datos ni gráficas precalculadas: tú añades tus archivos en tu ordenador.

## Instalación

Necesitas Python 3.10 o posterior. Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Uso

1. Copia tus tres CSV (o cualquier cantidad) dentro de `data/`.
2. Ejecuta desde la carpeta del proyecto:

   ```powershell
   .\.venv\Scripts\python.exe read_data.py
   ```

El programa busca todos los CSV de `data/`, muestra las filas procesadas y la
pendiente y el intercepto de cada serie. Guarda un PNG junto a cada CSV con el
mismo nombre: `data/medidas.csv` produce `data/medidas.png`. Si ese PNG ya existe,
lo sobrescribe. Cada ejecución vuelve a leer los archivos disponibles; no vigila
la carpeta en segundo plano ni busca en subcarpetas.

También puedes procesar otra carpeta local:

```powershell
.\.venv\Scripts\python.exe read_data.py "C:\ruta\a\mis\mediciones"
```

Si no hay CSV, muestra un aviso. Si un archivo falla con alguno de los errores
controlados, informa del problema y continúa con los demás.

## Formato de los datos

La primera fila contiene los nombres de las columnas. La primera columna es el
tiempo en segundos; cada columna restante es una serie de temperaturas en grados
Celsius. Los nombres de las columnas son libres. Se admiten archivos UTF-8 con
o sin BOM y una fila opcional de unidades con `s` en la primera columna.

Usa tiempos numéricos con un intervalo constante y distinto de cero, comas como
separador y punto decimal. Una celda de temperatura vacía termina esa serie:
los valores posteriores de esa columna no se procesan. Cada serie necesita al
menos seis muestras y derivadas que no sean todas iguales para obtener un ajuste
lineal válido. Evita tiempos vacíos y valores no finitos.

La derivada se calcula mediante una diferencia central de cinco puntos. Los dos
primeros y los dos últimos puntos quedan fuera del ajuste. La recta ajustada es
`temperatura = pendiente * derivada + intercepto`.

## Archivos locales y Git

`data/` está reservada para archivos locales; Git solo incluye su marcador vacío
`.gitkeep`. Además, `.gitignore` excluye los CSV y PNG con extensiones `.csv`,
`.CSV`, `.png` y `.PNG` en todo el proyecto. No fuerces su inclusión con
`git add -f`. El programa no sube los datos a ningún servicio.

Estas reglas no eliminan archivos que ya estuvieran en commits anteriores.
