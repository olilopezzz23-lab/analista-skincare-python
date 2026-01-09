import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# 1. CARGA Y PROCESAMIENTO DE DATOS
archivos = glob.glob("*.ods")
if not archivos:
    print("❌ No se encontró el archivo .ods")
else:
    df = pd.read_excel(archivos[0], engine='odf')
    
    # Detección automática de columnas
    def encontrar_col(nombres, clave):
        for c in nombres:
            if clave.lower() in c.lower(): return c
        return nombres[0]

    c_activo = encontrar_col(df.columns, 'activo')
    c_piel = encontrar_col(df.columns, 'Preocupación')
    c_vol = encontrar_col(df.columns, 'Volumen')
    c_efi = encontrar_col(df.columns, 'Eficacia')

    # Escalado Min-Max (1 a 5) para que los puntos se distribuyan bien
    df['E_Raw'] = pd.to_numeric(df[c_efi], errors='coerce')
    min_v, max_v = df['E_Raw'].min(), df['E_Raw'].max()
    if max_v != min_v:
        df['E_Num'] = 1 + (df['E_Raw'] - min_v) * (4 / (max_v - min_v))
    else:
        df['E_Num'] = 3

    # Mapeo del eje X
    mapa_v = {'Bajo': 1, 'Medio': 2, 'Alto': 3, 'Muy Alto': 4}
    df['V_Num'] = df[c_vol].astype(str).str.strip().map(mapa_v)
    df = df.dropna(subset=['V_Num', 'E_Num'])

    # 2. CONFIGURACIÓN DEL GRÁFICO
    plt.figure(figsize=(12, 10))
    sns.set_style("whitegrid")

    # Creamos el gráfico (las burbujas crecen, pero limpiaremos la leyenda luego)
    scatter = sns.scatterplot(
        data=df, x='V_Num', y='E_Num', hue=c_piel,
        size='E_Num', sizes=(200, 1000), 
        palette='bright', edgecolor='black', alpha=0.8
    )

    # 3. ETIQUETAS DE TEXTO (Nombres de activos)
    for i in range(len(df)):
        plt.text(
            df.iloc[i]['V_Num'], 
            df.iloc[i]['E_Num'] + 0.2, 
            str(df.iloc[i][c_activo]), 
            fontsize=10, fontweight='bold', ha='center'
        )

    # 4. PERSONALIZACIÓN DE EJES
    plt.title('MATRIZ ESTRATÉGICA DE ACTIVOS SKINCARE', fontsize=16, pad=20)
    plt.xlabel('Volumen de Reviews (Hype)', fontsize=12, fontweight='bold')
    plt.ylabel('Valoración Media (Escala 1-5)', fontsize=12, fontweight='bold')
    plt.xticks([1, 2, 3, 4], ['Bajo', 'Medio', 'Alto', 'Muy Alto'])
    plt.ylim(0, 6)

    # --- 5. LIMPIEZA TOTAL DE LA LEYENDA (SOLO COLORES) ---
    # Obtenemos los elementos de la leyenda
    handles, labels = scatter.get_legend_handles_labels()
    
    # Buscamos dónde terminan los colores y empieza el tamaño (e_num)
    # Filtramos para quedarnos SOLO con los tipos de piel
    num_categorias = df[c_piel].nunique()
    
    # Creamos la nueva leyenda solo con los primeros elementos (los colores)
    plt.legend(
        handles[1:num_categorias+1], 
        labels[1:num_categorias+1],
        title='Tipo de Piel',
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        frameon=True,
        shadow=True
    )

    # Ajuste final para que no se corte nada
    plt.subplots_adjust(bottom=0.25)
    
    plt.savefig('grafico_skincare_perfecto.png', dpi=300, bbox_inches='tight')
    print("✅ ¡Gráfico limpio! Se han eliminado las bolas negras de la leyenda.")
    plt.show()