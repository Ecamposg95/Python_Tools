import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_diagrama_llanta():
    dot = Digraph('Cambio_Llanta', filename='proc_02_cambio_llanta', format='svg')
    
    # Atributos Estéticos Modernos
    dot.attr(rankdir='TB', fontname='Segoe UI,Arial', fontsize='18', compound='true', 
             nodesep='0.9', ranksep='0.6', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA OPERATIVO: CAMBIO DE LLANTA\nSISTEMA SYNER_BJX | MÉXICO 2026\n ', 
             labelloc='t', fontcolor='#2c3e50', fontname='Segoe UI Bold')

    # Estilo de Nodos
    dot.attr('node', shape='rect', style='filled,rounded', fillcolor='#ffffff', 
             color='#bdc3c7', penwidth='1.5', fontname='Segoe UI', fontsize='10')
    dot.attr('edge', color='#7f8c8d', penwidth='1.2', arrowhead='vee')

    # --- COLUMNA 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='filled', color='#ebf5fb', fontcolor='#2980b9', fontname='Segoe UI Bold')
        c.node('START', 'INICIO', shape='circle', fillcolor='#d5f5e3', color='#2ecc71', width='0.6')
        c.node('A1', 'Recepción: Identificar Llanta\n(Medida y Posición)')
        c.node('A2', 'Apertura de Orden\nen Notion')
        c.node('A3', 'Notificación de Listado\ny Cobro')
        c.node('END', 'FIN', shape='circle', fillcolor='#fadbd8', color='#e74c3c', width='0.6')

    # --- COLUMNA 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='filled', color='#f8f9f9', fontcolor='#7f8c8d', fontname='Segoe UI Bold')
        c.node('J1', 'Inspección de Rines\n(Golpes o Fisuras)')
        c.node('J2', 'Asignar Técnico\nde Montaje')
        c.node('J3', 'Verificación de Torque\ny Balanceo Final')

    # --- COLUMNA 3: MECÁNICO (PASOS TÉCNICOS) ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='filled', color='#e9f7ef', fontcolor='#27ae60', fontname='Segoe UI Bold')
        c.node('M1', 'Desmontaje y Extracción\nde Válvula Vieja')
        c.node('M2', 'Montaje de Llanta Nueva\n(Respetar Sentido de Giro)')
        c.node('M3', 'Balanceo Computarizado\n(Plomos Internos/Externos)')
        c.node('M4', 'Calibración de Presión\nsegún Fabricante (PSI)')
        c.node('M5', 'Carga de Evidencia en Notion\n(Foto de Dibujo y DOT)')

    # --- COLUMNA 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='filled', color='#fef5e7', fontcolor='#e67e22', fontname='Segoe UI Bold')
        c.node('S1', 'Surtir Neumático\n(Validar Medida)')
        c.node('S2', 'Kit de Válvula Nueva\ny Pesas de Balanceo')

    # --- FLUJO LÓGICO ---
    dot.edge('START', 'A1')
    dot.edge('A1', 'A2')
    dot.edge('A2', 'J1')
    dot.edge('J1', 'J2')
    dot.edge('J2', 'M1')
    
    # Interacción con Almacén
    dot.edge('M1', 'S1', label=' Solicitar Material')
    dot.edge('S1', 'S2')
    dot.edge('S2', 'M2', label=' Entrega')
    
    dot.edge('M2', 'M3')
    dot.edge('M3', 'M4')
    dot.edge('M4', 'M5')
    dot.edge('M5', 'J3')
    dot.edge('J3', 'A3', label=' Control OK')
    dot.edge('A3', 'END')

    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Llanta' generado exitosamente.")

if __name__ == "__main__":
    generar_diagrama_llanta()