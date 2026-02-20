import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_choque_final():
    dot = Digraph('Ingreso_Choque', filename='proc_15_choque_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: INGRESO POR CHOQUE (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos (Formato Contraloría)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA / VALUADOR ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora / Valuador', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_CH', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_CH', 'Inventario de Daños y\nRegistro 360° (Notion)')
        c.node('A2_CH', '¿Es Pérdida Total?', shape='diamond', fillcolor='#fff9c4')
        c.node('A3_CH', 'Gestión con Seguro\ny Cierre de Orden')
        c.node('END_CH', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE COLISIÓN ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Colisión', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_CH', '¿Daño en Chasis / Bastidor?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_CH', 'Validación de Color\ny Acabado de Pintura')
        c.node('J3_CH', 'Prueba de Hermeticidad\ny Cuadraje Final')

    # --- CARRIL 3: MECÁNICO / HOJALATERO ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Hojalatero / Pintor', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_CH', 'Estirado en Banco y\nReparación de Lámina')
        c.node('M2_CH', 'Preparación y Pintura\nen Cabina')
        c.node('M3_CH', 'Armado, Pulido y\nDetallado Estético')
        c.node('M4_CH', 'Carga de Evidencias\nen Notion (Antes/Después)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_CH', '¿Refacciones en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_CH', 'Surtir Láminas, Defensas\ny Kit de Pintura')
        c.node('S3_CH', 'Solicitar Compra de\nPiezas Originales')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_CH', 'A1_CH')
    dot.edge('A1_CH', 'A2_CH')
    
    # Decisión: Pérdida Total
    dot.edge('A2_CH', 'A3_CH', label=' SÍ')
    dot.edge('A2_CH', 'J1_CH', label=' NO')
    
    # Decisión: Estructura
    dot.edge('J1_CH', 'M1_CH', label=' SÍ (Uso de Banco)')
    dot.edge('J1_CH', 'M1_CH', label=' NO')
    
    # Interacción Almacén
    dot.edge('M1_CH', 'S1_CH', label=' Solicitar')
    dot.edge('S1_CH', 'S3_CH', label=' NO')
    dot.edge('S3_CH', 'S2_CH')
    dot.edge('S1_CH', 'S2_CH', label=' SÍ')
    dot.edge('S2_CH', 'M2_CH')
    
    # Finalización
    dot.edge('M2_CH', 'J2_CH')
    dot.edge('J2_CH', 'M3_CH', label=' OK')
    dot.edge('M3_CH', 'M4_CH')
    dot.edge('M4_CH', 'J3_CH')
    dot.edge('J3_CH', 'A3_CH', label=' OK')
    dot.edge('A3_CH', 'END_CH')

    dot.render(cleanup=True)
    print("✅ Proceso 'Ingreso por Choque' generado exitosamente.")

if __name__ == "__main__":
    generar_proceso_choque_final()