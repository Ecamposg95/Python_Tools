import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_planeacion_trabajo():
    dot = Digraph('DPO_PLANEACION_BJX', filename='DPO_CORE_A8_PLANEACION_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH) [cite: 7, 8, 9]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A8. Planeación del Trabajo</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbología Estándar [cite: 3, 20, 33])
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nRevisa carga de trabajo\\ny prioridad de órdenes\\naprobadas en Notion')
        c.node('2', '2\\nAsigna Técnico según\\nespecialidad y\\ndisponibilidad de bahía')
        c.node('3', '3\\n¿Requiere herramienta\\nespecializada?\\n(Prensa, Scanner, etc.)', shape='diamond', fillcolor='#FFFDE7')
        c.node('6', '6\\nEntrega orden física,\\nllaves y define meta\\nde tiempo de ejecución')

    # --- CARRIL 2: ALMACÉN / HERRAMENTAL ---
    with dot.subgraph(name='cluster_herramental') as c:
        c.attr(label='Almacén / Herramental', style='dotted', fontname='Arial Bold')
        c.node('4', '4\\nVerifica disponibilidad\\ny estado de equipo\\nespecializado')
        c.node('5', '5\\nReserva y prepara kit\\nde herramientas para\\nla estación asignada')

    # --- CARRIL 3: TÉCNICO MECÁNICO ---
    with dot.subgraph(name='cluster_tecnico') as c:
        c.attr(label='Técnico Mecánico', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nRecibe unidad y equipo;\\nactualiza estatus de\\norden a "En Proceso"')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Herramienta Especializada
    dot.edge('3', '4', label=' SÍ')
    dot.edge('3', '6', label=' NO')
    
    dot.edge('4', '5')
    dot.edge('5', '6')
    dot.edge('6', '7')
    
    dot.edge('7', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Jefe de Taller</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 08/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A8: Planeación del Trabajo generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_planeacion_trabajo()