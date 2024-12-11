from flask import Blueprint
from . import db
from .models import Beverage, Order

bp = Blueprint('admin', __name__, url_prefix='/admin/')

@bp.route('/dbseed/')
def dbseed():
    b1 = Beverage(id=1, name='Flavour of Shanghai', description='A light soda contains four different ingredients, includes ginger, lime, lemongrass, and pineapple.', image='shdrink.jpg', price=36.50)
    b2 = Beverage(id=2, name='Flavour of London', description='A mixed tea beverage contains two different ingredients, includes black tea and milk.', image='fldrink.jpg', price=36.50)
    b3 = Beverage(id=3, name='Flavour of ChiangMai', description='A fruit combination flavoured sparkling beverage unique to Southeast Asia.', image='cmdrink.jpg', price=36.50)
    b4 = Beverage(id=4, name='Flavour of Okinawa', description='Out Of Stock', image='jpdrink.jpg', price=36.50)
    
    try:
        db.session.add(b1)
        db.session.add(b2)
        db.session.add(b3)
        db.session.add(b4)
        db.session.commit()

    except:
        return 'There was an issue adding a item in dbseed function'

    return 'DATA LOADED'