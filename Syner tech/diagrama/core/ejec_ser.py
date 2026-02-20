import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_ejecucion_servicio():
    dot = Digraph('DPO_EJECUCION_BJX', filename='DPO_CORE_A10_EJECUCION_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH) [cite: 7, 43, 95]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A10. Ejecución del Servicio</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbología Estándar)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: TÉCNICO MECÁNICO ---
    with dot.subgraph(name='cluster_tecnico') as c:
        c.attr(label='Técnico Mecánico', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nInstala kit de protección\\ny prepara herramientas\\ny EPP')
        c.node('2', '2\\nEjecuta el servicio según\\norden de trabajo y\\nmanual de taller')
        c.node('3', '3\\n¿Detecta falla\\nadicional?', shape='diamond', fillcolor='#FFFDE7')
        c.node('5', '5\\nRealiza pruebas de apriete,\\nniveles y funcionamiento\\nparcial')
        c.node('6', '6\\nCarga evidencias de\\ncomponentes instalados\\nen Notion')

    # --- CARRIL 2: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('4', '4\\nValida hallazgo adicional\\ny notifica a la Asesora\\npara recotizar')
        c.node('7', '7\\nSupervisa avance técnico\\ny cumplimiento de\\ntiempos estándar')

    # --- CARRIL 3: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('8', '8\\nMonitorea estatus y\\nmantiene informado al\\ncliente (WhatsApp)')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Falla Adicional
    dot.edge('3', '4', label=' SÍ')
    dot.edge('3', '5', label=' NO')
    
    dot.edge('4', '8')
    dot.edge('5', '6')
    dot.edge('6', '7')
    dot.edge('7', '8')
    
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control de Calidad y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Jefe de Taller</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 10/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A10: Ejecución del Servicio generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_ejecucion_servicio()