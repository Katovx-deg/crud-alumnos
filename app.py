from flask import Flask, render_template, request, redirect, url_for, flash
import MySQLdb

app = Flask(__name__)
app.secret_key = 'clave_secreta_123'


DB_CONFIG = {
    'host':   'localhost',
    'user':   'root',
    'passwd': '',       
    'db':     'taller_alumnos',
    'charset':'utf8mb4',
}

def get_db():
    return MySQLdb.connect(**DB_CONFIG)


@app.route('/')
def index():
    db  = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, nombre, apellido, edad, correo FROM alumnos ORDER BY id DESC")
    alumnos = cur.fetchall()
    db.close()
    return render_template('index.html', alumnos=alumnos)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre   = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        edad     = request.form['edad'].strip()
        correo   = request.form['correo'].strip()

        if not nombre or not apellido or not edad or not correo:
            flash('⚠️ Todos los campos son obligatorios.', 'warning')
            return redirect(url_for('crear'))

        db  = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO alumnos (nombre, apellido, edad, correo) VALUES (%s, %s, %s, %s)",
            (nombre, apellido, int(edad), correo)
        )
        db.commit()
        db.close()
        flash('Alumno creado exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', accion='Crear', alumno=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    db  = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        nombre   = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        edad     = request.form['edad'].strip()
        correo   = request.form['correo'].strip()

        cur.execute(
            "UPDATE alumnos SET nombre=%s, apellido=%s, edad=%s, correo=%s WHERE id=%s",
            (nombre, apellido, int(edad), correo, id)
        )
        db.commit()
        db.close()
        flash('Alumno actualizado.', 'success')
        return redirect(url_for('index'))

    cur.execute("SELECT id, nombre, apellido, edad, correo FROM alumnos WHERE id=%s", (id,))
    alumno = cur.fetchone()
    db.close()

    if not alumno:
        flash('Alumno no encontrado.', 'danger')
        return redirect(url_for('index'))

    return render_template('form.html', accion='Editar', alumno=alumno)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    db  = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM alumnos WHERE id=%s", (id,))
    db.commit()
    db.close()
    flash('Alumno eliminado.', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)