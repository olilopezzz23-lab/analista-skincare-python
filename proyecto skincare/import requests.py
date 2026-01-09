import pandas as pd

# 1. ESTO SIMULA LO QUE PYTHON VE AL ENTRAR EN UNA WEB
# Es un montón de texto desordenado (HTML)
contenido_web = """
<div class="producto">
    <h2 class="nombre">Retinol 0.5%</h2>
    <span class="precio">25.99€</span>
    <div class="rating">4.8</div>
</div>
<div class="producto">
    <h2 class="nombre">Vitamina C</h2>
    <span class="precio">18.50€</span>
    <div class="rating">4.2</div>
</div>
"""

print("--- 🔍 INICIANDO EXTRACCIÓN SIMULADA ---")

# 2. CREAMOS UNA LISTA PARA GUARDAR LO QUE "CAZAMOS"
datos_extraidos = []

# 3. LÓGICA DE EXTRACCIÓN (Simulando BeautifulSoup)
# Imagina que Python recorre la web buscando etiquetas específicas
import re # Usamos esto para buscar texto de forma inteligente

nombres = re.findall(r'<h2 class="nombre">(.*?)</h2>', contenido_web)
precios = re.findall(r'<span class="precio">(.*?)</span>', contenido_web)
ratings = re.findall(r'<div class="rating">(.*?)</div>', contenido_web)

# 4. ORGANIZAMOS LA INFORMACIÓN
for i in range(len(nombres)):
    item = {
        'Activo': nombres[i],
        'Precio': precios[i],
        'Puntuación': ratings[i]
    }
    datos_extraidos.append(item)
    print(f"✅ Encontrado: {nombres[i]} a {precios[i]}")

# 5. ¡LO CONVERTIMOS EN UNA TABLA!
df_nuevo = pd.DataFrame(datos_extraidos)

print("\n--- 📊 RESULTADO FINAL EN TABLA ---")
print(df_nuevo)

# Guardar en un nuevo Excel para tu portafolio
# df_nuevo.to_excel("datos_extraidos_web.xlsx", index=False)