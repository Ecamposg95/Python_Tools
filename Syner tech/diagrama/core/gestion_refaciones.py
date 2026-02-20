import os
from graphviz import Digraph

# Configuración de ruta para Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

def generar_dpo_gestion_refacciones():
    dot = Digraph('DPO_REFACCIONES_BJX', filename='DPO_CORE_A9_REFACCIONES_BJX', format='svg')
    
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
            <TD><B>Core de Servicio | A9. Gestión de Refacciones</B></TD>
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
        c.node('1', '1\\nGenera requisición de\\nrefacciones basada en\\ndiagnóstico aprobado')
        c.node('8', '8\\nRecibe refacción y firma\\nresguardo de salida\\nde almacén')

    # --- CARRIL 2: ALMACÉN ---
    with dot.subgraph(name='cluster_almacen') as c:
        c.attr(label='Almacén', style='dotted', fontname='Arial Bold')
        c.node('2', '2\\nVerifica disponibilidad\\ny ubicación en anaquel')
        c.node('3', '3\\n¿Existe en\\nStock?', shape='diamond', fillcolor='#FFFDE7')
        c.node('4', '4\\nSurtir refacción y\\ndescontar de inventario\\nen sistema')
        c.node('6', '6\\nRecibe refacción de\\nproveedor y valida\\nintegridad y aplicación')
        c.node('7', '7\\nRegistra ingreso y\\nasigna folio a la\\norden en Notion')

    # --- CARRIL 3: COMPRAS / PROVEEDORES ---
    with dot.subgraph(name='cluster_compras') as c:
        c.attr(label='Compras / Proveedores', style='dotted', fontname='Arial Bold')
        c.node('5', '5\\nGenera pedido a proveedor\\ny gestiona logística\\nde entrega urgente')

    # --- FLUJO LÓGICO ---
    dot.edge('ST', '1')
    dot.edge('1', '2')
    dot.edge('2', '3')
    
    # Decisión: Existencia en Stock [cite: 3, 20]
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
            <TD>Revisó:</TD><TD WIDTH="120">Encargado de Almacén</TD>
            <TD>Autorizó:</TD><TD WIDTH="120">Carlos (CEO)</TD>
            <TD>Fecha: 07-02-2026</TD>
            <TD>Hoja: 09/18</TD>
          </TR>
        </TABLE>>''', labelloc='b')

    dot.render(cleanup=True)
    print("✅ DPO A9: Gestión de Refacciones generado exitosamente.")

if __name__ == "__main__":
    generar_dpo_gestion_refacciones()