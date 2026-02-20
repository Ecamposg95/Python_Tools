import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_recepcion_unidad():
    dot = Digraph('DPO_RECEPCION_BJX', filename='DPO_CORE_A2_RECEPCION_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Flujo Horizontal con Carriles Verticales)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado (Basado en DPO de RRHH) [cite: 7, 8, 9]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A2. Recepción de Unidad</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.0', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.0', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nBienvenida al cliente\\ny verificación de cita')
        c.node('2', '2\\nValidación de datos\\ny generación de\\norden preliminar')
        c.node('7', '7\\nExplicación de términos\\ny recolección de firma')
        c.node('9', '9\\nActualización de estatus\\nen Notion y entrega\\nde copia al cliente')

    # --- CARRIL 2: TÉCNICO / VALUADOR ---
    with dot.subgraph(name='cluster_tecnico') as c:
        c.attr(label='Técnico / Valuador', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\nInspección visual 360°\\n(Golpes, rayones, luces)')
        c.node('4', '4\\nInventario de interiores\\n(Pertenencias, niveles,\\nkilometraje)')
        c.node('5', '5\\n¿Hallazgos de\\ndaño previo?', shape='diamond', fillcolor='#FFFDE7')
        c.node('6', '6\\nCaptura de evidencias\\nfotográficas en Notion')
        c.node('8', '8\\nInstalación de kit de\\nprotección y traslado\\na zona STBY')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    dot.edge('4', '5')
    
    # Decisión: Hallazgos
    dot.edge('5', '6', label=' SÍ')
    dot.edge('5', '7', label=' NO')
    dot.edge('6', '7')
    
    dot.edge('7', '8')
    dot.edge('8', '9')
    dot.edge('9', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Nivel de detalle RRHH) [cite: 40, 41]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Jefe de Taller</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 02/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A2: Recepción de Unidad generado.")

if __name__ == "__main__":
    generar_dpo_recepcion_unidad()