from flask import Flask, render_template, request
from services.renamer import rename_files
from services.pendientes import generar_pendientes

app = Flask(__name__)

# NIT fijo de la clínica
NIT_CLINICA = "830510991"

# Logos por EPS
LOGOS = {
    "SANITAS": "sani1.png",
    "SALUD_TOTAL": "saludtotal.png",
    "FOMAG": "fomag.png",
    "MUTUAL_SER": "mutualser.png",
    "NUEVA_EPS": "nuevaeps.png"
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/eps/<eps_name>", methods=["GET", "POST"])
def eps_page(eps_name):
    eps_normalizada = eps_name.upper().replace(" ", "_")
    logo = LOGOS.get(eps_normalizada)

    if request.method == "POST":
        folder_path = request.form["folder"]

        # 👉 SOLO PASAMOS NIT A LAS EPS QUE LO REQUIEREN
        nit = NIT_CLINICA if eps_normalizada in (
            "FOMAG",
            "SALUD_TOTAL",
            "NUEVA_EPS",
            "MUTUAL_SER"
        ) else None

        rename_files(
            ruta_base=folder_path,
            eps=eps_normalizada,
            nit=nit
        )

        generar_pendientes(folder_path, eps_normalizada)

        return render_template(
            "eps.html",
            eps=eps_name,
            logo=logo,
            success=True
        )

    return render_template(
        "eps.html",
        eps=eps_name,
        logo=logo
    )


if __name__ == "__main__":
    app.run(debug=True)
