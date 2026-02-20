import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_afinacion_final():
    dot = Digraph('Afinacion_Final', filename='proc_06_afinacion_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: AFINACIÓN MAYOR (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_AF', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_AF', 'Recepción: Mantenimiento\nPreventivo/Kilometraje')
        c.node('A2_AF', 'Cierre de Orden y\nReporte de Consumo')
        c.node('END_AF', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_AF', 'Escaneo Inicial:\n¿Códigos de Error?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_AF', 'Diagnóstico de Sensores\ny Actuadores')
        c.node('J3_AF', 'Validación de Emisiones\ny Marcha Mínima')

    # --- CARRIL 3: MECÁNICO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_AF', 'Lavado de Inyectores\n(Presurizado/Boyita)')
        c.node('M2_AF', 'Limpieza de Cuerpo de\nAceleración y MAF')
        c.node('M3_AF', 'Cambio de Bujías,\nFiltros y Aceite')
        c.node('M4_AF', 'Aprendizaje de Cuerpo\n(Relenty con Scanner)')
        c.node('M5_AF', 'Carga de Evidencia\nen Notion (Antes/Después)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_AF', '¿Kit Completo en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_AF', 'Surtir Kit: Bujías, Aceite,\nFiltros y Limpiadores')
        c.node('S3_AF', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_AF', 'A1_AF')
    dot.edge('A1_AF', 'J1_AF')
    
    # Decisión de Errores de Motor
    dot.edge('J1_AF', 'J2_AF', label=' SÍ')
    dot.edge('J1_AF', 'M1_AF', label=' NO')
    dot.edge('J2_AF', 'M1_AF', label=' Corregido')
    
    # Interacción Almacén
    dot.edge('M1_AF', 'S1_AF', label=' Solicitar')
    dot.edge('S1_AF', 'S3_AF', label=' NO')
    dot.edge('S3_AF', 'S2_AF')
    dot.edge('S1_AF', 'S2_AF', label=' SÍ')
    dot.edge('S2_AF', 'M2_AF')
    
    # Finalización Técnica
    dot.edge('M2_AF', 'M3_AF')
    dot.edge('M3_AF', 'M4_AF')
    dot.edge('M4_AF', 'M5_AF')
    dot.edge('M5_AF', 'J3_AF')
    dot.edge('J3_AF', 'A2_AF', label=' OK')
    dot.edge('A2_AF', 'END_AF')

    dot.render(cleanup=True)
    print("✅ Proceso 'Afinación Mayor' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_afinacion_final()