from datetime import datetime
import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_dropzone import Dropzone 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from forms import RegisterForm, LoginForm, PostForm, EventosForm, UpdateForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "MEGUSTACOMERARROZ"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
dropzone = Dropzone(app)
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'


#Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first = db.Column(db.String(1000), nullable=False)
    username = db.Column(db.String(1000), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String, nullable= False, default = 'Download.jpeg')
    posts = db.relationship('Post', backref='author', lazy=True)
    eventos = db.relationship('Eventos', backref = 'user', lazy = True )
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0
    def __repr__(self):
        return f"User('{ self.first }','{ self.username }', { self.created }')"

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True )
    title = db.Column(db.String(1000), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created  =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #points  = db.Column(db.Integer, nullable = False, default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')


    def __repr__(self):
       return f"Post('{ self.title }', '{ self.content }','{ self.created }')"


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Eventos(db.Model):
    id = db.Column(db.Integer(),  primary_key = True)
    name = db.Column(db.String(10000), nullable = False)
    descripcion = db.Column(db.String(100000), nullable= False )
    fecha = db.Column(db.DateTime, nullable = False  )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created  =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    archivos = db.relationship('Archivos', backref='author', lazy=True)




    def __repr__(self):
        return f"Eventos('{ self.name }', '{ self.descripcion }', '{ self.fecha }'"

class Archivos(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(500), nullable = False )
    descripcion = db.Column(db.String(500))
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Archivos('{ self.name }', '{ self.descripcion }', '{ self.user_id}'"



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_archivos(form_archivos):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_archivos.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/archivos', picture_fn)
    form_archivos.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_archivos)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/like/<int:post_id>/<action>', methods=['GET', 'POST'])
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/')
@app.route("/registrate", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first = form.first.data, username = form.username.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template ('register.html', form = form )

@app.route("/logineate", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return  redirect(url_for('home'))
    
        else:
            flash(f'Invalid password provided', 'error')
    return render_template ('login.html', form = form )



@app.route("/home", methods = ['GET'])
@login_required
def home():
    return render_template ('home.html' )


@app.route("/posts", methods=["GET", "POST"])
@login_required
def posts():
    form = PostForm()
    all_posts = Post.query.order_by(Post.created.desc())
    if form.validate_on_submit():
        post = Post( title = form.title.data, content = form.content.data,  author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template ('posts.html', all_posts = all_posts,  form = form)

@app.route("/adios")
def adios():
    return render_template('adios.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('adios'))

@app.route("/posts/<int:post_id>/delete", methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect( url_for('posts'))

@app.route("/eventos/<int:evento_id>/delete", methods = ['POST'])
def delete_evento(evento_id):
    eventos = Eventos.query.get(evento_id)
    db.session.delete(eventos)
    db.session.commit()
    return redirect( url_for('eventos'))

@app.route("/cuentas")
@login_required
def cuentas():
    all_cuentas = User.query.all()
    return render_template('cuentas.html', all_cuentas = all_cuentas)

@app.route("/eventos", methods=["GET", "POST"])
@login_required
def eventos():
    form = EventosForm()
    if form.validate_on_submit():
        evento = Eventos(name = form.name.data, descripcion = form.descripcion.data, fecha = form.fecha.data, user = current_user)
        db.session.add(evento)
        db.session.commit()
        return redirect(url_for('archivos'))
    return render_template('eventos.html', form = form)





@app.route("/eventos/eventos_creados")
@login_required
def eventos_creados(): 
    eventos  = Eventos.query.order_by(Eventos.created.desc())
    return render_template('eventos_creados.html', eventos = eventos)

@app.route("/post/<int:post_id>")
def post_unique(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('post_unique.html',  post=post)


@app.route("/eventos/memorias_creadas/<int:evento_id>")
def evento_unique(evento_id):
    eventos = Eventos.query.get_or_404(evento_id)
    all_fotos = url_for('static', filename = 'archivos/')
    return render_template('memorias_unique.html',  eventos = eventos )

@app.route("/cuenta",methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.first= form.first.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first.data = current_user.first
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route('/archivos', methods=['GET', 'POST'])
@login_required
def archivos():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('archivos.html')

    
@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('archivos'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    session.pop('file_urls', None)
    
    return render_template('results.html', file_urls=file_urls)








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)