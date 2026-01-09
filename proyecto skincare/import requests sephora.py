import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. URL de la categoría de tratamiento/sérums de Sephora
url = "https://www.sephora.es/shop/tratamiento-rostro-c1214/"

# 2. El "Disfraz" (User-Agent) para que Sephora nos deje entrar
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

print(f"--- 🧴 CONECTANDO CON SEPHORA: {url} ---")

try:
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos_finales = []

        # 3. Buscamos las tarjetas de producto
        # Nota: Las clases de Sephora cambian a veces, usamos selectores comunes
        productos = soup.find_all('div', class_='product-tile') 

        for p in productos:
            try:
                # Extraemos nombre y marca
                marca = p.find('span', class_='product-brand').text.strip()
                nombre = p.find('span', class_='product-name').text.strip()
                precio = p.find('span', class_='value').get_text().strip()
                
                print(f"✅ Capturado: {marca} - {nombre} ({precio})")
                
                productos_finales.append({
                    'Marca': marca,
                    'Producto': nombre,
                    'Precio': precio,
                    'Fuente': 'Sephora Real'
                })
            except:
                continue # Si un producto falla, saltamos al siguiente

        # 4. Guardamos los datos reales
        if productos_finales:
            df_sephora = pd.DataFrame(productos_finales)
            df_sephora.to_excel("datos_sephora_reales.xlsx", index=False)
            print(f"\n✨ ¡Misión cumplida! Se han guardado {len(df_sephora)} productos de Sephora.")
        else:
            print("⚠️ Conectamos, pero Sephora no nos mostró los productos. Puede que necesitemos un disfraz más fuerte.")
            
    else:
        print(f"❌ Error de acceso: {response.status_code}. Sephora ha detectado el bot.")

except Exception as e:
    print(f"❌ Error técnico: {e}")