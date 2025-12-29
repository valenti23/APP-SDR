import os

SOPORTES_CLINICOS = ("HAM", "HAU", "EPI")

IGNORAR = (
    "RIPS_",
    "RIPS_CUV_",
    "AD"
)

def generar_pendientes(ruta_base, eps):
    eps = eps.upper().replace(" ", "_")
    pendientes = []

    for carpeta in os.listdir(ruta_base):
        if not carpeta.upper().startswith("FC"):
            continue

        ruta_fc = os.path.join(ruta_base, carpeta)
        if not os.path.isdir(ruta_fc):
            continue

        archivos = os.listdir(ruta_fc)

        # ---- FILTRAR ARCHIVOS VALIDOS ----
        validos = [
            a.upper() for a in archivos
            if not a.upper().startswith(IGNORAR)
        ]

        fev = [a for a in validos if a.startswith("FEV")]
        pde = [a for a in validos if a.startswith("PDE")]
        pdx_hev = [a for a in validos if a.startswith(("PDX", "HEV"))]
        clinicos = [a for a in validos if a.startswith(SOPORTES_CLINICOS)]
        ldp = [a for a in validos if a.startswith("LDP")]

        estado = None

        # ===============================
        # REGLAS GENERALES
        # ===============================
        if not pdx_hev:
            if clinicos:
                estado = "FACTURA POR COMPLETAR"
            else:
                estado = "FACTURA SIN SOPORTE"

        # ---- MAS DE 1 PDE ----
        if len(pde) > 1:
            estado = "FACTURA POR COMPLETAR"

        # ---- FOMAG: LDP obligatorio ----
        if eps == "FOMAG" and not ldp:
            estado = "FACTURA POR COMPLETAR"

        if estado:
            pendientes.append(f"{carpeta} -> {estado}")

    salida = os.path.join(ruta_base, f"PENDIENTES_{eps}.txt")

    with open(salida, "w", encoding="utf-8") as f:
        if pendientes:
            f.write("\n".join(pendientes))
        else:
            f.write("✔ No hay facturas pendientes")

    print("📄 Pendientes generados:", salida)
