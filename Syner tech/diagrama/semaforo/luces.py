import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_luces_final():
    dot = Digraph('Cambio_Luces_Final', filename='proc_05_luces_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE LUCES (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_LUZ', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_LUZ', 'Recepción: Falla en\nIluminación (Int/Ext)')
        c.node('A2_LUZ', 'Cierre de Orden\ny Entrega de Unidad')
        c.node('END_LUZ', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_LUZ', 'Inspección Eléctrica:\n¿Llega Voltaje?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_LUZ', 'Revisión de Fusibles\ny Relevadores')
        c.node('J3_LUZ', 'Validar Alineación de\nHaz de Luz (Luxómetro)')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_LUZ', 'Acceso a Faro y\nExtracción de Bulbo')
        c.node('M2_LUZ', 'Limpieza de Conector\ncon Limpiador de Contactos')
        c.node('M3_LUZ', 'Sustitución de Bulbo y\nPrueba de Encendido')
        c.node('M4_LUZ', 'Carga de Evidencia\nen Notion (Antes/Después)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_LUZ', '¿Bulbo en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_LUZ', 'Surtir Bulbo (LED/\nHalógeno) y Fusibles')
        c.node('S3_LUZ', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_LUZ', 'A1_LUZ')
    dot.edge('A1_LUZ', 'J1_LUZ')
    
    # Decisión Eléctrica Inicial
    dot.edge('J1_LUZ', 'J2_LUZ', label=' NO')
    dot.edge('J1_LUZ', 'M1_LUZ', label=' SÍ')
    dot.edge('J2_LUZ', 'M1_LUZ', label=' Corregido')
    
    # Interacción Almacén
    dot.edge('M1_LUZ', 'S1_LUZ', label=' Solicitar')
    dot.edge('S1_LUZ', 'S3_LUZ', label=' NO')
    dot.edge('S3_LUZ', 'S2_LUZ')
    dot.edge('S1_LUZ', 'S2_LUZ', label=' SÍ')
    dot.edge('S2_LUZ', 'M2_LUZ')
    
    # Finalización
    dot.edge( 'M2_LUZ', 'M3_LUZ')
    dot.edge('M3_LUZ', 'M4_LUZ')
    dot.edge('M4_LUZ', 'J3_LUZ')
    dot.edge('J3_LUZ', 'A2_LUZ', label=' OK')
    dot.edge('A2_LUZ', 'END_LUZ')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Luces' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_luces_final()