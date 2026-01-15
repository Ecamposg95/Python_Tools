# ticket_generator.py
# Generador editable de tickets 80mm (por caracteres) -> TXT / PDF / ESC-POS
#
# Install:
#   pip install python-escpos reportlab
#
# Usage:
#   python ticket_generator.py --template ticket_template.json --mode text --out ticket.txt
#   python ticket_generator.py --template ticket_template.json --mode pdf  --out ticket.pdf
#   python ticket_generator.py --template ticket_template.json --mode escpos --printer network --host 192.168.1.50 --port 9100
#   python ticket_generator.py --template ticket_template.json --mode escpos --printer usb --vendor 0x04b8 --product 0x0e15
#
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
import sys
try:
    import win32print
except ImportError:
    win32print = None


MONEY_Q = Decimal("0.01")


def D(x: Any) -> Decimal:
    return Decimal(str(x))


def money(x: Decimal, space: bool = False) -> str:
    x = x.quantize(MONEY_Q, rounding=ROUND_HALF_UP)
    s = " " if space else ""
    return f"${s}{x:.2f}"


def center(text: str, width: int) -> str:
    text = (text or "").strip()
    if len(text) >= width:
        return text[:width]
    pad = (width - len(text)) // 2
    return " " * pad + text


def hr(width: int, ch: str = "-") -> str:
    return (ch or "-") * width


def wrap_text(text: str, width: int) -> List[str]:
    """Word-wrap simple."""
    text = (text or "").strip()
    if not text:
        return [""]
    words = text.split()
    lines: List[str] = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fmt_kv(left: str, right: str, width: int) -> str:
    left = (left or "").strip()
    right = (right or "").strip()
    if len(left) + len(right) + 1 > width:
        max_left = max(0, width - len(right) - 1)
        left = left[:max_left]
    spaces = width - len(left) - len(right)
    return left + (" " * spaces) + right


@dataclass
class Item:
    desc: str
    price: Decimal
    qty: Decimal

    @property
    def amount(self) -> Decimal:
        return (self.price * self.qty).quantize(MONEY_Q, rounding=ROUND_HALF_UP)


def build_ticket_text(tpl: Dict[str, Any], is_thermal: bool = False) -> str:
    paper = tpl.get("paper", {})
    width = int(paper.get("char_width", 48))
    title_centered = bool(paper.get("title_centered", True))

    ESC = "\x1b"
    GS = "\x1d"
    # Comandos de alineación
    ALIGN_LEFT = f"{ESC}a\x00"
    ALIGN_CENTER = f"{ESC}a\x01"
    ALIGN_RIGHT = f"{ESC}a\x02"
    # Comandos de tamaño
    BIG_ON = f"{GS}!\x11"
    BIG_OFF = f"{GS}!\x00"

    header = tpl.get("header", {})
    h1 = header.get("line1", "")
    h2 = header.get("line2", "")
    sep_ch = header.get("separator_char", "-")

    store = tpl.get("store", {})
    sale = tpl.get("sale", {})
    cols = tpl.get("columns", {})
    totals = tpl.get("totals", {})
    footer = tpl.get("footer", {})

    # Parse datetime
    dt_raw = sale.get("fecha_hora", "")
    try:
        dt = datetime.strptime(dt_raw, "%Y-%m-%d %H:%M:%S")
    except Exception:
        dt = None

    items_in = tpl.get("items", [])
    items: List[Item] = []
    for it in items_in:
        items.append(
            Item(
                desc=str(it.get("desc", "")),
                price=D(it.get("price", 0)),
                qty=D(it.get("qty", 0)),
            )
        )

    total_calc = sum((i.amount for i in items), Decimal("0.00")).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
    efectivo = D(totals.get("efectivo", 0)).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
    cambio = D(totals.get("cambio", 0)).quantize(MONEY_Q, rounding=ROUND_HALF_UP)
    total_productos = int(totals.get("total_productos", 0))

    out: List[str] = []

    # Header lines
    if h1:
        h1_str = str(h1).upper()
        if is_thermal:
            # Comando explícito de centrado para el título
            eff_width = width // 2
            if title_centered:
                out.append(ALIGN_CENTER)
                h1_str = center(h1_str, eff_width)
            else:
                out.append(ALIGN_LEFT)
            out.append(f"{BIG_ON}{h1_str}{BIG_OFF}")
        else:
            if title_centered:
                out.append(center(h1_str, width))
            else:
                out.append(h1_str[:width])
    
    if h2:
        h2_str = str(h2).upper()
        if is_thermal:
            out.append(ALIGN_CENTER if title_centered else ALIGN_LEFT)
        if title_centered:
            out.append(center(h2_str, width))
        else:
            out.append(h2_str[:width])

    # Reset a izquierda para el resto del ticket
    if is_thermal:
        out.append(ALIGN_LEFT)

    out.append(hr(width, sep_ch))

    # Store info
    suc = store.get("sucursal", "")
    dir_ = store.get("direccion", "")
    tel = store.get("telefono", "")
    vis = store.get("visita", "")

    # En tu ticket se ve centrado, lo dejamos centrado por defecto
    if suc:
        out.append(center(f"Sucursal: {suc}", width))
    if dir_:
        out.append(center(f"Dirección: {dir_}", width))
    if tel:
        out.append(center(f"Teléfono: {tel}", width))
    if vis:
        out.append(center(f"Visita: {vis}", width))

    out.append("")

    venta = sale.get("venta", "")
    atendio = sale.get("atendio", "")

    out.append(f"VENTA: #{venta}")
    if dt:
        out.append(f"FECHA Y HORA: {dt.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        out.append(f"FECHA Y HORA: {dt_raw}")
    out.append(f"ATENDIÓ: {atendio}")
    out.append("")

    # Column header
    if bool(cols.get("show_header", True)):
        out.append(fmt_kv(cols.get("desc_label", "DESC."), cols.get("right_label", "PRECIO. CANT. IMPORTE"), width))
        out.append(hr(width, sep_ch))

    # Items formatting
    sections = tpl.get("sections", [])
    if sections:
        for sec in sections:
            sec_title = str(sec.get("title", "")).upper()
            if sec_title:
                out.append(sec_title)
            
            idx_list = sec.get("items_idx", [])
            for idx in idx_list:
                if 0 <= idx < len(items):
                    i = items[idx]
                    out.append("")
                    for line in wrap_text(i.desc.upper(), width):
                        out.append(line)
                    op = f"{money(i.price, space=True)} X {i.qty:.2f} = {money(i.amount)}"
                    out.append(op.rjust(width))
    else:
        for i in items:
            # Description wrapped
            for line in wrap_text(i.desc.upper(), width):
                out.append(line[:width])

            op = f"{money(i.price)} X {i.qty:.2f} = {money(i.amount)}"
            if len(op) < width:
                op = " " * (width - len(op)) + op
            else:
                op = op[:width]
            out.append(op)

    out.append(hr(width, sep_ch))

    # Totals block (labels editables)
    final_total = total_calc
    if "total_override" in totals:
        final_total = D(totals["total_override"]).quantize(MONEY_Q, rounding=ROUND_HALF_UP)

    if is_thermal:
        # Alineación derecha real para los totales en impresoras térmicas
        out.append(ALIGN_RIGHT)
        out.append(f"{totals.get('total_label', 'TOTAL:')} {money(final_total)}")
        out.append(f"{totals.get('efectivo_label', 'EFECTIVO:')} {money(efectivo, space=True)}")
        out.append(f"{totals.get('cambio_label', 'CAMBIO:')} {money(cambio, space=True)}")
        out.append(f"{totals.get('total_productos_label', 'TOTAL DE PRODUCTOS:')} {total_productos}")
        out.append(ALIGN_LEFT)
    else:
        out.append(f"{totals.get('total_label', 'TOTAL:')} {money(final_total)}".rjust(width))
        out.append(f"{totals.get('efectivo_label', 'EFECTIVO:')} {money(efectivo, space=True)}".rjust(width))
        out.append(f"{totals.get('cambio_label', 'CAMBIO:')} {money(cambio, space=True)}".rjust(width))
        out.append(f"{totals.get('total_productos_label', 'TOTAL DE PRODUCTOS:')} {total_productos}".rjust(width))
    out.append("")

    # Footer lines
    footer_lines = footer.get("lines", [])
    for fl in footer_lines:
        fl = str(fl)
        if title_centered:
            out.append(center(fl, width))
        else:
            out.append(fl[:width])

    out.append("")
    return "\n".join(out)


def save_text(text: str, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)


def save_pdf(text: str, out_path: str, char_width: int) -> None:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import mm

    lines = text.splitlines()

    # 80mm ancho, alto dinámico; monoespaciado
    width_mm = 80
    line_h_mm = 4.0
    top_mm = 6
    bottom_mm = 6
    height_mm = top_mm + bottom_mm + line_h_mm * max(1, len(lines))

    c = canvas.Canvas(out_path, pagesize=(width_mm * mm, height_mm * mm))
    c.setFont("Courier", 9)

    x = 4 * mm
    y = (height_mm - top_mm) * mm
    for ln in lines:
        c.drawString(x, y, ln)
        y -= line_h_mm * mm

    c.showPage()
    c.save()


def print_escpos(text: str, printer_type: str, **kwargs) -> None:
    from escpos.printer import Network, Usb, Serial

    if printer_type == "network":
        p = Network(kwargs["host"], port=int(kwargs.get("port", 9100)), timeout=10)
    elif printer_type == "usb":
        vendor = int(str(kwargs["vendor"]), 16) if str(kwargs["vendor"]).lower().startswith("0x") else int(kwargs["vendor"])
        product = int(str(kwargs["product"]), 16) if str(kwargs["product"]).lower().startswith("0x") else int(kwargs["product"])
        p = Usb(vendor, product)
    elif printer_type == "serial":
        p = Serial(kwargs["port"], baudrate=int(kwargs.get("baudrate", 9600)), timeout=1)
    else:
        raise ValueError("printer_type debe ser: network | usb | serial")

    p.hw("INIT")
    try:
        # Puedes probar estilos con set():
        # p.set(align='center', bold=True, double_width=True, double_height=True)
        p.text(text)
        p.cut()
    finally:
        try:
            p.close()
        except Exception:
            pass


def print_win32(text: str, printer_name: str) -> None:
    if not win32print:
        print("Error: El módulo 'pywin32' no está instalado. Ejecuta: pip install pywin32")
        return

    # Comandos ESC/POS para corte
    GS = b'\x1d'
    CUT = GS + b'V\x42\x00'

    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            # Encode text
            raw_data = text.encode('cp437', errors='replace')
            # Append Cut command
            raw_data += b'\n' * 3 + CUT
            win32print.WritePrinter(hPrinter, raw_data)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True, help="Ruta al JSON editable del ticket")
    ap.add_argument("--mode", choices=["text", "pdf", "escpos", "win32"], required=True)
    ap.add_argument("--out", default="ticket.out", help="Salida para text/pdf")

    # ESC/POS config
    ap.add_argument("--printer", choices=["network", "usb", "serial"], help="Tipo impresora ESC/POS")
    ap.add_argument("--host", help="IP impresora (network)")
    ap.add_argument("--port", type=int, default=9100, help="Puerto (network)")
    ap.add_argument("--vendor", help="VendorID USB (hex) ej 0x04b8")
    ap.add_argument("--product", help="ProductID USB (hex) ej 0x0e15")
    ap.add_argument("--serial_port", help="Puerto serial (serial) ej COM3 o /dev/ttyUSB0")
    ap.add_argument("--baudrate", type=int, default=9600)
    ap.add_argument("--name", help="Nombre de la impresora (win32)")

    args = ap.parse_args()

    with open(args.template, "r", encoding="utf-8") as f:
        tpl = json.load(f)

    text = build_ticket_text(tpl)
    char_width = int(tpl.get("paper", {}).get("char_width", 48))

    if args.mode == "text":
        out = args.out if args.out.lower().endswith(".txt") else args.out + ".txt"
        save_text(text, out)
        print(f"OK: TXT -> {out}")

    elif args.mode == "pdf":
        out = args.out if args.out.lower().endswith(".pdf") else args.out + ".pdf"
        save_pdf(text, out, char_width)
        print(f"OK: PDF -> {out}")

    elif args.mode == "escpos":
        if not args.printer:
            raise SystemExit("Falta --printer (network|usb|serial)")

        if args.printer == "network":
            if not args.host:
                raise SystemExit("Falta --host para printer network")
            print_escpos(text, "network", host=args.host, port=args.port)

        elif args.printer == "usb":
            if not args.vendor or not args.product:
                raise SystemExit("Falta --vendor y --product para printer usb")
            print_escpos(text, "usb", vendor=args.vendor, product=args.product)

        elif args.printer == "serial":
            if not args.serial_port:
                raise SystemExit("Falta --serial_port para printer serial")
            print_escpos(text, "serial", port=args.serial_port, baudrate=args.baudrate)

        print("OK: Impresión ESC/POS enviada")

    elif args.mode == "win32":
        if not args.name:
            raise SystemExit("Falta --name (Nombre de la impresora en Windows)")
        # Forzamos thermal=True para win32 ya que suele ser ticketera
        text_thermal = build_ticket_text(tpl, is_thermal=True)
        print_win32(text_thermal, args.name)
        print(f"OK: Ticket enviado a {args.name}")

    else:
        raise SystemExit("Modo no soportado")


if __name__ == "__main__":
    main()
