import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_horquilla_decisiones():
    dot = Digraph('Horquilla_Decisiones', filename='proc_01_horquilla_final', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: CAMBIO DE HORQUILLA (CON DECISIONES)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1', 'Recepción y Registro\nen Notion')
        c.node('A2', 'Firma y Entrega')
        c.node('END', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1', 'Diagnóstico y\nAsignación')
        c.node('J2', '¿Trabajo Conforme?', shape='diamond', fillcolor='#fff9c4')
        c.node('J3', 'Validar Alineación')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1', 'Desmontaje de\nHorquilla Dañada')
        c.node('M2', 'Instalación de\nPieza Nueva')
        c.node('M3', 'Carga Evidencias\nen Notion')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1', '¿Hay Existencia?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2', 'Solicitar Compra')
        c.node('S3', 'Entrega de Kit\n(Horquilla/Pernos)')

    # --- FLUJO CON LÓGICA DE DECISIÓN ---
    dot.edge('ST', 'A1')
    dot.edge('A1', 'J1')
    dot.edge('J1', 'M1')
    
    # Decisión de Stock
    dot.edge('M1', 'S1', label=' Solicitar')
    dot.edge('S1', 'S2', label=' NO')
    dot.edge('S2', 'S3', label=' Recibir')
    dot.edge('S1', 'S3', label=' SÍ')
    dot.edge('S3', 'M2')
    
    dot.edge('M2', 'M3')
    dot.edge('M3', 'J2')
    
    # Decisión de Calidad
    dot.edge('J2', 'M2', label=' NO', style='dashed', color='red')
    dot.edge('J2', 'J3', label=' SÍ')
    dot.edge('J3', 'A2')
    dot.edge('A2', 'END')

    dot.render(cleanup=True)
    print("✅ Proceso con rombos de decisión generado.")

if __name__ == "__main__":
    generar_proceso_horquilla_decisiones()