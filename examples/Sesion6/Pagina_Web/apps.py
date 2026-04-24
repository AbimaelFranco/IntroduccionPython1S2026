# =========================
# INSTALACIÓN DE LIBRERÍAS
# =========================

# pip install flask

# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================

from flask import Flask, request, render_template_string, redirect
# Flask: framework para crear aplicaciones web
# request: permite acceder a los datos enviados desde el formulario
# render_template_string: permite renderizar HTML directamente desde un string
# redirect: permite redirigir a otra página

import os
# Permite trabajar con el sistema de archivos (crear carpetas, rutas, etc.)

import csv
# Permite guardar datos en formato CSV (como Excel)

from datetime import datetime
# Permite obtener fecha y hora actual


# =========================
# CREACIÓN DE LA APP
# =========================

app = Flask(__name__)

# Carpeta donde se guardarán las imágenes subidas
UPLOAD_FOLDER = "examples/uploads"

# Crear la carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# HTML (FRONTEND)
# =========================

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Título de la página -->
<title>Registro Inteligente</title>

<style>
/* =========================
   RESET GENERAL
========================= */
* {
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family: 'Segoe UI', sans-serif;
}

/* =========================
   FONDO PRINCIPAL
========================= */
body {
    height:100vh;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    overflow:hidden;
    color:white;
}

/* =========================
   CANVAS PARA PARTÍCULAS
========================= */
canvas {
    position:fixed;
    top:0;
    left:0;
    z-index:-1;
}

/* =========================
   CONTENEDOR PRINCIPAL
========================= */
.container {
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    padding:20px;
}

/* Tarjeta donde está el formulario */
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

/* Animación de entrada */
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

/* Efecto al enfocar */
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

/* Efecto hover */
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
   TOAST (MENSAJE)
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

/* Cuando se activa */
.toast.show {
    opacity:1;
    transform:translateY(0);
}
</style>
</head>

<body>

<!-- Canvas para animación de fondo -->
<canvas id="bg"></canvas>

<div class="container">
<div class="card">

<!-- Título -->
<h2 style="text-align:center; margin-bottom:15px;">Registro 🚀</h2>

<!-- FORMULARIO -->
<form action="/submit" method="POST" enctype="multipart/form-data">
    
    <!-- Nombre -->
    <div class="input-group">
        <input name="nombre" placeholder="Nombre completo" required>
    </div>

    <!-- Correo -->
    <div class="input-group">
        <input name="correo" placeholder="Correo electrónico" required>
    </div>

    <!-- Comentario -->
    <div class="input-group">
        <textarea name="comentario" placeholder="¿Qué te pareció la clase?"></textarea>
    </div>

    <!-- Subida de imagen -->
    <div class="input-group">
        <input type="file" name="foto" accept="image/*" onchange="preview(event)" required>
        <div class="preview" id="preview"></div>
    </div>

    <!-- Checkbox -->
    <div class="checkbox">
        <input type="checkbox" required>
        <label>Acepto términos y condiciones</label>
    </div>

    <!-- Botón -->
    <button type="submit">Registrarme</button>
</form>
</div>
</div>

<!-- Mensaje de éxito -->
<div class="toast" id="toast">✅ Registro completado</div>

<script>
// =========================
// TOAST (MENSAJE DE ÉXITO)
// =========================

// Leer parámetros de la URL
const params = new URLSearchParams(window.location.search);

// Si existe ?ok=1 mostrar mensaje
if(params.get("ok")){
    const t = document.getElementById("toast");
    t.classList.add("show");

    // Ocultarlo después de 3 segundos
    setTimeout(()=>t.classList.remove("show"),3000);
}

// =========================
// PREVIEW IMAGEN
// =========================
function preview(e){
    const file = e.target.files[0];
    const reader = new FileReader();

    // Cuando se carga la imagen
    reader.onload = function(){
        document.getElementById("preview").innerHTML =
        `<img src="${reader.result}">`;
    }

    // Leer archivo como URL
    reader.readAsDataURL(file);
}

// =========================
// PARTÍCULAS ANIMADAS
// =========================

// Obtener canvas
const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");

// Ajustar tamaño
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Lista de partículas
let particles = [];

// Crear partículas aleatorias
for(let i=0;i<70;i++){
    particles.push({
        x:Math.random()*canvas.width,
        y:Math.random()*canvas.height,
        vx:(Math.random()-0.5)*0.7,
        vy:(Math.random()-0.5)*0.7
    });
}

// Función de dibujo
function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);

    particles.forEach(p=>{
        p.x+=p.vx;
        p.y+=p.vy;

        // Rebote en bordes
        if(p.x<0||p.x>canvas.width) p.vx*=-1;
        if(p.y<0||p.y>canvas.height) p.vy*=-1;

        // Dibujar partícula
        ctx.beginPath();
        ctx.arc(p.x,p.y,2,0,Math.PI*2);
        ctx.fillStyle="#4ade80";
        ctx.fill();
    });

    // Dibujar conexiones entre partículas cercanas
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

// Iniciar animación
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
    # Muestra el HTML en la página principal
    return render_template_string(HTML)


@app.route("/submit", methods=["POST"])
def submit():
    # Obtener datos del formulario
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    comentario = request.form["comentario"]

    # Obtener archivo (imagen)
    foto = request.files["foto"]

    # Crear nombre único
    filename = f"{datetime.now().timestamp()}_{foto.filename}"

    # Ruta donde guardar
    path = os.path.join(UPLOAD_FOLDER, filename)

    # Guardar archivo
    foto.save(path)

    # Verificar si CSV existe
    file_exists = os.path.isfile("data.csv")

    # Abrir CSV en modo agregar
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Escribir encabezados si es nuevo
        if not file_exists:
            writer.writerow(["nombre","correo","comentario","foto"])

        # Guardar datos
        writer.writerow([nombre, correo, comentario, filename])

    # Redirigir con mensaje de éxito
    return redirect("/?ok=1")


# =========================
# EJECUCIÓN
# =========================

if __name__ == "__main__":
    # Iniciar servidor en modo debug
    app.run(debug=True)