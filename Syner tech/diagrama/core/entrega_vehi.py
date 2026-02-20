import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_entrega_vehiculo():
    dot = Digraph('DPO_ENTREGA_BJX', filename='DPO_CORE_A16_ENTREGA_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A16. Entrega del vehículo</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nVerifica estatus de "Pagado"\\ny solicita unidad a la\\nzona de entrega')
        c.node('4', '4\\nExplica trabajos realizados,\\nentrega piezas usadas\\ny póliza de garantía')
        c.node('7', '7\\nRecaba firma de conformidad\\nen la orden de servicio\\ny encuesta de salida')
        c.node('8', '8\\nEntrega llaves, pase de\\nsalida y despide al\\ncliente')

    # --- CARRIL 2: LAVADO / DETALLADO ---
    with dot.subgraph(name='cluster_lavado') as c:
        c.attr(label='Lavado / Detallado', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\nRealiza limpieza final de\\ninteriores, cristales y\\nabrillantado de llantas')
        c.node('3', '3\\nRetira kit de protección\\n(Funda de asiento, piso\\ny volante)')

    # --- CARRIL 3: CLIENTE ---
    with dot.subgraph(name='cluster_cliente') as c:
        c.attr(label='Cliente', style='dotted', fontname='Arial Bold')
        c.node('5', '5\\nInspección visual 360°\\n(Validación de estética\\ny niveles)')
        c.node('6', '6\\n¿Conforme con el\\nservicio?', shape='diamond', fillcolor='#FFFDE7')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    dot.edge('4', '5')
    dot.edge('5', '6')
    
    # Decisión: Conformidad del Cliente
    dot.edge('6', '7', label=' SÍ')
    dot.edge('6', '1', label=' NO / Ajuste', style='dashed')
    
    dot.edge('7', '8')
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Atención al Cliente</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 16/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A16: Entrega del vehículo generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_entrega_vehiculo()