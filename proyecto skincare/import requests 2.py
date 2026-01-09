import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. URL de una categoría de ejemplo (puedes cambiarla por otra de una web similar)
url = "https://tiddlywinkscosmetics.com/collections/all" 

# 2. El "disfraz" para que no nos bloqueen
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

print(f"--- 🧴 INVESTIGANDO PRODUCTOS EN: {url} ---")

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lista_productos = []

        # 3. Buscamos los contenedores de productos (esto varía según la web)
        # Normalmente los nombres están en etiquetas h2 o h3
        nombres = soup.find_all(['h2', 'h3'])

        for n in nombres:
            texto = n.get_text().strip()
            if len(texto) > 3: # Filtramos textos muy cortos
                print(f"✨ Producto encontrado: {texto}")
                lista_productos.append({"Activo/Producto": texto})

        # 4. Guardamos los resultados
        if lista_productos:
            df = pd.DataFrame(lista_productos)
            df.to_excel("productos_extraidos_REALES.xlsx", index=False)
            print(f"\n✅ ¡Misión cumplida! {len(df)} productos guardados.")
        else:
            print("⚠️ Conectamos, pero no encontramos nombres. Hay que ajustar las etiquetas.")
            
    else:
        print(f"❌ La web nos ha rechazado (Código {response.status_code})")

except Exception as e:
    print(f"❌ Error inesperado: {e}")