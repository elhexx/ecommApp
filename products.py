from datetime import datetime

from main import db


class Products(db.Model):
    __tablename__ = 'products_table'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    description = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    url = db.Column(db.String)



    def __init__(self, name, price, url, category, stock="stock"):
        self.name = name
        self.price = price
        self.stock = stock
        self.date = datetime.utcnow()
        self.url = url
        self.description = "some dummy descr"
        self.category = category


    def __repr__(self):
        return "<Product(%r, %r, %r)>" % (self.name, self.price, self.stock)



class Product(db.Model):
    __tablename__ = 'product_table'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    description = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    #url = db.Column(db.String, nullable=False)
    #pictures = db.relationship('ProductPictures', backref='product',
    # lazy='dynamic')


    def __init__(self, name, price, url, category, stock="stock"):
        self.name = name
        self.price = price
        self.stock = stock
        self.date = datetime.utcnow()
        #self.url = url
        self.description = "some dummy descr"
        self.category = category


    def __repr__(self):
        return "<Product(%r, %r, %r)>" % (self.name, self.price, self.stock)


## Use to represent the pictures of a product.
class ProductPictures(db.Model):
    __tablename__ = "product_pictures_table"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    #productId = db.Column(db.Integer, db.ForeignKey('product_table.id'))

    def __init__(self, link, productId):
        self.link = link
        self.productId = productId
        self.date = datetime.utcnow()

    def __repr__(self):
        return "<ProductPicures(%r)>" % self.link


## Used to represent the categories that a product can belong
#  to.
class Categories(db.Model):
    __tablename__ = 'categories_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    # If we delete delete all the products in a category, it doesn't
    # make any sense to keep that category available, since there are
    # no products in it.
    available = db.Column(db.Boolean, nullable=True, default=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Categories(%r)" % self.name

def createProduct(name, price, url, category):
    db.create_all()
    product = Products(name, price, url, category)
    db.session.add(product)
    db.session.commit()

def getProducts():
    products = Products.query.all()
    return products

def getProduct_byID(id):
    product = Products.query.filter_by(id=id).first()
    return product