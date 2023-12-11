from flask import Flask, render_template, request, redirect, url_for
import os
import database as db
#prueba 5dic
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM martin")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)
try:
#Ruta para guardar usuarios en la bdd
    @app.route('/user', methods=['POST'])
    def addUser():
        nombre = request.form['nombre']
        asignatura = request.form['asignatura']
        nota = request.form['nota']

        if nombre and asignatura and nota:
            cursor = db.database.cursor()
            sql = "INSERT INTO martin (nombre, asignatura, nota) VALUES (%s, %s, %s)"
            data = (nombre, asignatura, nota)
            cursor.execute(sql, data)
            db.database.commit()
        return redirect(url_for('home'))
except ValueError:
    print("Tipo de dato incorrecto")

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM martin WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    asignatura = request.form['asignatura']
    nota = request.form['nota']

    if nombre and asignatura and nota:
        cursor = db.database.cursor()
        sql = "UPDATE martin SET nombre = %s, asignatura = %s, nota = %s WHERE id = %s"
        data = (nombre, asignatura, nota, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/jugar/', methods=(['GET']))
def jugar():
    
    return render_template('jugar.html')



if __name__ == '__main__':
    app.run(debug=True, port=5500)
