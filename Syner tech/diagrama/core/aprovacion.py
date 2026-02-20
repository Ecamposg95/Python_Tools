import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_aprobacion_cliente():
    dot = Digraph('DPO_APROBACION_BJX', filename='DPO_CORE_A7_APROBACION_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales / Flujo Horizontal)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO_RRHH) [cite: 7-9]
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A7. Aprobación del Cliente</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos (Simbología Estándar [cite: 19, 27, 33])
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nEnvía cotización y enlace\\nde evidencias (Notion)\\nvía WhatsApp/Correo')
        c.node('2', '2\\nRealiza llamada de\\nseguimiento y explica\\nhallazgos técnicos')
        c.node('5', '5\\n¿Aprobación\\nParcial?', shape='diamond', fillcolor='#FFFDE7')
        c.node('6', '6\\nRealiza ajustes a la\\ncotización y solicita\\nnueva validación')
        c.node('8', '8\\nActualiza estatus de\\norden a "Aprobado"\\nen Notion y Sistema')

    # --- CARRIL 2: CLIENTE ---
    with dot.subgraph(name='cluster_cliente') as c:
        c.attr(label='Cliente', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\nRevisa presupuesto y\\nvalida evidencias\\nfotográficas/video')
        c.node('4', '4\\n¿Autoriza el\\nservicio?', shape='diamond', fillcolor='#FFFDE7')
        c.node('7', '7\\nFirma autorización\\n(Digital o Física en\\nrecepción)')

    # --- CARRIL 3: JEFE DE TALLER ---
    with dot.subgraph(name='cluster_taller') as c:
        c.attr(label='Jefe de Taller', style='dotted', fontname='Arial Bold')
        c.node('9', '9\\nRecibe notificación de\\naprobación y libera\\norden para ejecución')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    
    # Decisión: Autorización Total
    dot.edge('4', '7', label=' SÍ')
    dot.edge('4', '5', label=' NO')
    
    # Decisión: ¿Parcial?
    dot.edge('5', '6', label=' SÍ')
    dot.edge('5', 'FIN_RECH', label=' NO', style='dashed')
    dot.node('FIN_RECH', 'FIN (Cerrar sin Venta)', shape='oval', fillcolor='#FFEBEE')
    
    dot.edge('6', '4')
    dot.edge('7', '8')
    dot.edge('8', '9')
    dot.edge('9', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control de Calidad y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Gerencia Comercial</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 07/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A7: Aprobación del Cliente generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_aprobacion_cliente()