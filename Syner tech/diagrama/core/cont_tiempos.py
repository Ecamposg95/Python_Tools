import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_control_tiempos():
    dot = Digraph('DPO_TIEMPOS_BJX', filename='DPO_CORE_A11_TIEMPOS_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH) [cite: 7-9, 946]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A11. Control de Tiempos</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: TÉCNICO MECÁNICO ---
    with dot.subgraph(name='cluster_tecnico') as c:
        c.attr(label='Técnico Mecánico', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nRegistra hora de inicio\\nen sistema/Notion al\\nrecibir la unidad')
        c.node('2', '2\\nNotifica interrupciones\\n(Falta de refacción /\\nherramienta)')
        c.node('3', '3\\nRegistra hora de término\\ny solicita validación\\ndel Jefe de Taller')

    # --- CARRIL 2: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('4', '4\\nMonitorea avance en\\ntiempo real vs tiempo\\nestándar de manual')
        c.node('5', '5\\n¿Existe\\ndesviación / retraso?', shape='diamond', fillcolor='#FFFDE7')
        c.node('6', '6\\nIdentifica causa raíz\\ny ajusta planeación\\nde bahías')

    # --- CARRIL 3: ADMINISTRACIÓN ---
    with dot.subgraph(name='cluster_admin') as c:
        c.attr(label='Administración', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nCalcula eficiencia y\\nproductividad por técnico\\ny por servicio')
        c.node('8', '8\\nGenera reporte de KPIs\\npara junta operativa\\nmensual')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '4')
    dot.edge('4', '5')
    
    # Decisión: Retraso
    dot.edge('5', '6', label=' SÍ')
    dot.edge('5', '2', label=' NO')
    
    dot.edge('6', '2')
    dot.edge('2', '3')
    dot.edge('3', '7')
    dot.edge('7', '8')
    
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Administración</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 11/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A11: Control de Tiempos generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_control_tiempos()