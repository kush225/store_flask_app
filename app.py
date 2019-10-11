from flask import Flask, render_template, redirect, url_for,request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, IntegerField, validators
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        flash("Invalid username or password","danger")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
        if user is None:
            db.session.add(new_user)
            db.session.commit()
            flash("User Account Created","success")
        else:
            flash('User with "{0}" Username or "{1}" as Email Address already Exist' .format(user.username,user.email), "danger")
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    result = Item.query.filter_by(user_name=current_user.username)
    if result:
        return render_template('dashboard.html', name=current_user.username,items=result)
    return render_template('dashboard.html',items=result, name=current_user.username,msg=msg)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

class Item(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    user_name = db.Column(db.String(15))

class ItemForm(Form):
    name = StringField('name', [validators.Length(min=2, max=20)])
    price = IntegerField('Price')

@app.route('/item/<string:name>')
@login_required
def get(name):
    result = Item.query.filter_by(name=name,user_name=current_user.username).first()
    if result:
        return render_template('item.html',item =result, name=current_user.username)
    return render_template('no_item.html', name=current_user.username),404


@app.route('/edit_item/<string:id>', methods=['GET','POST'])
@login_required
def set(id):
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        result = Item.query.filter_by(id=id).first()
        result.name = form.name.data
        result.price = form.price.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', form=form)

@app.route('/add_item', methods=['GET','POST'])
@login_required
def add_item():
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        result = Item.query.filter_by(name=form.name.data,user_name=current_user.username).first()
        if result:
            flash("Item with {} Name Already Exist".format(form.name.data), "failure")
        else:
            new_item = Item(name=form.name.data, price=form.price.data, user_name=current_user.username)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('add_item.html', form=form)

@app.route('/delete_item/<string:id>', methods=['POST'])
@login_required
def delete_item(id):
    Item.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
