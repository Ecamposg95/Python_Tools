import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_registro_cliente():
    dot = Digraph('DPO_REGISTRO_BJX', filename='DPO_CORE_A3_REGISTRO_BJX', format='svg')
    
    # Atributos Globales: Estilo de Contraloría BJX (Carriles Verticales)
    dot.attr(rankdir='LR', fontname='Arial', fontsize='12', compound='true', 
             nodesep='0.6', ranksep='0.8', bgcolor='#ffffff', splines='ortho')
    
    # Encabezado Institucional (Basado en DPO de RRHH)
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10">
          <TR>
            <TD WIDTH="100" ROWSPAN="2"><B>BJX MOTORS</B></TD>
            <TD WIDTH="600" BGCOLOR="#F2F2F2"><B>Diagrama de Proceso Operativo (DPO)</B></TD>
          </TR>
          <TR>
            <TD><B>Core de Servicio | A3. Registro del Cliente</B></TD>
          </TR>
        </TABLE>>''', labelloc='t')

    # Estilos de Nodos
    dot.attr('node', shape='rect', style='filled', fillcolor='#ffffff', color='#000000', 
             penwidth='1.0', fontname='Arial', fontsize='10', height='0.8', width='2.0')
    dot.attr('edge', color='#000000', penwidth='1.0', arrowhead='normal', arrowsize='0.7')

    # --- CARRIL 1: ASESORA DE SERVICIOS ---
    with dot.subgraph(name='cluster_asesora') as c:
        c.attr(label='Asesora de Servicios', style='dotted', fontname='Arial Bold')
        c.node('ST', 'INICIO', shape='oval', fillcolor='#E8F5E9')
        c.node('1', '1\\nSolicita identificación\\ny tarjeta de circulación\\n(Digitalización)')
        c.node('3', '3\\nActualiza datos de\\ncontacto, correo y\\ndirección actual')
        c.node('4', '4\\nCaptura de nuevo\\ncliente y vinculación\\nde VIN/Placas')
        c.node('5', '5\\nRegistro de datos\\nfiscales (CSF actualizada)\\npara facturación')
        c.node('6', '6\\nValidación de integridad\\nde datos y cierre de\\nperfil en Notion')

    # --- CARRIL 2: ADMINISTRACIÓN / SISTEMAS ---
    with dot.subgraph(name='cluster_sistemas') as c:
        c.attr(label='Administración / Sistemas', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\n¿Existe registro\\nprevio en CRM /\\nBase de Datos?', shape='diamond', fillcolor='#FFFDE7')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    
    # Decisión: ¿Existe en CRM?
    dot.edge('2', '3', label=' SÍ')
    dot.edge('2', '4', label=' NO')
    
    dot.edge('3', '5')
    dot.edge('4', '5')
    dot.edge('5', '6')
    
    dot.edge('6', 'FIN', shape='oval', fillcolor='#FFEBEE')
    dot.node('FIN', 'FIN')

    # PIE DE PÁGINA (Control de Calidad)
    dot.attr(label='''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
          <TR>
            <TD>Elaboró:</TD><TD WIDTH="120">Ing. Emmanuel G.</TD>
            <TD>Revisó:</TD><TD WIDTH="120">Administración</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 03/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A3: Registro del Cliente generado.")

if __name__ == "__main__":
    generar_dpo_registro_cliente()