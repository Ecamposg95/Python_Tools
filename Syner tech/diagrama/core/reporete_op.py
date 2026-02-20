import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_reporteo_operativo():
    dot = Digraph('DPO_REPORTEO_BJX', filename='DPO_CORE_A18_REPORTEO_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A18. Reporteo operativo</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA / OPERACIONES ---
    with dot.subgraph(name='cluster_operaciones') as c:
        c.attr(label='Asesora / Operaciones', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nExtrae datos de ventas,\\nticket promedio y NPS\\ndesde Notion')
        c.node('2', '2\\nReporta estatus de\\nórdenes abiertas, en\\nSTBY y terminadas')

    # --- CARRIL 2: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\nConsolida métricas de\\neficiencia técnica y\\nuso de bahías')
        c.node('4', '4\\nReporta mermas, daños\\nen herramienta y piezas\\ndefectuosas')

    # --- CARRIL 3: ADMINISTRACIÓN / DIRECCIÓN ---
    with dot.subgraph(name='cluster_admin') as c:
        c.attr(label='Administración / Dirección', style='dotted', fontname='Arial Bold')
        c.node('5', '5\\nIntegra reporte financiero\\n(Ingresos vs Egresos de\\nrefacciones/nómina)')
        c.node('6', '6\\n¿Existen desviaciones\\nfuera de límites?', shape='diamond', fillcolor='#FFFDE7')
        c.node('7', '7\\nPresenta Dashboard de\\nKPIs en Junta Operativa\\nMensual')
        c.node('8', '8\\nEstablece planes de\\nmejora y objetivos\\npara el siguiente mes')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    dot.edge('4', '5')
    dot.edge('5', '6')
    
    # Decisión: Desviaciones
    dot.edge('6', '8', label=' SÍ')
    dot.edge('6', '7', label=' NO')
    
    dot.edge('7', '8')
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Gerencia Operativa</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 18/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A18: Reporteo operativo generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_reporteo_operativo()