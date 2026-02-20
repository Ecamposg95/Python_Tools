import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_clutch_final():
    dot = Digraph('Cambio_Clutch_Final', filename='proc_11_clutch_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE KIT DE CLUTCH (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_CLU', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_CLU', 'Recepción: Reporte de\nPatinamiento o Pedal Duro')
        c.node('A2_CLU', 'Cierre de Orden y\nValidación de Corte')
        c.node('END_CLU', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_CLU', 'Prueba de Esfuerzo:\n¿Pátina el Disco?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_CLU', '¿Volante Motor\nRequiere Rectificado?', shape='diamond', fillcolor='#fff9c4')
        c.node('J3_CLU', 'Validación de Carrera\nde Pedal y Cambios')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_CLU', 'Bajado de Transmisión\ny Desmonte de Kit Viejo')
        c.node('M2_CLU', 'Rectificado de Volante\ny Cambio de Piloto')
        c.node('M3_CLU', 'Instalación de Kit Nuevo\n(Centrado de Disco)')
        c.node('M4_CLU', 'Purgado de Sistema\nHidráulico / Ajuste')
        c.node('M5_CLU', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_CLU', '¿Kit y Collarín\nen Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_CLU', 'Surtir Kit, Aceite de\nCaja y Líquido')
        c.node('S3_CLU', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_CLU', 'A1_CLU')
    dot.edge('A1_CLU', 'J1_CLU')
    
    # Decisión de Falla
    dot.edge('J1_CLU', 'M1_CLU', label=' SÍ')
    dot.edge('J1_CLU', 'A2_CLU', label=' NO (Ajuste)')
    
    # Evaluación de Volante
    dot.edge('M1_CLU', 'J2_CLU')
    dot.edge('J2_CLU', 'M2_CLU', label=' SÍ')
    dot.edge('J2_CLU', 'M3_CLU', label=' NO')
    
    # Interacción Almacén
    dot.edge('M2_CLU', 'S1_CLU', label=' Solicitar')
    dot.edge('S1_CLU', 'S3_CLU', label=' NO')
    dot.edge('S3_CLU', 'S2_CLU')
    dot.edge('S1_CLU', 'S2_CLU', label=' SÍ')
    dot.edge('S2_CLU', 'M3_CLU')
    
    # Finalización Técnica
    dot.edge('M3_CLU', 'M4_CLU')
    dot.edge('M4_CLU', 'M5_CLU')
    dot.edge('M5_CLU', 'J3_CLU')
    dot.edge('J3_CLU', 'A2_CLU', label=' OK')
    dot.edge('A2_CLU', 'END_CLU')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Clutch' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_clutch_final()