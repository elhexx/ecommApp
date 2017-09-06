from flask import flash
from flask import render_template, jsonify
from flask import request
from flask import session, redirect, url_for
from passlib.handlers.sha2_crypt import sha256_crypt
from main import app
from forms import RegistrationForm, AddNewProductForm
from models import createUser, getUsers, getUser

from products import createProduct, getProducts, getProduct_byID


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#************************************************************************
"""
from flask_uploads import IMAGES, UploadSet, configure_uploads

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

upld_tmplt ='''
<html>
<head>
	<title>Upload</title>
</head>
<body>
<form method=POST enctype=multipart/form-data action="/addProduct">
    <input type=file name=photo>
    <input type="submit">
</form>
</body>
</html>''' """


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = str(request.form['password'])
        user = getUser(username)
        if user:
            if sha256_crypt.verify(password, str(user.password)):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
            else :
                return render_template('login.html', msg="incorrect password")
        else :
            return render_template('login.html', msg="user not found")


    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        #if form.validate_on_submit():
        fname= form.fname.data
        lname= form.lname.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt((str(form.password.data)))
        createUser(fname, lname, username, email, password)
        return "success"
        #else :
         #   return render_template('register.html', msg= form.errors, form = form)

@app.route('/logout')
def logout():
    session.clear()
    flash('you are logged out', 'success')
    return redirect(url_for('login'))

@app.route('/get')
def get():
    users = getUsers()
    return jsonify(users)

@app.route('/store')
def store():
    products = getProducts()

    return render_template('store.html', products = products)

@app.route('/store/products/<int:id>')
def product(id):
    product = getProduct_byID(id)
    return render_template('product.html', product=product)


@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    form = AddNewProductForm()
    if request.method == "POST" :
        name = request.form['pname']
        category = request.form['category']
        price = request.form['price']

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            createProduct(name, price, url, category)
            return redirect(url_for('addProduct', msg="success"))
    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    return render_template('addProducet.html', form=form)