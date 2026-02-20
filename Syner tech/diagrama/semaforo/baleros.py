import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_baleros_final():
    dot = Digraph('Cambio_Baleros_Final', filename='proc_10_baleros_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE BALEROS DE RUEDA (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_BAL', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_BAL', 'Recepción: Reporte de\nZumbido o Vibración')
        c.node('A2_BAL', 'Cierre de Orden y\nValidación de Silencio')
        c.node('END_BAL', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_BAL', 'Prueba de Giro:\n¿Es el Balero?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_BAL', 'Diagnóstico de Llantas\no Diferencial')
        c.node('J3_BAL', 'Validación de Giro Libre\ny Ausencia de Ruido')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_BAL', 'Desmontaje de Maza,\nCalipers y Sensores')
        c.node('M2_BAL', 'Extracción de Balero\nViejo con Prensa')
        c.node('M3_BAL', 'Instalación de Balero\nNuevo y Retenes')
        c.node('M4_BAL', 'Limpieza de Sensor ABS\ny Ensamble Final')
        c.node('M5_BAL', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_BAL', '¿Balero en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_BAL', 'Surtir Balero Sellado\ny Seguro de Maza')
        c.node('S3_BAL', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_BAL', 'A1_BAL')
    dot.edge('A1_BAL', 'J1_BAL')
    
    # Decisión de Diagnóstico
    dot.edge('J1_BAL', 'J2_BAL', label=' NO')
    dot.edge('J1_BAL', 'M1_BAL', label=' SÍ')
    dot.edge('J2_BAL', 'A2_BAL', label=' Corregir')
    
    # Interacción Almacén
    dot.edge('M1_BAL', 'S1_BAL', label=' Solicitar')
    dot.edge('S1_BAL', 'S3_BAL', label=' NO')
    dot.edge('S3_BAL', 'S2_BAL')
    dot.edge('S1_BAL', 'S2_BAL', label=' SÍ')
    dot.edge('S2_BAL', 'M2_BAL')
    
    # Finalización Técnica
    dot.edge('M2_BAL', 'M3_BAL')
    dot.edge('M3_BAL', 'M4_BAL')
    dot.edge('M4_BAL', 'M5_BAL')
    dot.edge('M5_BAL', 'J3_BAL')
    dot.edge('J3_BAL', 'A2_BAL', label=' OK')
    dot.edge('A2_BAL', 'END_BAL')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Baleros' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_baleros_final()