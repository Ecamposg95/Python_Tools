import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_apertura_orden():
    dot = Digraph('DPO_APERTURA_BJX', filename='DPO_CORE_A4_APERTURA_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH [cite: 7, 8])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A4. Apertura de Orden de Servicio</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbolización Estándar)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.0', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.0', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nConsolida reporte de falla,\\ninventario y diagnóstico\\npreliminar')
        c.node('2', '2\\nGenera número de\\norden en sistema y\\nasigna folio físico')
        c.node('3', '3\\nEstablece compromiso de\\nentrega y costo\\nestimado inicial')
        c.node('6', '6\\nRecaba firma de\\naceptación y contrato\\nde adhesión')
        c.node('8', '8\\nEntrega copia de orden\\nal cliente y carga\\nPDF en Notion')

    # --- CARRIL 2: CLIENTE ---
    with dot.subgraph(name='cluster_cliente') as c:
        c.attr(label='Cliente', style='dotted', fontname='Arial Bold')
        c.node('4', '4\\n¿Acepta presupuesto\\ny tiempo de entrega?', shape='diamond', fillcolor='#FFFDE7')
        c.node('5', '5\\nRevisión de cláusulas\\ny condiciones de\\ngarantía')

    # --- CARRIL 3: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_taller') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nRecibe orden física y\\nprocede a planeación\\nde bahía')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    
    # Decisión: Aceptación del Cliente
    dot.edge('4', '5', label=' SÍ')
    dot.edge('4', 'FIN_CANC', label=' NO', style='dashed')
    dot.node('FIN_CANC', 'FIN (Cerrar Cita)', shape='oval', fillcolor='#FFEBEE')
    
    dot.edge('5', '6')
    dot.edge('6', '7')
    dot.edge('7', '8')
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Asesora Senior</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 04/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A4: Apertura de Orden generado.")

if __name__ == "__main__":
    generar_dpo_apertura_orden()