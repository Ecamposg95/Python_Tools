import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_postventa():
    dot = Digraph('DPO_POSTVENTA_BJX', filename='DPO_CORE_A17_POSTVENTA_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX
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
            <TD><B>Core de Servicio | A17. Postventa / garantías</B></TD>
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
        c.node('1', '1\\nRealiza llamada de cortesía\\n(3-7 días post-servicio)')
        c.node('2', '2\\nAplica encuesta de\\nsatisfacción (NPS) y\\nregistra en Notion')
        c.node('3', '3\\n¿Cliente\\nSatisfecho?', shape='diamond', fillcolor='#FFFDE7')
        c.node('4', '4\\nAgradece preferencia y\\nprograma próximo recordatorio')
        c.node('5', '5\\nDetecta inconformidad y\\nclasifica: Atención o\\nGarantía Técnica')

    # --- CARRIL 2: CLIENTE ---
    with dot.subgraph(name='cluster_cliente') as c:
        c.attr(label='Cliente', style='dotted', fontname='Arial Bold')
        c.node('6', '6\\nReporta falla o duda sobre\\nel servicio ejecutado\\n(Reclamación)')

    # --- CARRIL 3: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_jefe') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('7', '7\\nRealiza inspección física;\\n¿Aplica Garantía?\\n(Pieza o Mano de Obra)', shape='diamond', fillcolor='#FFFDE7')
        c.node('8', '8\\nEjecuta reparación a costo\\ncero y actualiza historial\\nde garantías en Notion')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Satisfacción
    dot.edge('3', '4', label=' SÍ')
    dot.edge('3', '5', label=' NO')
    
    dot.edge('5', '6')
    dot.edge('6', '7')
    
    # Decisión: Aplicación de Garantía
    dot.edge('7', '8', label=' SÍ')
    dot.edge('7', 'FIN_RECH', label=' NO', style='dashed')
    dot.node('FIN_RECH', 'FIN (Explicar y Cotizar)', shape='oval', fillcolor='#FFEBEE')
    
    dot.edge('8', '1', style='dashed', label=' Re-evaluar')
    dot.edge('4', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Atención al Cliente</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 17/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A17: Postventa / garantías generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_postventa()