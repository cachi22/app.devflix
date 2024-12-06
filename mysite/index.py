from flask import Flask, render_template, request, redirect, url_for, flash, session
import firebase_admin
from firebase_admin import credentials, db
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializar Firebase
cred = credentials.Certificate("devflixalumnos-firebase-adminsdk-y80cc-ec8273a96d.json")  # Ruta al archivo JSON de Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://devflixalumnos-default-rtdb.firebaseio.com/'
})

# Inicializar Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesaria para manejar sesiones

# Página de Inicio
@app.route('/')
def home():
    return render_template('home.html')

# Página de Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        confirmar_contraseña = request.form['confirmarContraseña']

        # Validaciones
        if contraseña != confirmar_contraseña:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('registro'))

        # Verificar si el correo ya existe en Firebase
        ref = db.reference('alumnos')  # Referencia a la colección 'alumnos'
        alumnos = ref.get()

        if alumnos and any(alumno['correo'] == correo for alumno in alumnos.values()):
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('registro'))

        # Guardar usuario en Firebase con contraseña hasheada
        nuevo_alumno = {
            'nombre': nombre,
            'correo': correo,
            'contraseña': generate_password_hash(contraseña)  # Hasheamos la contraseña
        }
        ref.push(nuevo_alumno)

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

# Página de Inicio de Sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Referencia a Firebase
        ref = db.reference('alumnos')
        alumnos = ref.get()

        if alumnos:
            for key, alumno in alumnos.items():
                if alumno['correo'] == correo and check_password_hash(alumno['contraseña'], contraseña):
                    # Iniciar sesión
                    session['user'] = alumno['nombre']  # Guardar nombre en sesión
                    flash(f'Bienvenido {alumno["nombre"]}', 'success')
                    return redirect(url_for('perfil'))

        flash('Correo o contraseña incorrectos', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

# Página de Perfil (Protegida)
@app.route('/perfil')
def perfil():
    if 'user' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('login'))

    return render_template('perfil.html', nombre=session['user'])

# Cerrar Sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('home'))

# Página de Cursos
@app.route('/cursos')
def cursos():
    return render_template('cursos.html')

# Blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Página "Nosotros"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Soporte
@app.route('/soporte')
def soporte():
    return render_template('soporte.html')

# Detalle de un curso
@app.route('/detalle_curso')
def detalle_curso():
    curso_id = request.args.get('id')  # Obtener parámetro 'id'
    return render_template('detalle_curso.html', curso_id=curso_id)

if __name__ == '__main__':
    app.run(debug=True)
