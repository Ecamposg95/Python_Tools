import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_cierre_tecnico():
    dot = Digraph('DPO_CIERRE_BJX', filename='DPO_CORE_A13_CIERRE_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH) 
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A13. Cierre Técnico de Orden</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nVerifica conclusión de\\nprotocolo de calidad\\ny pruebas de ruta')
        c.node('2', '2\\nFirma orden física y\\nconsolida reporte final\\nen Notion')

    # --- CARRIL 2: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\nConcilia refacciones\\nsolicitadas vs piezas\\ninstaladas')
        c.node('4', '4\\n¿Existen\\ndiscrepancias?', shape='diamond', fillcolor='#FFFDE7')
        c.node('5', '5\\nRealiza ajustes de\\ninventario o cargos\\nadicionales a la orden')

    # --- CARRIL 3: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('6', '6\\nValida conceptos de\\nmano de obra y carga\\nfinal de evidencias')
        c.node('7', '7\\nCambia estatus de orden\\na "Lista para Cobro"\\nen sistema y Notion')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    
    # Decisión: Discrepancias en Refacciones
    dot.edge('4', '5', label=' SÍ')
    dot.edge('4', '6', label=' NO')
    
    dot.edge('5', '6')
    dot.edge('6', '7')
    
    dot.edge('7', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Control Interno</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 13/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A13: Cierre Técnico de Orden generado.")

if __name__ == "__main__":
    generar_dpo_cierre_tecnico()