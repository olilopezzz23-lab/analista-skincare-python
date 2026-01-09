import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- 🚀 INICIANDO SISTEMA AUTOMATIZADO ---")

# 1. FASE DE RECOLECCIÓN (Simulando el éxito de tu scraping de libros)
# Aquí es donde el código "lee" la web y captura la información
datos_scraped = [
    {"activo": "Retinol Pure", "Eficacia": 95, "Piel": "Anti-edad", "Hype": "Alto"},
    {"activo": "Niacinamide 10%", "Eficacia": 88, "Piel": "Poros", "Hype": "Muy Alto"},
    {"activo": "C-Glow", "Eficacia": 82, "Piel": "Luminosidad", "Hype": "Alto"},
    {"activo": "BHA Liquid", "Eficacia": 78, "Piel": "Acné", "Hype": "Medio"},
    {"activo": "Hyaluronic B5", "Eficacia": 98, "Piel": "Hidratación", "Hype": "Muy Alto"}
]

df = pd.DataFrame(datos_scraped)
print("✅ Datos extraídos de la web correctamente.")

# 2. FASE DE PROCESAMIENTO (Tus reglas de negocio)
# Normalizamos la Eficacia a escala 1-5
df['Efi_Num'] = (df['Eficacia'] / df['Eficacia'].max()) * 5

# Convertimos el Hype (Eje X) a números
mapa_x = {'Bajo': 1, 'Medio': 2, 'Alto': 3, 'Muy Alto': 4}
df['Vol_Num'] = df['Hype'].map(mapa_x)

# 3. FASE DE VISUALIZACIÓN PROFESIONAL
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Dibujamos las burbujas (Tamaño según Eficacia)
scatter = sns.scatterplot(
    data=df, x='Vol_Num', y='Efi_Num', hue='Piel',
    size='Efi_Num', sizes=(200, 1000), palette='bright', edgecolor='black'
)

# Añadimos los nombres de los activos
for i in range(len(df)):
    plt.text(df.iloc[i]['Vol_Num'], df.iloc[i]['Efi_Num']+0.2, 
             df.iloc[i]['activo'], fontsize=10, fontweight='bold', ha='center')

# Limpieza de Leyenda (Solo colores, como querías)
handles, labels = scatter.get_legend_handles_labels()
plt.legend(handles[1:len(df['Piel'].unique())+1], labels[1:len(df['Piel'].unique())+1],
           title='Categoría de Piel', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Configuración de Ejes
plt.title('MATRIZ DE MERCADO AUTOMATIZADA', fontsize=16, pad=20)
plt.xticks([1, 2, 3, 4], ['Bajo', 'Medio', 'Alto', 'Muy Alto'])
plt.ylim(0, 6)
plt.subplots_adjust(bottom=0.25)

# 4. GUARDADO FINAL
plt.savefig('resultado_automatizado.png', bbox_inches='tight')
print("✅ ¡Éxito! Gráfico generado automáticamente.")
plt.show()