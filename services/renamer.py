import os
import shutil
from pypdf import PdfWriter


def rename_files(ruta_base, eps, nit=None):
    """
    RENOMBRADO OFICIAL RNF
    """

    if not os.path.isdir(ruta_base):
        raise Exception("La ruta base no existe")

    eps = eps.upper().replace(" ", "_")

    # ==============================
    # VALIDACIÓN LDP SOLO FOMAG
    # ==============================
    if eps == "FOMAG":
        if not nit:
            raise Exception("FOMAG requiere NIT")

        ldp_origen = os.path.join(ruta_base, "LDP.pdf")
        if not os.path.exists(ldp_origen):
            raise Exception("FOMAG requiere obligatoriamente LDP.pdf en la ruta base")

    # ==============================
    # RECORRER CARPETAS FC*
    # ==============================
    for nombre_carpeta in os.listdir(ruta_base):
        if not nombre_carpeta.upper().startswith("FC"):
            continue

        ruta_carpeta = os.path.join(ruta_base, nombre_carpeta)
        if not os.path.isdir(ruta_carpeta):
            continue

        # ------------------------------
        # FACTURA ELECTRÓNICA
        # ------------------------------
        factura_original = os.path.join(
            ruta_carpeta,
            f"{nombre_carpeta}.pdf"
        )

        if os.path.exists(factura_original):

            if eps == "SANITAS":
                nuevo_nombre = f"FEV_{nombre_carpeta}.pdf"

            elif eps in ("FOMAG", "SALUD_TOTAL", "NUEVA_EPS"):
                nuevo_nombre = f"FEV_{nit}_{nombre_carpeta}.pdf"

            elif eps == "MUTUAL_SER":
                nuevo_nombre = f"FVS_{nit}_{nombre_carpeta}.pdf"

            else:
                nuevo_nombre = None

            if nuevo_nombre:
                destino = os.path.join(ruta_carpeta, nuevo_nombre)
                if not os.path.exists(destino):
                    os.rename(factura_original, destino)

        # ==================================================
        # SOPORTES
        # ==================================================

        # ---------- MUTUAL SER ----------
        if eps == "MUTUAL_SER":

            adc_files = sorted([
                f for f in os.listdir(ruta_carpeta)
                if f.upper().startswith("ADC_") and f.lower().endswith(".pdf")
            ])

            if adc_files:
                writer = PdfWriter()

                for adc in adc_files:
                    writer.append(os.path.join(ruta_carpeta, adc))

                opf_final = os.path.join(
                    ruta_carpeta,
                    f"OPF_{nit}_{nombre_carpeta}.pdf"
                )

                with open(opf_final, "wb") as f:
                    writer.write(f)

                # eliminar ADC originales
                for adc in adc_files:
                    os.remove(os.path.join(ruta_carpeta, adc))

        # ---------- DEMÁS EPS ----------
        else:
            for archivo in os.listdir(ruta_carpeta):
                if archivo.upper().startswith("ADC_") and archivo.lower().endswith(".pdf"):
                    origen = os.path.join(ruta_carpeta, archivo)
                    destino = os.path.join(ruta_carpeta, "PDE_" + archivo[4:])

                    if not os.path.exists(destino):
                        os.rename(origen, destino)

        # ------------------------------
        # LDP SOLO FOMAG
        # ------------------------------
        if eps == "FOMAG":
            destino_ldp = os.path.join(
                ruta_carpeta,
                f"LDP_{nit}_{nombre_carpeta}.pdf"
            )

            if not os.path.exists(destino_ldp):
                shutil.copy(ldp_origen, destino_ldp)
