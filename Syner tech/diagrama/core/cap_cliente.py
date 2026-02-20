import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_captacion_cliente():
    dot = Digraph('DPO_CAPTACION_BJX', filename='DPO_CORE_A1_CAPTACION_BJX', format='svg')
    
    # Atributos Globales: Estilo BJX Motors (Lane Vertical / Estilo PDF RRHH)
    dot.attr(rankdir='TB', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.5', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A1. Captación de Cliente</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.0', fontname='Arial', fontsize='10', height='0.7', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.0', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL: MARKETING / VENTAS ---
    with dot.subgraph(name='cluster_ventas') as c:
        c.attr(label='Marketing / Ventas (Omnicanal)', style='dotted', fontname='Arial Bold')
        
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nIdentifica Lead por\\nWhatsApp, Redes o\\nLlamada Directa')
        c.node('2', '2\\n¿Cliente es\\nNuevo?', shape='diamond', fillcolor='#FFFDE7')
        c.node('3', '3\\nSolicita datos de\\ncontacto y del\\nvehículo (Placas/VIN)')
        c.node('4', '4\\nBusca registro en\\nbase de datos / CRM')
        c.node('5', '5\\nRealiza Pre-diagnóstico\\nremoto sobre la\\nnecesidad del servicio')
        c.node('6', '6\\n¿Requiere cita\\npresencial?', shape='diamond', fillcolor='#FFFDE7')
        c.node('7', '7\\nAgendar cita en\\ncalendario operativo')
        c.node('8', '8\\nEnvía recordatorio\\ny ubicación vía\\nWhatsApp')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    
    # Decisión: ¿Cliente Nuevo?
    dot.edge('2', '3', label=' SÍ')
    dot.edge('2', '4', label=' NO')
    dot.edge('3', '5')
    dot.edge('4', '5')
    
    dot.edge('5', '6')
    
    # Decisión: ¿Requiere Cita?
    dot.edge('6', '7', label=' SÍ')
    dot.edge('6', '1', label=' NO / Seguimiento', style='dashed')
    
    dot.edge('7', '8')
    dot.edge('8', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control de Calidad)
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Dirección Operativa</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 01/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A1: Captación de Cliente generado.")

if __name__ == "__main__":
    generar_dpo_captacion_cliente()