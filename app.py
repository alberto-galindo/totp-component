import io
import base64
import pyotp
import qrcode
from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = "totp-demo-secret-key-change-in-production"

SERVICE_NAME = "TareaSeguridad"
ISSUER      = "MasterCiberseguridad"


def _generate_qr_b64(uri: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=8, border=4,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


@app.route("/")
def index():
    if "totp_secret" not in session:
        session["totp_secret"] = pyotp.random_base32()
    secret = session["totp_secret"]
    totp   = pyotp.TOTP(secret)
    uri    = totp.provisioning_uri(name=SERVICE_NAME, issuer_name=ISSUER)
    qr_b64 = _generate_qr_b64(uri)
    return render_template("index.html", qr_b64=qr_b64, secret=secret,
                           service=SERVICE_NAME, issuer=ISSUER)


@app.route("/validate", methods=["POST"])
def validate():
    code   = request.form.get("code", "").strip()
    secret = session.get("totp_secret", "")
    if not secret:
        return jsonify({"valid": False, "message": "Sesión no inicializada."})
    totp  = pyotp.TOTP(secret)
    valid = totp.verify(code, valid_window=1)   # ±30 s de tolerancia
    msg   = "✅ Código CORRECTO. Autenticación exitosa." if valid             else "❌ Código INCORRECTO o expirado."
    return jsonify({"valid": valid, "message": msg})


@app.route("/regenerate", methods=["POST"])
def regenerate():
    session["totp_secret"] = pyotp.random_base32()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
