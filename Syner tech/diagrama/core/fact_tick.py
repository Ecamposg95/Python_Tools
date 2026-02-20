import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_facturacion():
    dot = Digraph('DPO_FACTURACION_BJX', filename='DPO_CORE_A14_FACTURACION_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A14. Facturación / ticket</B></TD>
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
        c.node('1', '1\\nRecibe notificación de\\ncierre técnico y valida\\nmontos finales')
        c.node('2', '2\\nConfirma con el cliente\\nforma de pago y datos\\nfiscales (RFC)')
        c.node('3', '3\\nGenera pre-factura o\\nticket de venta en\\nel sistema administrativo')
        c.node('8', '8\\nEnvía archivo PDF/XML\\nal cliente y registra\\nfolio en Notion')

    # --- CARRIL 2: ADMINISTRACIÓN / CAJA ---
    with dot.subgraph(name='cluster_admin') as c:
        c.attr(label='Administración / Caja', style='dotted', fontname='Arial Bold')
        c.node('4', '4\\nVerifica ingreso de\\npago (Transferencia, Card,\\nEfectivo)')
        c.node('5', '5\\n¿Requiere\\nTimbrado Fiscal?', shape='diamond', fillcolor='#FFFDE7')
        c.node('6', '6\\nEjecuta proceso de\\ntimbrado CFDI ante\\nel SAT')
        c.node('7', '7\\nGenera comprobante de\\npago y libera orden\\npara entrega')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    dot.edge('3', '4')
    dot.edge('4', '5')
    
    # Decisión: Timbrado
    dot.edge('5', '6', label=' SÍ')
    dot.edge('5', '7', label=' NO')
    
    dot.edge('6', '7')
    dot.edge('7', '8')
    
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Administración</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 14/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A14: Facturación / ticket generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_facturacion()