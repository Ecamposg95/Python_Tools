import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_llanta_final():
    dot = Digraph('Cambio_Llanta_Final', filename='proc_02_llanta_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE LLANTA (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos (Contraloría/Estructurado)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_LL', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_LL', 'Recepción de Unidad y\nValidación de Medida')
        c.node('A2_LL', 'Cierre de Orden\ny Cobro en Sistema')
        c.node('END_LL', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_LL', 'Inspección de Rin\ny Geometría')
        c.node('J2_LL', '¿Rin en Buen Estado?', shape='diamond', fillcolor='#fff9c4')
        c.node('J3_LL', 'Notificar Daño Estructural\na Cliente')
        c.node('J4_LL', 'Validación Final de\nTorque y Balanceo')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_LL', 'Desmontaje de\nLlanta Dañada')
        c.node('M2_LL', 'Montaje de Pieza Nueva\ny Válvula')
        c.node('M3_LL', 'Balanceo Computarizado')
        c.node('M4_LL', 'Carga de Evidencia\n(Notion: DOT/Dibujo)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_LL', '¿Medida en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_LL', 'Solicitar Compra\nUrgente')
        c.node('S3_LL', 'Entrega de Neumático\ny Plomos de Balanceo')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_LL', 'A1_LL')
    dot.edge('A1_LL', 'J1_LL')
    dot.edge('J1_LL', 'J2_LL')
    
    # Decisión del Rin
    dot.edge('J2_LL', 'J3_LL', label=' NO')
    dot.edge('J2_LL', 'M1_LL', label=' SÍ')
    dot.edge('J3_LL', 'A2_LL', label=' Reportar')
    
    # Decisión de Stock
    dot.edge('M1_LL', 'S1_LL', label=' Solicitar')
    dot.edge('S1_LL', 'S2_LL', label=' NO')
    dot.edge('S2_LL', 'S3_LL')
    dot.edge('S1_LL', 'S3_LL', label=' SÍ')
    dot.edge('S3_LL', 'M2_LL')
    
    dot.edge('M2_LL', 'M3_LL')
    dot.edge('M3_LL', 'M4_LL')
    dot.edge('M4_LL', 'J4_LL')
    dot.edge('J4_LL', 'A2_LL', label=' OK')
    dot.edge('A2_LL', 'END_LL')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Llanta' con decisiones generado.")

if __name__ == "__main__":
    generar_proceso_llanta_final()