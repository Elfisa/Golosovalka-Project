import flask
from flask import Flask, url_for, request

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/astronaut_selection', methods=['POST', 'GET'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style2.css')}" />
                            <title>Отбор астронавтов</title>
                          </head>
                          <body>
                            <center>
                              <h1>Анкета претендента</h1>
                              <h3>на участие в миссии</h3>
                            </center>
                            <div>
                                <form class="login_form" method="post" enctype="multipart/form-data">
                                    <input type="text" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                                    <input type="text" class="form-control" id="name" placeholder="Введите имя" name="name"><br>
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <div class="form-group">
                                        <label for="classSelect">Какое у вас образование?</label>
                                        <select class="form-control" id="classSelect" name="education">
                                          <option>Начальное</option>
                                          <option>Среднее</option>
                                          <option>Высшее</option>
                                        </select>
                                    </div><br>
                                    <div class="form-group">
                                        <label for="form-check">Какие у вас есть профессии?</label>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="researcher">Инженер-исследователь</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="pilot">Пилот</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="stroitel">Строитель</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="biolog">Экзобиолог</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="doctor">Врач</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="terra engineer">Инженер по терраформированию</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="radiation specialist">Специалист по радиационной защите</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="astrogeolog">Астрогеолог</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="glaziolog">Гляциолог</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="life engineer">Инженер жизнеобеспечения</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="meteorolog">Метеоролог</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="operator">Оператор марсохода</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="shturman">Штурман</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="cyberengineer">Киберинженер</label>
                                        </div>
                                        <div class="form-check">
                                          <input type="checkbox" class="form-check-input" id="acceptRules" name="profession">
                                          <label class="form-check-label" for="pilot dronov">Пилот дронов</label>
                                        </div>
                                    </div><br>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div><br>
                                    <div class="form-group">
                                        <label for="about">Почему вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div><br>
                                    <div class="form-group">
                                      <label for="photo">Выберите файл</label>
                                      <input type="file" class="form-control-file" id="photo" name="file">
                                    </div><br>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                                    </div><br>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['surname'])
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['education'])
        print(request.form['about'])
        print(request.form['profession'])
        print(request.form['sex'])
        print(request.form['accept'])
        print(request.files['file'])
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
