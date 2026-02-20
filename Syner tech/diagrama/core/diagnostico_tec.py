import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_diagnostico_tecnico():
    dot = Digraph('DPO_DIAGNOSTICO_BJX', filename='DPO_CORE_A5_DIAGNOSTICO_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A5. Diagnóstico Técnico</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbología Estándar)
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nRecibe orden de servicio\\ny asigna técnico\\nespecialista y bahía')
        c.node('8', '8\\nValida hallazgos técnicos\\ny autoriza paso a\\nárea de cotización')

    # --- CARRIL 2: TÉCNICO ESPECIALISTA ---
    with dot.subgraph(name='cluster_tecnico') as c:
        c.attr(label='Técnico Especialista', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\nRealiza inspección visual\\ny física de puntos de\\nseguridad (Checklist)')
        c.node('3', '3\\n¿Requiere diagnóstico\\nespecializado o escaneo?', shape='diamond', fillcolor='#FFFDE7')
        c.node('4', '4\\nEjecuta pruebas de ruta,\\nescaneo electrónico o\\npruebas de presión')
        c.node('5', '5\\nIdentifica piezas de\\ndesgaste y requerimiento\\nde mano de obra')
        c.node('6', '6\\nCaptura evidencias\\nfotográficas y video\\nde fallas en Notion')
        c.node('7', '7\\nConsolida reporte técnico\\ndetallado con causa raíz')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Diagnóstico Especializado
    dot.edge('3', '4', label=' SÍ')
    dot.edge('3', '5', label=' NO')
    
    dot.edge('4', '5')
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
            <TD>Hoja: 05/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A5: Diagnóstico Técnico generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_diagnostico_tecnico()