import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_control_calidad():
    dot = Digraph('DPO_CALIDAD_BJX', filename='DPO_CORE_A12_CALIDAD_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional [cite: 7-9, 946]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A12. Control de Calidad</B></TD>
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
        c.node('1', '1\\nLimpia unidad y bahía;\\nretira refacciones\\nusadas (para cliente)')
        c.node('2', '2\\nNotifica término de\\nservicio para inspección')

    # --- CARRIL 2: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\nInspección física vs\\nOrden de Servicio y\\nmanual de reparación')
        c.node('4', '4\\n¿Pasa Prueba\\nTécnica?', shape='diamond', fillcolor='#FFFDE7')
        c.node('5', '5\\nRealiza prueba de ruta\\ny escaneo final de\\nconfirmación (Cero DTC)')
        c.node('6', '6\\nFirma liberación técnica\\ny actualiza Notion')

    # --- CARRIL 3: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nInspección estética:\\nLimpieza, niveles y\\nkit de protección')
        c.node('8', '8\\n¿Calidad\\nConforme?', shape='diamond', fillcolor='#FFFDE7')
        c.node('9', '9\\nCarga reporte de calidad\\nfinal en Notion')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    
    # Decisión: Prueba Técnica
    dot.edge('4', '1', label=' NO', style='dashed')
    dot.edge('4', '5', label=' SÍ')
    
    dot.edge('5', '6')
    dot.edge('6', '7')
    dot.edge('7', '8')
    
    # Decisión: Calidad Estética
    dot.edge('8', '1', label=' NO', style='dashed')
    dot.edge('8', '9', label=' SÍ')
    
    dot.edge('9', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA [cite: 34-41]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Jefe de Taller</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 12/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A12: Control de Calidad generado.")

if __name__ == "__main__":
    generar_dpo_control_calidad()