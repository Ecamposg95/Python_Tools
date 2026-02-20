import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_espejos_final():
    dot = Digraph('Espejos_Final', filename='proc_07_espejos_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE ESPEJOS LATERALES (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_ESP', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_ESP', 'Recepción: Espejo Dañado\n(Cristal/Carcasa/Motor)')
        c.node('A2_ESP', 'Cierre de Orden y\nVerificación de Ajuste')
        c.node('END_ESP', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_ESP', 'Inspección de Función:\n¿Falla Eléctrica?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_ESP', 'Revisión de Cableado\ny Mando Central')
        c.node('J3_ESP', 'Validar Estética y\nAjuste sin Vibración')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_ESP', 'Desmontaje de Panel\nInterno de Puerta')
        c.node('M2_ESP', 'Desconexión Eléctrica\ny Retiro de Tornillería')
        c.node('M3_ESP', 'Instalación de Espejo\ny Sellado de Empaque')
        c.node('M4_ESP', 'Prueba de Motores\ny Direccional')
        c.node('M5_ESP', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_ESP', '¿Pieza en Color Correcto?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_ESP', 'Surtir Espejo Lateral\ny Grapas de Panel')
        c.node('S3_ESP', 'Solicitar Pintura o\nCambio de Carcasa')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_ESP', 'A1_ESP')
    dot.edge('A1_ESP', 'J1_ESP')
    
    # Decisión de Falla Eléctrica
    dot.edge('J1_ESP', 'J2_ESP', label=' SÍ')
    dot.edge('J1_ESP', 'M1_ESP', label=' NO')
    dot.edge('J2_ESP', 'M1_ESP', label=' OK')
    
    # Interacción Almacén
    dot.edge('M1_ESP', 'S1_ESP', label=' Solicitar')
    dot.edge('S1_ESP', 'S3_ESP', label=' NO')
    dot.edge('S3_ESP', 'S2_ESP')
    dot.edge('S1_ESP', 'S2_ESP', label=' SÍ')
    dot.edge('S2_ESP', 'M2_ESP')
    
    # Finalización Técnica
    dot.edge('M2_ESP', 'M3_ESP')
    dot.edge('M3_ESP', 'M4_ESP')
    dot.edge('M4_ESP', 'M5_ESP')
    dot.edge('M5_ESP', 'J3_ESP')
    dot.edge('J3_ESP', 'A2_ESP', label=' OK')
    dot.edge('A2_ESP', 'END_ESP')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Espejos' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_espejos_final()