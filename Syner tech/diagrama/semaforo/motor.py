import os
from graphviz import Digraph

# Configuración de ruta para Graphviz en Windows
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_proceso_motor_final():
    dot = Digraph('Motor_Final', filename='proc_13_motor_decisiones', format='svg')
    
    # --- CONFIGURACIÓN ESTÉTICA SYNER GROUP ---
    dot.attr(rankdir='LR', fontname='Segoe UI, Arial', fontsize='16', compound='true', 
             nodesep='0.5', ranksep='0.8', bgcolor='#ffffff')
    
    dot.attr(label='DIAGRAMA DE PROCESO: REPARACIÓN O CAMBIO DE MOTOR (SOP)\nSYNER GROUP | CLIENTE: BJX MOTORS | 2026\n ', 
             labelloc='t', fontcolor='#1a1a1a', fontname='Segoe UI Bold')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#2c3e50', 
             penwidth='1.5', fontname='Segoe UI', fontsize='9', height='0.7', width='1.8')
    dot.attr('edge', color='#34495e', penwidth='1.2', arrowhead='normal', arrowsize='0.8')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='solid', color='#2980b9', bgcolor='#f4f9fd')
        c.node('ST_MOT', 'INICIO', shape='oval', fillcolor='#27ae60', fontcolor='white')
        c.node('A1_MOT', 'Recepción: Motor Desvielado,\nCalentamiento o Humo Azul')
        c.node('A2_MOT', 'Presentar Presupuesto\ny Tiempo Estimado')
        c.node('A3_MOT', 'Cierre de Orden y\nEntrega de Póliza de Garantía')
        c.node('END_MOT', 'FIN', shape='oval', fillcolor='#c0392b', fontcolor='white')

    # --- CARRIL 2: JEFE DE MECÁNICOS ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Mecánicos', style='solid', color='#7f8c8d', bgcolor='#f8f9f9')
        c.node('J1_MOT', 'Diagnóstico Mayor:\n¿Es Reparable?', shape='diamond', fillcolor='#fff9c4')
        c.node('J2_MOT', 'Evaluación de Monoblock\ny Cigüeñal (Rectificadora)')
        c.node('J3_MOT', 'Validación de Compresión\ny Presión de Aceite')

    # --- CARRIL 3: MECÁNICO (ESPECIALISTA MOTORES) ---
    with dot.subgraph(name='cluster_mecanico') as c:
        c.attr(label='Mecánico', style='solid', color='#27ae60', bgcolor='#f1fcf4')
        c.node('M1_MOT', 'Desmontaje Total de\nPeriféricos y Motor')
        c.node('M2_MOT', 'Limpieza Química y\nAnillado / Ajuste')
        c.node('M3_MOT', 'Montaje de Motor y\nPuesta a Tiempo')
        c.node('M4_MOT', 'Prueba de Asentamiento\ny Escaneo de Sensores')
        c.node('M5_MOT', 'Carga de Evidencia\nen Notion (Fotos/Video)')

    # --- CARRIL 4: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='solid', color='#f39c12', bgcolor='#fffdf9')
        c.node('S1_MOT', '¿Refacciones o Motor\nNuevo en Stock?', shape='diamond', fillcolor='#fff9c4')
        c.node('S2_MOT', 'Surtir Kit de Empaques,\nMetales y Aceite')
        c.node('S3_MOT', 'Gestionar Compra de\nMotor Completo')

    # --- FLUJO LÓGICO ---
    dot.edge('ST_MOT', 'A1_MOT')
    dot.edge('A1_MOT', 'J1_MOT')
    
    # Decisión de Reparación vs Cambio
    dot.edge('J1_MOT', 'J2_MOT', label=' REPARAR')
    dot.edge('J1_MOT', 'S3_MOT', label=' CAMBIO')
    
    # Interacción Almacén
    dot.edge('J2_MOT', 'M1_MOT')
    dot.edge('M1_MOT', 'S1_MOT', label=' Solicitar')
    dot.edge('S1_MOT', 'S3_MOT', label=' NO')
    dot.edge('S3_MOT', 'S2_MOT')
    dot.edge('S1_MOT', 'S2_MOT', label=' SÍ')
    dot.edge('S2_MOT', 'M2_MOT')
    
    # Finalización Técnica
    dot.edge('M2_MOT', 'M3_MOT')
    dot.edge('M3_MOT', 'M4_MOT')
    dot.edge('M4_MOT', 'M5_MOT')
    dot.edge('M5_MOT', 'J3_MOT')
    dot.edge('J3_MOT', 'A3_MOT', label=' OK')
    dot.edge('A3_MOT', 'END_MOT')

    dot.render(cleanup=True)
    print("✅ Proceso 'Reparación de Motor' con decisiones generado para BJX Motors.")

if __name__ == "__main__":
    generar_proceso_motor_final()