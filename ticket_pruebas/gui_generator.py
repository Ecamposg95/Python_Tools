import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Importamos la lógica de generación
from ticket_generator import build_ticket_text, print_win32

class TicketGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Tickets - Comercializadora Rmazh")
        self.root.geometry("1100x800")
        
        # Color palette
        self.bg_color = "#f0f2f5"
        self.accent_color = "#1a73e8"
        self.root.configure(bg=self.bg_color)

        self.template_path = "ticket_template.json"
        self.data = self.load_initial_data()

        self.setup_ui()
        self.refresh_printers()

    def load_initial_data(self):
        if os.path.exists(self.template_path):
            try:
                with open(self.template_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {
            "paper": {"char_width": 42},
            "header": {"line1": "MI NEGOCIO", "line2": "", "separator_char": "-"},
            "store": {"sucursal": "Centro", "direccion": "Calle 123", "telefono": "555-1234", "visita": "web.com"},
            "sale": {"venta": "001", "atendio": "Admin"},
            "items": [],
            "totals": {"efectivo": 0, "cambio": 0, "total_productos": 0}
        }

    def setup_ui(self):
        # Header App
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="SISTEMA DE TICKETS - RMAZH", fg="white", bg=self.accent_color, font=("Helvetica", 26, "bold")).pack(pady=15)

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left side: Form
        form_frame = tk.LabelFrame(main_frame, text=" Configuración del Ticket ", bg=self.bg_color, padx=10, pady=10)
        form_frame.pack(side="left", fill="both", expand=True)

        # Store section
        row = 0
        tk.Label(form_frame, text="Título 1:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_h1 = tk.Entry(form_frame, width=40)
        self.ent_h1.insert(0, self.data.get("header", {}).get("line1", ""))
        self.ent_h1.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="Sucursal:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_suc = tk.Entry(form_frame, width=40)
        self.ent_suc.insert(0, self.data.get("store", {}).get("sucursal", ""))
        self.ent_suc.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="Dirección:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_dir = tk.Entry(form_frame, width=40)
        self.ent_dir.insert(0, self.data.get("store", {}).get("direccion", ""))
        self.ent_dir.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="Teléfono:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_tel = tk.Entry(form_frame, width=40)
        self.ent_tel.insert(0, self.data.get("store", {}).get("telefono", ""))
        self.ent_tel.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="Web/Visita:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_vis = tk.Entry(form_frame, width=40)
        self.ent_vis.insert(0, self.data.get("store", {}).get("visita", ""))
        self.ent_vis.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="No. Venta:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_venta = tk.Entry(form_frame, width=40)
        self.ent_venta.insert(0, self.data.get("sale", {}).get("venta", ""))
        self.ent_venta.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        tk.Label(form_frame, text="Atendió:", bg=self.bg_color).grid(row=row, column=0, sticky="w")
        self.ent_atendio = tk.Entry(form_frame, width=40)
        self.ent_atendio.insert(0, self.data.get("sale", {}).get("atendio", ""))
        self.ent_atendio.grid(row=row, column=1, pady=2, padx=5, sticky="ew")
        row += 1

        # Items section
        items_frame = tk.LabelFrame(form_frame, text=" Partidas ", bg=self.bg_color, padx=5, pady=5)
        items_frame.grid(row=row, column=0, columnspan=2, sticky="nsew", pady=10)
        form_frame.grid_rowconfigure(row, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        row += 1

        self.tree = ttk.Treeview(items_frame, columns=("desc", "price", "qty", "total"), show="headings", height=10)
        self.tree.heading("desc", text="Descripción")
        self.tree.heading("price", text="Precio")
        self.tree.heading("qty", text="Cant.")
        self.tree.heading("total", text="Total")
        self.tree.column("desc", width=200)
        self.tree.column("price", width=80)
        self.tree.column("qty", width=60)
        self.tree.column("total", width=80)
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(items_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Add item controls
        add_frame = tk.Frame(form_frame, bg=self.bg_color)
        add_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
        row += 1

        tk.Label(add_frame, text="Desc:", bg=self.bg_color).pack(side="left")
        self.ent_item_desc = tk.Entry(add_frame, width=15)
        self.ent_item_desc.pack(side="left", padx=5)

        tk.Label(add_frame, text="Precio:", bg=self.bg_color).pack(side="left")
        self.ent_item_price = tk.Entry(add_frame, width=8)
        self.ent_item_price.pack(side="left", padx=5)

        tk.Label(add_frame, text="Cant:", bg=self.bg_color).pack(side="left")
        self.ent_item_qty = tk.Entry(add_frame, width=5)
        self.ent_item_qty.pack(side="left", padx=5)

        btn_add = tk.Button(add_frame, text="Añadir Item", command=self.add_item, bg="#4caf50", fg="white", relief="flat", padx=10)
        btn_add.pack(side="left", padx=5)

        btn_del = tk.Button(add_frame, text="Quitar Seleccionado", command=self.remove_item, bg="#f44336", fg="white", relief="flat", padx=10)
        btn_del.pack(side="left", padx=5)

        # Right side: Preview & Print
        right_frame = tk.Frame(main_frame, bg=self.bg_color, width=350)
        right_frame.pack(side="right", fill="both", expand=False, padx=(20, 0))

        tk.Label(right_frame, text="Vista Previa", bg=self.bg_color, font=("Arial", 10, "bold")).pack()
        self.txt_preview = tk.Text(right_frame, width=48, height=35, font=("Courier", 10))
        self.txt_preview.pack(pady=5)

        # Printer selection
        tk.Label(right_frame, text="Seleccionar Impresora:", bg=self.bg_color).pack(anchor="w")
        self.combo_printers = ttk.Combobox(right_frame, state="readonly", width=45)
        self.combo_printers.pack(pady=5)

        btn_refresh = tk.Button(right_frame, text="🔄 Actualizar Impresoras", command=self.refresh_printers)
        btn_refresh.pack(pady=2)

        btn_preview = tk.Button(right_frame, text="👁️ Actualizar Vista Previa", command=self.update_preview, bg="#2196f3", fg="white", height=2)
        btn_preview.pack(fill="x", pady=10)

        btn_print = tk.Button(right_frame, text="🖨️ IMPRIMIR TICKET", command=self.do_print, bg="#f44336", fg="white", font=("Arial", 12, "bold"), height=2)
        btn_print.pack(fill="x", pady=5)

        # Load initial items into tree from JSON
        for it in self.data.get("items", []):
            self.tree.insert("", "end", values=(it["desc"], it["price"], it["qty"], float(it["price"]) * float(it["qty"])))

        self.update_preview()

    def refresh_printers(self):
        try:
            import win32print
            printers = [p[2] for p in win32print.EnumPrinters(2)]
            self.combo_printers['values'] = printers
            if printers:
                idx = 0
                for i, p in enumerate(printers):
                    if any(x in p.upper() for x in ["POS", "TICKET", "RECEIPT", "58", "80"]):
                        idx = i
                        break
                self.combo_printers.current(idx)
        except:
            self.combo_printers['values'] = ["Error al obtener impresoras"]

    def add_item(self):
        d = self.ent_item_desc.get()
        p = self.ent_item_price.get()
        q = self.ent_item_qty.get()
        if not d or not p or not q:
            return
        try:
            total = float(p) * float(q)
            self.tree.insert("", "end", values=(d, p, q, total))
            self.ent_item_desc.delete(0, tk.END)
            self.ent_item_price.delete(0, tk.END)
            self.ent_item_qty.delete(0, tk.END)
            self.update_preview()
        except ValueError:
            messagebox.showerror("Error", "Precio y Cantidad deben ser números")

    def remove_item(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                self.tree.delete(item)
            self.update_preview()

    def collect_data(self):
        items = []
        total_p = 0
        total_val = 0
        for child in self.tree.get_children():
            v = self.tree.item(child)["values"]
            items.append({"desc": v[0], "price": float(v[1]), "qty": float(v[2])})
            total_p += float(v[2])
            total_val += float(v[1]) * float(v[2])

        self.data["header"]["line1"] = self.ent_h1.get()
        self.data["store"]["sucursal"] = self.ent_suc.get()
        self.data["store"]["direccion"] = self.ent_dir.get()
        self.data["store"]["telefono"] = self.ent_tel.get()
        self.data["store"]["visita"] = self.ent_vis.get()
        self.data["sale"]["venta"] = self.ent_venta.get()
        self.data["sale"]["atendio"] = self.ent_atendio.get()
        self.data["sale"]["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.data["items"] = items
        self.data["totals"]["total_productos"] = int(total_p)
        self.data["totals"]["efectivo"] = total_val
        self.data["totals"]["cambio"] = 0
        
        return self.data

    def update_preview(self):
        data = self.collect_data()
        text = build_ticket_text(data)
        self.txt_preview.delete("1.0", tk.END)
        self.txt_preview.insert("1.0", text)

    def do_print(self):
        printer = self.combo_printers.get()
        if not printer:
            messagebox.showwarning("Aviso", "Selecciona una impresora")
            return
        
        data = self.collect_data()
        # Generar texto con comandos térmicos (título grande) para la impresora
        text_to_print = build_ticket_text(data, is_thermal=True)
        
        try:
            print_win32(text_to_print, printer)
            messagebox.showinfo("Éxito", f"Ticket enviado a {printer}")
        except Exception as e:
            messagebox.showerror("Error de Impresión", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketGui(root)
    root.mainloop()
