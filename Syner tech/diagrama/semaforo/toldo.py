import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_soldadura_toldo():
    dot = Digraph('Soldadura_Toldo', filename='proc_08_soldadura_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: SOLDADURA DE TOLDO (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_SOL', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_SOL', 'Recepción: Daño Estructural\no Filtración en Toldo')
        c.node('A2_SOL', 'Cierre de Orden y\nValidación de Acabado')
        c.node('END_SOL', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_SOL', 'Evaluación de Daño:\n¿Compromete Seguridad?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_SOL', 'Notificar Sustitución\nde Panel Completo')
        c.node('J3_SOL', 'Validar Hermeticidad\ny Alineación de Postes')

    # --- CARRIL 3: MECÁNICO (ESPECIALISTA HOJALATERÍA) ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_SOL', 'Desmontaje de Cielo,\nAirbags y Molduras')
        c.node('M2_SOL', 'Protección Térmica de\nInteriores (Mantas)')
        c.node('M3_SOL', 'Soldadura (MIG/MAG)\ny Esmerilado de Puntos')
        c.node('M4_SOL', 'Aplicación de Sellador\ny Anticorrosivo')
        c.node('M5_SOL', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_SOL', '¿Insumos Disponibles?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_SOL', 'Surtir Microalambre, Gas,\nSellador y Mantas')
        c.node('S3_SOL', 'Solicitar Compra\nUrgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_SOL', 'A1_SOL')
    dot.edge('A1_SOL', 'J1_SOL')
    
    # Decisión de Seguridad Estructural
    dot.edge('J1_SOL', 'J2_SOL', label=' SÍ')
    dot.edge('J1_SOL', 'M1_SOL', label=' NO')
    dot.edge('J2_SOL', 'A2_SOL', label=' Reportar')
    
    # Interacción Almacén
    dot.edge('M1_SOL', 'S1_SOL', label=' Solicitar')
    dot.edge('S1_SOL', 'S3_SOL', label=' NO')
    dot.edge('S3_SOL', 'S2_SOL')
    dot.edge('S1_SOL', 'S2_SOL', label=' SÍ')
    dot.edge('S2_SOL', 'M2_SOL')
    
    # Finalización Técnica
    dot.edge('M2_SOL', 'M3_SOL')
    dot.edge('M3_SOL', 'M4_SOL')
    dot.edge('M4_SOL', 'M5_SOL')
    dot.edge('M5_SOL', 'J3_SOL')
    dot.edge('J3_SOL', 'A2_SOL', label=' OK')
    dot.edge('A2_SOL', 'END_SOL')

    dot.render(cleanup=True)
    print("✅ Proceso 'Soldadura de Toldo' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_soldadura_toldo()