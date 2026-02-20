import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_cotizacion():
    dot = Digraph('DPO_COTIZACION_BJX', filename='DPO_CORE_A6_COTIZACION_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH [cite: 7, 43])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A6. Cotización</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbología Estándar [cite: 3, 20])
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nRecibe diagnóstico\\ntecnico y lista de\\nrefacciones sugeridas')
        c.node('5', '5\\nCalcula costos de MO\\nsegún tabulador de\\ntiempos estándar')
        c.node('6', '6\\n¿Aplica promoción\\no descuento?', shape='diamond', fillcolor='#FFFDE7')
        c.node('8', '8\\nGenera PDF de cotización\\ny actualiza tablero\\nen Notion')

    # --- CARRIL 2: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\nVerifica existencias\\nen inventario y\\nprecios vigentes')
        c.node('3', '3\\n¿Piezas en stock?', shape='diamond', fillcolor='#FFFDE7')
        c.node('4', '4\\nSolicita cotización a\\nproveedores externos\\n(Urgente)')

    # --- CARRIL 3: ADMINISTRACIÓN ---
    with dot.subgraph(name='cluster_admin') as c:
        c.attr(label='Administración', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nAutoriza descuentos\\nespeciales o cortesías\\nsegún política')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Stock
    dot.edge('3', '5', label=' SÍ')
    dot.edge('3', '4', label=' NO')
    dot.edge('4', '5')
    
    dot.edge('5', '6')
    
    # Decisión: Descuento
    dot.edge('6', '7', label=' SÍ')
    dot.edge('6', '8', label=' NO')
    dot.edge('7', '8')
    
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control de Calidad y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Control de Inventarios</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 06/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A6: Cotización generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_cotizacion()