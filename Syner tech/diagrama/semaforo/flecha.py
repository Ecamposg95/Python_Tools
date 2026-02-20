import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_flechas_final():
    dot = Digraph('Flechas_Final', filename='proc_12_flechas_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE FLECHAS (CV AXLE) - SOP\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_FL', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_FL', 'Recepción: Tronido al Girar\no Vibración en Tracción')
        c.node('A2_FL', 'Cierre de Orden y\nValidación de Silencio')
        c.node('END_FL', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_FL', 'Inspección: ¿Cubrepolvo\nRoto o Fuga de Grasa?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_FL', 'Diagnóstico de Tripoides\ny Baleros Internos')
        c.node('J3_FL', 'Verificación de Apriete\ny Juego Longitudinal')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_FL', 'Desmontaje de Rueda,\nMaza y Flecha Dañada')
        c.node('M2_FL', 'Limpieza de Estrías y\nRetenes de Transmisión')
        c.node('M3_FL', 'Instalación de Flecha\nNueva y Seguro de Maza')
        c.node('M4_FL', 'Reponer Nivel de Aceite\nde Caja (Si Aplica)')
        c.node('M5_FL', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_FL', '¿Flecha/Espiga en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_FL', 'Surtir Flecha Completa,\nGrasa y Abrazaderas')
        c.node('S3_FL', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_FL', 'A1_FL')
    dot.edge('A1_FL', 'J1_FL')
    
    # Decisión de Inspección
    dot.edge('J1_FL', 'J2_FL', label=' SÍ')
    dot.edge('J1_FL', 'M1_FL', label=' NO')
    dot.edge('J2_FL', 'M1_FL', label=' OK')
    
    # Interacción Almacén
    dot.edge('M1_FL', 'S1_FL', label=' Solicitar')
    dot.edge('S1_FL', 'S3_FL', label=' NO')
    dot.edge('S3_FL', 'S2_FL')
    dot.edge('S1_FL', 'S2_FL', label=' SÍ')
    dot.edge('S2_FL', 'M2_FL')
    
    # Finalización Técnica
    dot.edge('M2_FL', 'M3_FL')
    dot.edge('M3_FL', 'M4_FL')
    dot.edge('M4_FL', 'M5_FL')
    dot.edge('M5_FL', 'J3_FL')
    dot.edge('J3_FL', 'A2_FL', label=' OK')
    dot.edge('A2_FL', 'END_FL')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Flechas' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_flechas_final()