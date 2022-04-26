from flask import redirect, render_template, jsonify, make_response, Flask
from flask_login import LoginManager, login_required
from flask_restful import Api, Resource, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def run():
    return render_template('index.html')


def main():
    # db_session.global_init(f'db/mars_explorer.sqlite')
    app.run()


if __name__ == '__main__':
    main()
