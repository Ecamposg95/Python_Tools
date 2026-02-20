import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_suspension_final():
    dot = Digraph('Suspension_General', filename='proc_09_suspension_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: MANTENIMIENTO DE SUSPENSIÓN GENERAL (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_SUS', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_SUS', 'Recepción: Reporte de\nRuidos, Inestabilidad o Golpeteo')
        c.node('A2_SUS', 'Cierre de Orden y\nReporte de Alineación')
        c.node('END_SUS', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_SUS', 'Inspección Visual y Juego:\n¿Hay Fugas o Roturas?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_SUS', 'Diagnóstico de Componentes\n(Amortiguadores/Bases)')
        c.node('J3_SUS', 'Validar Torque y\nPrueba de Ruta Final')

    # --- CARRIL 3: MECÁNICO (ESPECIALISTA) ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_SUS', 'Desmontaje de Amortiguadores\ny Brazos de Control')
        c.node('M2_SUS', 'Sustitución de Bujes,\nRótulas o Terminales')
        c.node('M3_SUS', 'Instalación con Carga\ny Geometría Preliminar')
        c.node('M4_SUS', 'Engrase de Puntos y\nLimpieza de Zonas')
        c.node('M5_SUS', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_SUS', '¿Refacciones Disponibles?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_SUS', 'Surtir Kit Suspensión\n(Gomas, Tornillos, Piezas)')
        c.node('S3_SUS', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_SUS', 'A1_SUS')
    dot.edge('A1_SUS', 'J1_SUS')
    
    # Decisión de Estado de Suspensión
    dot.edge('J1_SUS', 'J2_SUS', label=' SÍ')
    dot.edge('J1_SUS', 'M1_SUS', label=' NO')
    dot.edge('J2_SUS', 'M1_SUS', label=' OK')
    
    # Interacción Almacén
    dot.edge('M1_SUS', 'S1_SUS', label=' Solicitar')
    dot.edge('S1_SUS', 'S3_SUS', label=' NO')
    dot.edge('S3_SUS', 'S2_SUS')
    dot.edge('S1_SUS', 'S2_SUS', label=' SÍ')
    dot.edge('S2_SUS', 'M2_SUS')
    
    # Finalización Técnica
    dot.edge('M2_SUS', 'M3_SUS')
    dot.edge('M3_SUS', 'M4_SUS')
    dot.edge('M4_SUS', 'M5_SUS')
    dot.edge('M5_SUS', 'J3_SUS')
    dot.edge('J3_SUS', 'A2_SUS', label=' OK (Alineado)')
    dot.edge('A2_SUS', 'END_SUS')

    dot.render(cleanup=True)
    print("✅ Proceso 'Suspensión General' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_suspension_final()