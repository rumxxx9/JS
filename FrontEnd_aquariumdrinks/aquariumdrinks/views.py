from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Beverage, Order
from .forms import CheckoutForm
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/beverages')
def beverages():
    beverages = Beverage.query.order_by(Beverage.name).all()
    return render_template('beverages.html', beverages=beverages)


@bp.route('/beverages_view')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    beverages = Beverage.query.filter(Beverage.description.like(search)).all()
    return render_template('beverages.html', beverages = beverages)


@bp.route('/order', methods=['POST','GET'])
def order():
    beverage_id = request.values.get('beverage_id')

    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None
    
    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None

    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for beverage in order.beverages:
            totalprice = totalprice + beverage.price
    
    if beverage_id is not None and order is not None:
        beverage = Beverage.query.get(beverage_id)
        if beverage not in order.beverages:
            try:
                order.beverages.append(beverage)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order=order, totalprice=totalprice)


@bp.route('/deleteorder/')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))


@bp.route('/deleteorderitem/', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        beverage_to_delete = Beverage.query.get(id)
        try:
            order.beverages.remove(beverage_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))


@bp.route('/checkout/', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for beverage in order.beverages:
                totalcost = totalcost + beverage.price
            order.totalcost = totalcost
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.index'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form = form)