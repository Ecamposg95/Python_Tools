import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_frenos_final():
    dot = Digraph('Cambio_Frenos_Final', filename='proc_04_frenos_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE FRENOS (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos (Estructurado)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_FR', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_FR', 'Recepción: Reporte de\nRuido o Pedal Bajo')
        c.node('A2_FR', 'Cierre de Orden\ny Entrega de Unidad')
        c.node('END_FR', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_FR', 'Inspección Táctica:\nMedir Vida de Balatas')
        c.node('J2_FR', '¿Disco dentro de\nEspesor Mínimo?', shape='diamond', fillcolor='#fff9c4')
        c.node('J3_FR', 'Validar Frenado y\nNivel de Líquido')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_FR', 'Desmontaje y\nLimpieza de Calipers')
        c.node('M2_FR', 'Rectificado de Discos\n(En Torno)')
        c.node('M3_FR', 'Montaje de Balatas y\nEngrase de Guías')
        c.node('M4_FR', 'Purgado y Cambio\nde Líquido (DOT 4)')
        c.node('M5_FR', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_FR', 'Surtir Kit Balatas y\nLíquido de Frenos')
        c.node('S2_FR', '¿Solicitar Discos\nNuevos?', shape='diamond', fillcolor='#fff9c4')
        c.node('S3_FR', 'Registro de Salida\nen Sistema Digital')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_FR', 'A1_FR')
    dot.edge('A1_FR', 'J1_FR')
    dot.edge('J1_FR', 'M1_FR')
    
    # Decisión de Rectificado vs Cambio
    dot.edge('M1_FR', 'J2_FR')
    dot.edge('J2_FR', 'M2_FR', label=' SÍ')
    dot.edge('J2_FR', 'S2_FR', label=' NO')
    
    # Interacción Almacén
    dot.edge('S2_FR', 'S1_FR', label=' Surtir Todo')
    dot.edge('S1_FR', 'S3_FR')
    dot.edge('S3_FR', 'M3_FR')
    
    # Continuación Técnica
    dot.edge('M2_FR', 'M3_FR')
    dot.edge('M3_FR', 'M4_FR')
    dot.edge('M4_FR', 'M5_FR')
    dot.edge('M5_FR', 'J3_FR')
    dot.edge('J3_FR', 'A2_FR', label=' OK')
    dot.edge('A2_FR', 'END_FR')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Frenos' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_frenos_final()