import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_bateria():
    # rankdir='LR' para carriles horizontales estilo Contraloría
    dot = Digraph('Cambio_Bateria', filename='proc_03_cambio_bateria', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA MODERNA ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO OPERATIVO: CAMBIO DE BATERÍA\nSISTEMA SYNER_BJX | MÉXICO 2026\n ', 
             labelloc='t', fontcolor='#2c3e50', fontname='Segoe UI Bold')

    # Estilo de Nodos: Rectángulos limpios y profesionales
    dot.attr('node', shape='rect', style='filled', 
             fillcolor='#ffffff', color='#bdc3c7', penwidth='1.5',
             fontname='Segoe UI', fontsize='9', fontcolor='#34495e',
             height='0.6', width='1.6')

    # Estilo de Flechas
    dot.attr('edge', color='#7f8c8d', penwidth='1.2', arrowhead='vee', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS (Azul) ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', 
               fontname='Segoe UI Bold', fontcolor='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_BAT', 'INICIO', shape='oval', fillcolor='#d5f5e3', color='#2ecc71')
        c.node('A1_BAT', 'Recepción:\nFalla de Arranque')
        c.node('A2_BAT', 'Apertura de Orden\nen Notion')
        c.node('A3_BAT', 'Firma Aceptación\ny Encuesta Final')
        c.node('END_BAT', 'FIN', shape='oval', fillcolor='#fadbd8', color='#e74c3c')

    # --- CARRIL 2: JEFE DE MECÁNICOS (Gris) ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', 
               fontname='Segoe UI Bold', fontcolor='#34495e', bgcolor='#f8f9f9')
        c.node('J1_BAT', 'Prueba de Alternador\n(Validar Carga)')
        c.node('J2_BAT', 'Asignar Técnico\nEléctrico')
        c.node('J3_BAT', 'Validación de\nVoltajes Finales')

    # --- CARRIL 3: MECÁNICO (PASOS TÉCNICOS) ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', 
               fontname='Segoe UI Bold', fontcolor='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_BAT', 'Test de CCA y\nVoltaje Inicial')
        c.node('M2_BAT', 'Limpieza de Bornes\ny Terminales')
        c.node('M3_BAT', 'Instalación con\nRespaldo de Memoria')
        c.node('M4_BAT', 'Configuración de\nComputadora (Scan)')
        c.node('M5_BAT', 'Carga de Evidencia\nen Notion')

    # --- CARRIL 4: ALMACÉN (Naranja) ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', 
               fontname='Segoe UI Bold', fontcolor='#d35400', bgcolor='#fffdf9')
        c.node('S1_BAT', 'Surtir Batería\n(LTH / Bosch)')
        c.node('S2_BAT', 'Kit de Limpieza y\nProtector de Bornes')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_BAT', 'A1_BAT')
    dot.edge('A1_BAT', 'A2_BAT')
    dot.edge('A2_BAT', 'J1_BAT')
    dot.edge('J1_BAT', 'J2_BAT')
    dot.edge('J2_BAT', 'M1_BAT')
    
    # Interacción con Almacén
    dot.edge('M1_BAT', 'S1_BAT', label=' Solicitar')
    dot.edge('S1_BAT', 'S2_BAT')
    dot.edge('S2_BAT', 'M2_BAT', label=' Surtir')
    
    dot.edge('M2_BAT', 'M3_BAT')
    dot.edge('M3_BAT', 'M4_BAT')
    dot.edge('M4_BAT', 'M5_BAT')
    dot.edge('M5_BAT', 'J3_BAT')
    dot.edge('J3_BAT', 'A3_BAT', label=' OK')
    dot.edge('A3_BAT', 'END_BAT')

    # Renderizado
    dot.render(cleanup=True)
    print("✅ Proceso 'Cambio de Batería' generado exitosamente.")

if __name__ == "__main__":
    generar_proceso_bateria()