from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Plantilla HTML para la encuesta inicial con opciones de universidad, carrera y edad
encuesta_inicial_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Encuesta Divertida - Universidad</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f8ff; color: #333; text-align: center; }
        h1, h2 { color: #2c3e50; }
        form { margin: 20px; padding: 20px; border: 1px solid #3498db; border-radius: 10px; background-color: #ecf0f1; display: inline-block; }
        select, input[type="number"], button { margin: 10px; padding: 8px; font-size: 16px; border-radius: 5px; border: 1px solid #3498db; }
        input[type="submit"] { background-color: #3498db; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; }
        input[type="submit"]:hover { background-color: #2980b9; }
    </style>
</head>
<body style="text-align: center;">
    <h1>¿Qué universidad estudias?</h1>
    <form action="/encuesta/carrera" method="post">
        <select name="universidad" required>
            <option value="politecnica">Politecnica</option>
            <option value="catolica">Católica</option>
            <option value="uce">UCE</option>
        </select>
        <h2>¿Carrera que estudias?</h2>
        <select name="carrera" required>
            <option value="psicologia">Psicología</option>
            <option value="ingenieria">Ingeniería</option>
            <option value="medicina">Medicina</option>
            <option value="administracion">Administración</option>
            <option value="odontologia">Odontología</option>
            <option value="quimica">Química</option>
            <option value="otro">Otro</option>
        </select>
        <h2>¿Edad?</h2>
        <input type="number" name="edad" required><br><br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
"""

# Plantilla para el resultado inicial según universidad y carrera
resultado_inicial_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado Inicial</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; text-align: center; }
        h1 { color: #3498db; }
        button { padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin: 10px; }
        .si { background-color: #2ecc71; color: white; border: none; }
        .no { background-color: #e74c3c; color: white; border: none; }
    </style>
</head>
<body style="text-align: center;">
    <h1>{{ resultado }}</h1>
    <form action="/encuesta/animal" method="post">
        <button type="submit" name="continuar" value="si">Sí</button>
        <button type="submit" name="continuar" value="no">No</button>
    </form>
</body>
</html>
"""

# Plantilla HTML para la segunda parte de la encuesta con preguntas adicionales
encuesta_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Encuesta Divertida - Preguntas</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f1e3; color: #333; text-align: center; }
        h1 { color: #9b59b6; }
        form { padding: 20px; background-color: #ffffff; border-radius: 10px; display: inline-block; margin-top: 20px; }
        input[type="radio"] { margin: 5px; }
        input[type="submit"] { background-color: #9b59b6; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 5px; cursor: pointer; }
        input[type="submit"]:hover { background-color: #8e44ad; }
    </style>
</head>
<body style="text-align: center;">
    <h1>Responde las siguientes preguntas</h1>
    <form action="/encuesta/resultado" method="post">
        <h2>1. Si fueras un animal, ¿cuál serías?</h2>
        <input type="radio" name="animal" value="gato"> Un gato 🐱<br>
        <input type="radio" name="animal" value="perro"> Un perro 🐶<br>
        <input type="radio" name="animal" value="tigre"> Un tigre 🐯<br>
        <input type="radio" name="animal" value="delfín"> Un delfín 🐬<br><br>
        
        <h2>2. ¿Cuál es tu comida favorita?</h2>
        <input type="radio" name="comida" value="pizza"> Pizza 🍕<br>
        <input type="radio" name="comida" value="sushi"> Sushi 🍣<br>
        <input type="radio" name="comida" value="hamburguesa"> Hamburguesa 🍔<br>
        <input type="radio" name="comida" value="ensalada"> Ensalada 🥗<br><br>

        <h2>3. ¿Cuál sería tu superpoder ideal?</h2>
        <input type="radio" name="superpoder" value="volar"> Volar 🕊️<br>
        <input type="radio" name="superpoder" value="leer mente"> Leer la mente 💭<br>
        <input type="radio" name="superpoder" value="fuerza"> Superfuerza 💪<br>
        <input type="radio" name="superpoder" value="invisibilidad"> Invisibilidad 👻<br><br>
        
        <input type="submit" value="Ver Resultado">
    </form>
</body>
</html>
"""

# Plantilla para el resultado final de la encuesta
resultado_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado Final</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #eaf2f8; color: #333; text-align: center; }
        h1 { color: #e67e22; }
        p { font-size: 18px; }
    </style>
</head>
<body style="text-align: center;">
    <h1>🎉 ¡Aquí está tu resultado divertido! 🎉</h1>
    <p>{{ resultado }}</p>
</body>
</html>
"""

# Plantilla para la página de match con Franchesco
match_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>¡Haz hecho match con Franchesco!</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #fff5e1; color: #333; text-align: center; }
        h1 { color: #ff6b6b; }
        .boton { padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin: 10px; }
        .beso { background-color: #ff6b6b; color: white; }
        .shot { background-color: #f39c12; color: white; }
    </style>
</head>
<body style="text-align: center;">
    <h1>¡Haz hecho match con Franchesco!</h1>
    <p>Del 1 al 10, ¿qué tan bien se ve?</p>
    <form action="/encuesta/match-resultado" method="post">
        {% for i in range(1, 11) %}
            <input type="radio" name="puntuacion" value="{{ i }}"> {{ i }}<br>
        {% endfor %}
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
"""
#pablo
match2_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>¡Haz hecho match con Pablo!</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #fff5e1; color: #333; text-align: center; }
        h1 { color: #ff6b6b; }
        .boton { padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin: 10px; }
        .beso { background-color: #ff6b6b; color: white; }
        .shot { background-color: #f39c12; color: white; }
    </style>
</head>
<body style="text-align: center;">
    <h1>¡Haz hecho match con Pablo!</h1>
    <p>Del 1 al 10, ¿qué tan bien se ve?</p>
    <form action="/encuesta/match-resultado" method="post">
        {% for i in range(1, 11) %}
            <input type="radio" name="puntuacion" value="{{ i }}"> {{ i }}<br>
        {% endfor %}
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
"""
# Plantilla para el resultado del match
match_resultado_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado del Match</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f1e3; color: #333; text-align: center; }
        h1 { color: #27ae60; }
        p { font-size: 18px; color: #e74c3c; }
        .mensaje { font-size: 20px; font-weight: bold; }
        .dislike { color: #e74c3c; }
        .confianza { color: #f39c12; }
    </style>
</head>
<body style="text-align: center;">
    <h1>{{ mensaje }}</h1>
</body>
</html>
"""
# Plantilla para el resultado del match
match2_resultado_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultado del Match</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f1e3; color: #333; text-align: center; }
        h1 { color: #27ae60; }
        p { font-size: 18px; color: #e74c3c; }
        .mensaje { font-size: 20px; font-weight: bold; }
        .dislike { color: #e74c3c; }
        .confianza { color: #f39c12; }
    </style>
</head>
<body style="text-align: center;">
    <h1>{{ mensaje }}</h1>
</body>
</html>
"""
@app.route('/')
def inicio():
    return render_template_string(encuesta_inicial_html)

@app.route('/encuesta/carrera', methods=['POST'])
def encuesta_carrera():
    universidad = request.form.get('universidad')
    carrera = request.form.get('carrera')
    
    if universidad == "uce" and carrera == "psicologia":
        resultado = "¿Quieres decir que eres psicoloba de la UCE?"
    elif universidad == "uce" and carrera == "medicina":
        resultado = "¿Quieres decir que eres mediloca de la UCE?"
    elif universidad == "uce" and carrera == "odontologia":
        resultado = "¿Quieres decir que eres odontonena de la UCE?"
    elif carrera == "otro":
        resultado = "Eres diferente a las demás"
    else:
        resultado = "¡Eres muy joven para la Carrera!"
    
    return render_template_string(resultado_inicial_html, resultado=resultado)

@app.route('/encuesta/animal', methods=['POST'])
def encuesta_animal():
    return render_template_string(encuesta_html)

@app.route('/encuesta/resultado', methods=['POST'])
def encuesta_resultado():
    animal = request.form.get('animal')
    comida = request.form.get('comida')
    superpoder = request.form.get('superpoder')
    
    # Resultado para el "match"
    if animal == "perro" and comida == "pizza" and superpoder == "volar":
        return render_template_string(match_html)
    if animal == "gato" and comida == "pizza" and superpoder == "leer mente":
        return render_template_string(match2_html)
    # Otros resultados
    resultado = "¡Eres una persona única y especial!"  # Mensaje predeterminado
   # Combinación de animal, comida y superpoder
    if animal == "tigre" and comida == "pizza" and superpoder == "volar":
        resultado = "¡Eres una persona intensa! Siempre destacas y tienes una energía poderosa. 🐯💥"
    elif animal == "tigre" and comida == "pizza" and superpoder == "leer mente":
        resultado = "¡Eres un líder natural! Tus decisiones están siempre llenas de inteligencia. 🐯🧠"
    elif animal == "tigre" and comida == "pizza" and superpoder == "superfuerza":
        resultado = "¡Eres una fuerza de la naturaleza! Nadie puede detener tu energía. 🐯💪"
    elif animal == "tigre" and comida == "pizza" and superpoder == "invisibilidad":
        resultado = "¡Eres un misterio! Siempre te mantienes un paso adelante. 🐯👻"
    
    elif animal == "tigre" and comida == "sushi" and superpoder == "volar":
        resultado = "¡Eres un alma libre! Siempre vuelas alto sin que nada te detenga. 🐯🍣✈️"
    elif animal == "tigre" and comida == "sushi" and superpoder == "leer mente":
        resultado = "¡Eres muy astuto! Siempre entiendes lo que los demás piensan. 🐯🍣🧠"
    elif animal == "tigre" and comida == "sushi" and superpoder == "superfuerza":
        resultado = "¡Eres una máquina imparable! Con tu fuerza, no hay nada que te detenga. 🐯🍣💪"
    elif animal == "tigre" and comida == "sushi" and superpoder == "invisibilidad":
        resultado = "¡Eres un ninja! Siempre invisibles, siempre perfectos. 🐯🍣👻"
    
    elif animal == "tigre" and comida == "hamburguesa" and superpoder == "volar":
        resultado = "¡Eres el rey de la jungla! Siempre estás en control de todo. 🐯🍔✈️"
    elif animal == "tigre" and comida == "hamburguesa" and superpoder == "leer mente":
        resultado = "¡Tu poder mental es asombroso! Nadie te engaña. 🐯🍔🧠"
    elif animal == "tigre" and comida == "hamburguesa" and superpoder == "superfuerza":
        resultado = "¡Un verdadero titán! Nadie puede competir con tu poder. 🐯🍔💪"
    elif animal == "tigre" and comida == "hamburguesa" and superpoder == "invisibilidad":
        resultado = "¡Eres el mejor espía! Siempre te escapas sin ser visto. 🐯🍔👻"
    
    elif animal == "tigre" and comida == "ensalada" and superpoder == "volar":
        resultado = "¡Eres un águila! Vuelas alto y con elegancia. 🐯🥗✈️"
    elif animal == "tigre" and comida == "ensalada" and superpoder == "leer mente":
        resultado = "¡Eres muy sabio! Siempre entiendes todo a tu alrededor. 🐯🥗🧠"
    elif animal == "tigre" and comida == "ensalada" and superpoder == "superfuerza":
        resultado = "¡Con tu fuerza y sabiduría, nadie puede pararte! 🐯🥗💪"
    elif animal == "tigre" and comida == "ensalada" and superpoder == "invisibilidad":
        resultado = "¡Eres un fantasma! Nadie te ve venir. 🐯🥗👻"

    elif animal == "gato" and comida == "pizza" and superpoder == "volar":
        resultado = "¡Eres un gato volador! Siempre elegante y nunca te caes. 🐱🍕✈️"
    elif animal == "gato" and comida == "pizza" and superpoder == "superfuerza":
        resultado = "¡Un gato con súper fuerza! Nadie te puede parar. 🐱🍕💪"
    elif animal == "gato" and comida == "pizza" and superpoder == "invisibilidad":
        resultado = "¡Un gato invisible! Nadie te ve llegar. 🐱🍕👻"

    elif animal == "gato" and comida == "sushi" and superpoder == "volar":
        resultado = "¡Eres un gato elegante! Con sushi y vuelos, ¿qué más se puede pedir? 🐱🍣✈️"
    elif animal == "gato" and comida == "sushi" and superpoder == "leer mente":
        resultado = "¡Tu mente es tan afilada como tus garras! 🐱🍣🧠"
    elif animal == "gato" and comida == "sushi" and superpoder == "superfuerza":
        resultado = "¡Un gato súper fuerte! Nadie puede resistirse a tu poder. 🐱🍣💪"
    elif animal == "gato" and comida == "sushi" and superpoder == "invisibilidad":
        resultado = "¡Eres un ninja gato! Siempre invisibles, siempre perfectos. 🐱🍣👻"

    elif animal == "gato" and comida == "hamburguesa" and superpoder == "volar":
        resultado = "¡Eres un gato volador! Siempre sobrevolando el caos. 🐱🍔✈️"
    elif animal == "gato" and comida == "hamburguesa" and superpoder == "leer mente":
        resultado = "¡Eres un gato psíquico! Siempre sabes lo que los demás quieren. 🐱🍔🧠"
    elif animal == "gato" and comida == "hamburguesa" and superpoder == "superfuerza":
        resultado = "¡Un gato con fuerza sobrehumana! ¡Imparable! 🐱🍔💪"
    elif animal == "gato" and comida == "hamburguesa" and superpoder == "invisibilidad":
        resultado = "¡Un gato ninja! Nadie sabe cuándo llegas o te vas. 🐱🍔👻"

    elif animal == "gato" and comida == "ensalada" and superpoder == "volar":
        resultado = "¡Eres un gato que vuela alto con mucha clase! 🐱🥗✈️"
    elif animal == "gato" and comida == "ensalada" and superpoder == "leer mente":
        resultado = "¡Eres un gato sabio! Siempre entiendes lo que los demás piensan. 🐱🥗🧠"
    elif animal == "gato" and comida == "ensalada" and superpoder == "superfuerza":
        resultado = "¡Eres un gato fuerte! Nadie puede contigo. 🐱🥗💪"
    elif animal == "gato" and comida == "ensalada" and superpoder == "invisibilidad":
        resultado = "¡Un gato invisible con gran estilo! 🐱🥗👻"   

  # Combinaciones para perro

    elif animal == "perro" and comida == "pizza" and superpoder == "leer mente":
        resultado = "¡Tu mente es tan aguda como tu instinto de perro! 🐶🍕🧠"
    elif animal == "perro" and comida == "pizza" and superpoder == "superfuerza":
        resultado = "¡Un perro súper fuerte! ¡Tienes el poder de un león! 🐶🍕💪"
    elif animal == "perro" and comida == "pizza" and superpoder == "invisibilidad":
        resultado = "¡Eres un perro ninja! Nadie te ve llegar. 🐶🍕👻"

    elif animal == "perro" and comida == "sushi" and superpoder == "volar":
        resultado = "¡Eres un perro volador con sushi! ¡Qué combinación más genial! 🐶🍣✈️"
    elif animal == "perro" and comida == "sushi" and superpoder == "leer mente":
        resultado = "¡Un perro con poderes psíquicos! Sabes lo que piensan los demás. 🐶🍣🧠"
    elif animal == "perro" and comida == "sushi" and superpoder == "superfuerza":
        resultado = "¡Un perro con súper fuerza! Nadie te puede parar. 🐶🍣💪"
    elif animal == "perro" and comida == "sushi" and superpoder == "invisibilidad":
        resultado = "¡Eres un perro invisible! Nadie sabe dónde estás. 🐶🍣👻"

    elif animal == "perro" and comida == "hamburguesa" and superpoder == "volar":
        resultado = "¡Un perro volador con hamburguesas! ¿Qué más se puede pedir? 🐶🍔✈️"
    elif animal == "perro" and comida == "hamburguesa" and superpoder == "leer mente":
        resultado = "¡Tu mente es tan aguda como un perro persiguiendo su hueso! 🐶🍔🧠"
    elif animal == "perro" and comida == "hamburguesa" and superpoder == "superfuerza":
        resultado = "¡Un perro con una fuerza increíble! Nadie puede competir contigo. 🐶🍔💪"
    elif animal == "perro" and comida == "hamburguesa" and superpoder == "invisibilidad":
        resultado = "¡Eres un perro invisible! Nadie puede ver lo increíble que eres. 🐶🍔👻"

    elif animal == "perro" and comida == "ensalada" and superpoder == "volar":
        resultado = "¡Un perro volador con una dieta saludable! 🐶🥗✈️"
    elif animal == "perro" and comida == "ensalada" and superpoder == "leer mente":
        resultado = "¡Tu mente es tan clara como un perro con su dueño! 🐶🥗🧠"
    elif animal == "perro" and comida == "ensalada" and superpoder == "superfuerza":
        resultado = "¡Un perro fuerte y saludable! 🐶🥗💪"
    elif animal == "perro" and comida == "ensalada" and superpoder == "invisibilidad":
        resultado = "¡Eres un perro invisible con una dieta perfecta! 🐶🥗👻"
        
         # Combinaciones para delfín
    elif animal == "delfín" and comida == "pizza" and superpoder == "volar":
        resultado = "¡Eres un delfín volador! Surcas los cielos con gracia. 🐬🍕✈️"
    elif animal == "delfín" and comida == "pizza" and superpoder == "leer mente":
        resultado = "¡Eres un delfín súper inteligente! Siempre sabes lo que piensan los demás. 🐬🍕🧠"
    elif animal == "delfín" and comida == "pizza" and superpoder == "superfuerza":
        resultado = "¡Un delfín con súper fuerza! ¡Tienes el poder del océano! 🐬🍕💪"
    elif animal == "delfín" and comida == "pizza" and superpoder == "invisibilidad":
        resultado = "¡Un delfín invisible! Nadie puede verte venir. 🐬🍕👻"

    elif animal == "delfín" and comida == "sushi" and superpoder == "volar":
        resultado = "¡Eres un delfín volador y elegante! 🐬🍣✈️"
    elif animal == "delfín" and comida == "sushi" and superpoder == "leer mente":
        resultado = "¡Eres un delfín súper inteligente! Siempre sabes lo que los demás piensan. 🐬🍣🧠"
    elif animal == "delfín" and comida == "sushi" and superpoder == "superfuerza":
        resultado = "¡Un delfín con súper fuerza! ¡Tienes el poder de los mares! 🐬🍣💪"
    elif animal == "delfín" and comida == "sushi" and superpoder == "invisibilidad":
        resultado = "¡Un delfín invisible! Nadie sabe cuando apareces o desapareces. 🐬🍣👻"

    elif animal == "delfín" and comida == "hamburguesa" and superpoder == "volar":
        resultado = "¡Un delfín volador! ¿Quién dijo que los delfines solo nadan? 🐬🍔✈️"
    elif animal == "delfín" and comida == "hamburguesa" and superpoder == "leer mente":
        resultado = "¡Un delfín con poderes mentales! Puedes leer las mentes de todos. 🐬🍔🧠"
    elif animal == "delfín" and comida == "hamburguesa" and superpoder == "superfuerza":
        resultado = "¡Un delfín con una fuerza increíble! Nadie te puede detener. 🐬🍔💪"
    elif animal == "delfín" and comida == "hamburguesa" and superpoder == "invisibilidad":
        resultado = "¡Un delfín invisible con hamburguesas! ¡Nada como un buen secreto! 🐬🍔👻"

    elif animal == "delfín" and comida == "ensalada" and superpoder == "volar":
        resultado = "¡Un delfín que vuela alto con ensalada! ¡Saludable y libre! 🐬🥗✈️"
    elif animal == "delfín" and comida == "ensalada" and superpoder == "leer mente":
        resultado = "¡Eres un delfín con gran inteligencia! Puedes leer la mente de todos. 🐬🥗🧠"
    elif animal == "delfín" and comida == "ensalada" and superpoder == "superfuerza":
        resultado = "¡Un delfín fuerte! Nadie puede competir contigo. 🐬🥗💪"
    elif animal == "delfín" and comida == "ensalada" and superpoder == "invisibilidad":
        resultado = "¡Un delfín invisible! Nadie sabe lo que estás tramando. 🐬🥗👻"
    

# Combinaciones para gato


    return render_template_string(resultado_html, resultado=resultado)

@app.route('/encuesta/match-resultado', methods=['POST'])
def match_resultado():
    puntuacion = int(request.form.get('puntuacion'))
    
    if puntuacion <= 5:
        mensaje = "¡Mal! 👎"
    elif 6 <= puntuacion <= 8:
        mensaje = "Wow, nada mal. Reclama un shot con confianza."
    elif puntuacion >= 9:
        mensaje = "¡Beso o shot! ¿Qué eliges?"
    
    return render_template_string(match_resultado_html, mensaje=mensaje)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
