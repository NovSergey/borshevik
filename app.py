import os
import secrets
from flask_restful import abort
from flask import Flask, render_template, redirect
from os import getenv
from data import db_session
from data.users import User
from data.polygons import Polygons
from forms.user import AddPolygon, RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, static_url_path='', static_folder='templates/static')

login_manager = LoginManager()
login_manager.init_app(app)

#UPLOAD_PATH = '/var/www/u2483731/data/www/proborshevik67.ru/templates/static/'
UPLOAD_PATH = 'templates/static/'
map_api = "ef7b9ab9-d96b-45b2-aab6-51fdb0d80171"
app.config['SECRET_KEY'] = "borsheviktopsmol"


#@app.route("/")
#def index():
#    return render_template("index.html", title='proborshevik67.ru')

@app.route("/")
def history():
    return render_template("history.html", title='История')

@app.route("/danger")
def danger():
    return render_template("danger.html", title='Опасность')

@app.route("/methods")
def methods():
    return render_template("methods.html", title='Методы борьбы')

@app.route("/application")
def application():
    return render_template("application.html", title='Применение')

@app.route("/pmp")
def pmp():
    return render_template("pmp.html", title='Пмп')
    
@app.route("/sources")
def sources():
    return render_template("sources.html", title='Источники')
    
@app.route("/fight")
def fight():
    return render_template("fight.html", title='Источники')

    
@app.route("/map")
def map():
    return render_template("map.html", title="Карта", api=map_api)

def ret_coords(pols):
    coords = []
    for coord in pols:
        coords.append([[[[float(j) for j in i.split(",")] for i in k.split(";")] for k in coord.coords.split('/')], coord.status])
        print(coords)
    return coords

@app.route("/add_polygon", methods=['GET', 'POST'])
def add_polygon():
    if current_user.is_authenticated:
        form = AddPolygon()
        db_sess = db_session.create_session()
        if form.validate_on_submit():
            for i in form.coords.data[:-2].split('|'):
                polygon = Polygons()
                name = secrets.token_hex(16)
                if form.file.data:
                    form.file.data.save(UPLOAD_PATH + "polygons_imgs/" + f"{name}.png")  # сохранение каринки
                    polygon.picture = f"polygons_imgs/{name}.png"
                else:
                    polygon.picture = f""
                polygon.coords = i
                polygon.status = 0
                db_sess.add(polygon)
                db_sess.commit()
            return redirect("/map")
        return render_template("add.html", title='Добавление точки', form=form, api=map_api)
    else:
        return redirect("/map")

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if not current_user.is_authenticated:
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                    form=form,
                                    message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                status = "user"
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Регистрация', form=form)
    else:
        return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
        return render_template('login.html', title='Авторизация', form=form)
    else:
        return redirect("/")
        
def get_coords(flag):
    db_sess = db_session.create_session()
    pols = db_sess.query(Polygons)
    coords = []
    for coord in pols:
        if flag == coord.status:
            coords.append([[[[float(j) for j in i.split(",")] for i in k.split(";")] for k in coord.coords.split('/')], coord.id])
    return dict(coords=coords)

@app.route('/get_coords_vis')
def get_coords_vis():
    return get_coords(True)

@app.route('/get_coords_hid')
def get_coords_hid():
    return get_coords(False)

@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.status == "admin" or not current_user.is_authenticated:
        return render_template('admin_panel.html', title='proborshevik67.info', api=map_api)
    else:
        return redirect("/")


@app.route('/pol_add/<int:id>', methods=['GET', 'POST'])
@login_required
def pol_add(id):
    if current_user.status == "admin":
        db_sess = db_session.create_session()
        pol = db_sess.query(Polygons).filter(Polygons.id == id).first()
        if pol:
            try:
                os.remove(UPLOAD_PATH+pol.picture)
            except:
                pass
            pol.picture = ""
            pol.status = 1
            db_sess.commit()
        else:
            abort(404)
        return redirect("/admin_panel")
    else:
        return redirect("/")

@app.route('/pol_remove/<int:id>', methods=['GET', 'POST'])
@login_required
def pol_remove(id):
    if current_user.status == "admin":
        db_sess = db_session.create_session()
        pol = db_sess.query(Polygons).filter(Polygons.id == id).first()
        if pol:
            try:
                os.remove(UPLOAD_PATH+pol.picture)
            except:
                pass
            db_sess.delete(pol)
            db_sess.commit()
        else:
            abort(404)
        return redirect("/admin_panel")
    else:
        return redirect("/")
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

def main():
    #db_session.global_init(user='u2483731_borshev', password='Koshka+12*', host='127.0.0.1',database='u2483731_borshevik')
    db_session.global_init_sql("db/data.db")

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', debug=True)
    
