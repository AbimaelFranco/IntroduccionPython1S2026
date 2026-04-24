from flask import Flask, request, render_template_string, redirect
import os
import csv
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "examples/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# HTML (frontend)
# =========================

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Registro Inteligente</title>

<style>
* {
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family: 'Segoe UI', sans-serif;
}

body {
    height:100vh;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    overflow:hidden;
    color:white;
}

/* =========================
   PARTÍCULAS
========================= */
canvas {
    position:fixed;
    top:0;
    left:0;
    z-index:-1;
}

/* =========================
   CONTENEDOR
========================= */
.container {
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    padding:20px;
}

.card {
    width:100%;
    max-width:420px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius:20px;
    padding:25px;
    box-shadow:0 10px 40px rgba(0,0,0,0.5);
    animation:fadeIn 0.8s ease;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(20px);}
    to {opacity:1; transform:translateY(0);}
}

/* =========================
   INPUTS
========================= */
.input-group {
    margin-bottom:15px;
}

input, textarea {
    width:100%;
    padding:12px;
    border:none;
    border-radius:10px;
    background:rgba(255,255,255,0.08);
    color:white;
    outline:none;
    transition:0.3s;
}

input:focus, textarea:focus {
    background:rgba(255,255,255,0.15);
    box-shadow:0 0 10px #22c55e;
}

/* =========================
   BOTÓN
========================= */
button {
    width:100%;
    padding:12px;
    border:none;
    border-radius:12px;
    background:linear-gradient(135deg, #22c55e, #4ade80);
    color:white;
    font-size:16px;
    cursor:pointer;
    transition:0.3s;
}

button:hover {
    transform:scale(1.03);
}

/* =========================
   CHECKBOX
========================= */
.checkbox {
    display:flex;
    align-items:center;
    gap:10px;
    font-size:13px;
    margin:10px 0;
}

/* =========================
   PREVIEW IMAGEN
========================= */
.preview {
    margin-top:10px;
    text-align:center;
}

.preview img {
    max-width:100px;
    border-radius:10px;
}

/* =========================
   TOAST
========================= */
.toast {
    position:fixed;
    bottom:20px;
    right:20px;
    background:#22c55e;
    padding:15px 20px;
    border-radius:10px;
    opacity:0;
    transform:translateY(20px);
    transition:0.5s;
}

.toast.show {
    opacity:1;
    transform:translateY(0);
}
</style>
</head>

<body>

<canvas id="bg"></canvas>

<div class="container">
<div class="card">
<h2 style="text-align:center; margin-bottom:15px;">Registro 🚀</h2>

<form action="/submit" method="POST" enctype="multipart/form-data">
    
    <div class="input-group">
        <input name="nombre" placeholder="Nombre completo" required>
    </div>

    <div class="input-group">
        <input name="correo" placeholder="Correo electrónico" required>
    </div>

    <div class="input-group">
        <textarea name="comentario" placeholder="¿Qué te pareció la clase?"></textarea>
    </div>

    <div class="input-group">
        <input type="file" name="foto" accept="image/*" onchange="preview(event)" required>
        <div class="preview" id="preview"></div>
    </div>

    <div class="checkbox">
        <input type="checkbox" required>
        <label>Acepto términos y condiciones</label>
    </div>

    <button type="submit">Registrarme</button>
</form>
</div>
</div>

<div class="toast" id="toast">✅ Registro completado</div>

<script>
// =========================
// TOAST
// =========================
const params = new URLSearchParams(window.location.search);
if(params.get("ok")){
    const t = document.getElementById("toast");
    t.classList.add("show");
    setTimeout(()=>t.classList.remove("show"),3000);
}

// =========================
// PREVIEW IMAGEN
// =========================
function preview(e){
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = function(){
        document.getElementById("preview").innerHTML =
        `<img src="${reader.result}">`;
    }
    reader.readAsDataURL(file);
}

// =========================
// PARTÍCULAS CON CONEXIONES
// =========================
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

for(let i=0;i<70;i++){
    particles.push({
        x:Math.random()*canvas.width,
        y:Math.random()*canvas.height,
        vx:(Math.random()-0.5)*0.7,
        vy:(Math.random()-0.5)*0.7
    });
}

function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);

    particles.forEach(p=>{
        p.x+=p.vx;
        p.y+=p.vy;

        if(p.x<0||p.x>canvas.width) p.vx*=-1;
        if(p.y<0||p.y>canvas.height) p.vy*=-1;

        ctx.beginPath();
        ctx.arc(p.x,p.y,2,0,Math.PI*2);
        ctx.fillStyle="#4ade80";
        ctx.fill();
    });

    // conexiones
    for(let i=0;i<particles.length;i++){
        for(let j=i+1;j<particles.length;j++){
            let dx = particles[i].x - particles[j].x;
            let dy = particles[i].y - particles[j].y;
            let dist = Math.sqrt(dx*dx+dy*dy);

            if(dist < 120){
                ctx.strokeStyle="rgba(74,222,128,0.2)";
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }

    requestAnimationFrame(draw);
}

draw();
</script>

</body>
</html>
"""


# =========================
# RUTAS
# =========================
@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/submit", methods=["POST"])
def submit():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    comentario = request.form["comentario"]

    foto = request.files["foto"]
    filename = f"{datetime.now().timestamp()}_{foto.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    foto.save(path)

    # Guardar en CSV
    file_exists = os.path.isfile("data.csv")

    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["nombre","correo","comentario","foto"])

        writer.writerow([nombre, correo, comentario, filename])

    return redirect("/?ok=1")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)