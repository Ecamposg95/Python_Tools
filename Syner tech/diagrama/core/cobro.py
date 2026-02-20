import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_cobro():
    dot = Digraph('DPO_COBRO_BJX', filename='DPO_CORE_A15_COBRO_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A15. Cobro</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.5', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.2', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: CLIENTE ---
    with dot.subgraph(name='cluster_cliente') as c:
        c.attr(label='Cliente', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nPresenta comprobante de\\npago o realiza pago\\nen ventanilla / terminal')

    # --- CARRIL 2: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\nRecibe comprobante y\\nsolicita validación a\\nAdministración')
        c.node('7', '7\\nEntrega ticket final y\\nlibera llaves y pase\\nde salida')

    # --- CARRIL 3: ADMINISTRACIÓN / CAJA ---
    with dot.subgraph(name='cluster_admin') as c:
        c.attr(label='Administración / Caja', style='dotted', fontname='Arial Bold')
        c.node('3', '3\\n¿Método de\\npago es\\nTransferencia?', shape='diamond', fillcolor='#FFFDE7')
        c.node('4', '4\\nValida ingreso en portal\\nbancario (Cero capturas\\nde pantalla)')
        c.node('5', '5\\nProcesa pago en terminal\\no recibe efectivo y\\nvalida autenticidad')
        c.node('6', '6\\nRegistra ingreso en el\\nsistema ERP y marca\\norden como "Pagada"')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Método de Pago
    dot.edge('3', '4', label=' SÍ')
    dot.edge('3', '5', label=' NO')
    
    dot.edge('4', '6')
    dot.edge('5', '6')
    dot.edge('6', '7')
    
    dot.edge('7', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control y Firmas [cite: 34-41])
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Tesorería</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 15/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A15: Cobro generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_cobro()