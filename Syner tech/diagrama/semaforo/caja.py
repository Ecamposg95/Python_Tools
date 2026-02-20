import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_caja_velocidades():
    dot = Digraph('Reparacion_Caja', filename='proc_14_reparacion_caja', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: REPARACIÓN DE CAJA DE VELOCIDADES (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos (Formato Contraloría)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_CJ', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_CJ', 'Recepción: Falla en Cambios\no Modo Seguro (Limp Mode)')
        c.node('A2_CJ', 'Cierre de Orden y\nPrueba de Ruta con Cliente')
        c.node('END_CJ', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_CJ', 'Escaneo TBU:\n¿Falla Electrónica?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_CJ', 'Diagnóstico de Solenoides\ny Arnés Externo')
        c.node('J3_CJ', 'Validación de Presiones\ny Aprendizaje de Cambios')

    # --- CARRIL 3: MECÁNICO (ESPECIALISTA TRANSMISIONES) ---
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_CJ', 'Bajado de Caja e\nInspección de Turbina')
        c.node('M2_CJ', 'Desarme y Limpieza de\nCuerpo de Válvulas')
        c.node('M3_CJ', 'Cambio de Master Kit\n(Discos, Ligas y Filtro)')
        c.node('M4_CJ', 'Montaje y Reposición de\nAceite Sintético (ATF)')
        c.node('M5_CJ', 'Carga de Evidencia\nen Notion (Fotos)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_CJ', '¿Master Kit en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_CJ', 'Surtir Kit de Reparación,\nAceite ATF y Retenes')
        c.node('S3_CJ', 'Solicitar Importación\nde Partes Internas')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_CJ', 'A1_CJ')
    dot.edge('A1_CJ', 'J1_CJ')
    
    # Decisión Electrónica vs Mecánica
    dot.edge('J1_CJ', 'J2_CJ', label=' SÍ')
    dot.edge('J1_CJ', 'M1_CJ', label=' NO (Mecánica)')
    dot.edge('J2_CJ', 'A2_CJ', label=' Corregido')
    
    # Interacción Almacén
    dot.edge('M1_CJ', 'S1_CJ', label=' Solicitar')
    dot.edge('S1_CJ', 'S3_CJ', label=' NO')
    dot.edge('S3_CJ', 'S2_CJ')
    dot.edge('S1_CJ', 'S2_CJ', label=' SÍ')
    dot.edge('S2_CJ', 'M2_CJ')
    
    # Finalización Técnica
    dot.edge('M2_CJ', 'M3_CJ')
    dot.edge('M3_CJ', 'M4_CJ')
    dot.edge('M4_CJ', 'M5_CJ')
    dot.edge('M5_CJ', 'J3_CJ')
    dot.edge('J3_CJ', 'A2_CJ', label=' OK')
    dot.edge('A2_CJ', 'END_CJ')

    dot.render(cleanup=True)
    print("✅ Proceso 'Reparación de Caja' generado exitosamente.")

if __name__ == "__main__":
    generar_proceso_caja_velocidades()