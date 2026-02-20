import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_bateria_final():
    dot = Digraph('Cambio_Bateria_Final', filename='proc_03_bateria_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE BATERÍA (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos (Estructurado)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_BAT', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_BAT', 'Recepción: Reporte de\nFalla de Arranque')
        c.node('A2_BAT', 'Cierre de Orden\ny Entrega de Unidad')
        c.node('END_BAT', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_BAT', 'Prueba de Carga\n(Alternador/Parásitos)')
        c.node('J2_BAT', '¿Alternador en\nBuen Estado?', shape='diamond', fillcolor='#fff9c4')
        c.node('J3_BAT', 'Notificar Falla de\nSistema de Carga')
        c.node('J4_BAT', 'Validación de Voltajes\nFinales (Post-Instalación)')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_BAT', 'Test de CCA y\nVoltaje de Batería')
        c.node('M2_BAT', 'Desmontaje con\nRespaldo de Memoria')
        c.node('M3_BAT', 'Instalación y\nLimpieza de Bornes')
        c.node('M4_BAT', 'Carga de Evidencia\n(Notion: Scan/Voltaje)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_BAT', '¿Modelo en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_BAT', 'Surtir Batería Nueva\ny Protector de Bornes')
        c.node('S3_BAT', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_BAT', 'A1_BAT')
    dot.edge('A1_BAT', 'J1_BAT')
    dot.edge('J1_BAT', 'J2_BAT')
    
    # Decisión de Alternador
    dot.edge('J2_BAT', 'J3_BAT', label=' NO')
    dot.edge('J2_BAT', 'M1_BAT', label=' SÍ')
    dot.edge('J3_BAT', 'A2_BAT', label=' Reportar')
    
    # Decisión de Stock
    dot.edge('M1_BAT', 'S1_BAT', label=' Solicitar')
    dot.edge('S1_BAT', 'S3_BAT', label=' NO')
    dot.edge('S3_BAT', 'S2_BAT')
    dot.edge('S1_BAT', 'S2_BAT', label=' SÍ')
    dot.edge('S2_BAT', 'M2_BAT')
    
    dot.edge('M2_BAT', 'M3_BAT')
    dot.edge('M3_BAT', 'M4_BAT')
    dot.edge('M4_BAT', 'J4_BAT')
    dot.edge('J4_BAT', 'A2_BAT', label=' OK')
    dot.edge('A2_BAT', 'END_BAT')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Batería' con decisiones generado.")

if __name__ == "__main__":
    generar_proceso_bateria_final()