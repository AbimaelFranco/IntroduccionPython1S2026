import pandas as pd

# Cargar el archivo
archivo = "examples/Bot_Telegram/notas.xlsx"
df = pd.read_excel(archivo)

# Mostrar nombres de columnas
print("Columnas del archivo:")
# print(df.columns.tolist())
for columna in df.columns:
    print(columna)

# Mostrar cantidad de registros
print("\nCantidad de registros:")
print(len(df))