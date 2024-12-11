from . import db

class Beverage(db.Model):
    __tablename__='beverages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}, Price: {}\n" 
        str =str.format( self.id, self.name, self.description,self.image, self.price)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('beverage_id',db.Integer,db.ForeignKey('beverages.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'beverage_id') )

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    beverages = db.relationship("Beverage", secondary=orderdetails, backref="orders")
    totalcost = db.Column(db.Float)
    
    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Beverages: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.surname, self.email, self.phone, self.beverages, self.totalcost)
        return str
