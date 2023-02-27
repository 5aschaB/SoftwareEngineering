# import SQLAlchemy
from pickle import TRUE
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# create the Flask app
from flask import Flask, make_response, redirect, render_template, request, flash, jsonify
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = Flask(__name__)

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\xda88y\xd8\xb6\x9d\xd3%\xf1\x99^\x12,\x11u\xc7\xb2\xe0\xe18\x97\xf6\x95'

# set up a 'model' for the data you want to store
from db_schema import db, UserAccountTable, projectMetricsTable, subprocessTable, cycleTable, probabilitiesTable, subprocessPredecessorTable, cyclePredecessorTable, dbinit

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = False
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return UserAccountTable.query.get(int(userid))

""" #route to the home
@app.route('/')
def home():
    return render_template('home.html')

#route to login page
@app.route('/login.html')
def login():
    return render_template('login.html')

#route to register page
@app.route('/register.html')
def register():
    return render_template('register.html')

#route to to-do list page
@app.route('/list.html')
@login_required
def list():
    if not current_user.is_authenticated:
        redirect ('/')
    users = User.query.filter(User.id != current_user.id)       # only retrieves users that aren't the current user
    bills = Bills.query.filter_by(user_id=current_user.id)
    items = BillItems.query.join(Bills).filter_by(user_id=current_user.id)
    notifs = Notifications.query.filter_by(user_receiving=current_user.id).first()  # receives notifications for user one at a time
    for bill in bills:
        sum = 0
        for item in items:                  # adds up balance of each item in a bill and assigns total to the bill
            if item.bill_id == bill.id:
                sum = sum + item.balance
        bill.total = sum
    return render_template('list.html', bills=bills, items=items, users=users, notifs=notifs) """

""" #route to create a new list
@app.route('/newbill', methods=['GET','POST'])
def newBill():
    if request.method=="POST":
        billname=request.form['billname']

        db.session.add(Bills(billname,False,0,current_user.id))     # creates new bill row in database
        db.session.commit()
        return redirect('list.html') """

#route to login request
@app.route('/login', methods=['GET','POST'])
def loginRequest():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method=="POST":
        name=request.form['username']
        password=request.form['password']

        #find the users with this name
        user = UserAccountTable.query.filter_by(name=name).first()
        if not user:                                                # flashes message to user if username or password is incorrect
            flash("Incorrect username/password")
            return redirect('login.html')
        if not check_password_hash(user.password, password):        # compares hash of password entered with password hash stored in database
            flash("Incorrect username/password")
            return redirect("login.html")

        login_user(user)                # log in user
        return redirect('list.html')

    if request.method=="GET":
        return render_template('login.html')

#route for registration
@app.route('/registration', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method=="POST":
        name=request.form['username']
        password=request.form['password']
        password2=request.form['password2']
        email=request.form['email']

        #find the users with this name to check if name already exists
        user = UserAccountTable.query.filter_by(name=name).first()
        if user:
            return redirect('register.html')

        #find the users with this email to check if email has already been used
        email = UserAccountTable.query.filter_by(email=email).first()
        if email:
            return redirect('register.html')
            
        new_user = UserAccountTable(name=name, password=generate_password_hash(password), email=email)
        
        #add new user to database
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)        # logs user in straight after registering
        return redirect('list.html')

    if request.method=="GET":
        return render_template('login.html')

#route for logging out
@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/')

""" #route to create a new item and send notification to user
@app.route('/newitem', methods=['GET','POST'])
def newItem():
    if request.method=="POST":
        itemname=request.form['itemname']
        billid=request.form['billid']
        balance=request.form['balance']
        balance=float(balance)
        balance=abs(balance)        # keeps balance positive, even if user enters a negative balance

        db.session.add(BillItems(itemname,0,balance,billid))    # creates new item

        itemname=request.form['itemname']
        billid=request.form['billid']
        userid=request.form['userid']
        balance=request.form['balance']

        bill = Bills.query.filter_by(id=billid).first()
        
        notif = bill.name + ": " + itemname + " - £" + balance      # creates string for notification

        db.session.add(Notifications(notif,False,current_user.id,userid))       # creates new notification for user
        db.session.commit()
        return redirect('list.html')

#route to delete a list item
@app.route('/deleteitem', methods=['GET','POST'])
def deleteItem():
    if request.method=="POST":
        itemid=request.form['itemid']

        item = BillItems.query.filter_by(id=itemid).first()
        db.session.delete(item)                             # delete item from bill

        db.session.commit()
        return redirect('list.html')

#route to complete a bill item
@app.route('/completeitem', methods=['POST'])
def completeItem():
    if request.method=="POST":
        id = request.form['itemid']
        item = BillItems.query.filter_by(id=id).first()
        if item.complete == False:                  # changes state of completion of item when check-box is ticked or unticked
            item.complete = True
            db.session.commit()
        else:
            item.complete = False
            db.session.commit()
        return jsonify({'item': item.content, 'complete' : item.complete})

#route to delete a bill
@app.route('/deletebill', methods=['GET','POST'])
def deleteBill():
    if request.method=="POST":
        billid=request.form['billid']

        qrytext = text("DELETE FROM ITEMS WHERE bill_id=:billid;")              # first delete all items from the bill to be deleted 
        qry = qrytext.bindparams(billid=billid)
        db.session.execute(qry)

        bill = Bills.query.filter_by(id=billid).first()                         # then delete bill
        db.session.delete(bill)

        db.session.commit()
        return redirect('list.html')

#route to complete a bill
@app.route('/completebill', methods=['POST'])
def completeBill():
    if request.method=="POST":
        id = request.form['billid']
        bill = Bills.query.filter_by(id=id).first()
        if bill.complete == False:                      # changes state of completion of bill when check-box is ticked or unticked
            bill.complete = True
            db.session.commit()
        else:
            bill.complete = False
            db.session.commit()
        return jsonify({'item': bill.name, 'complete' : bill.complete})

#route to split bill
@app.route('/split', methods=['POST'])
def split():
    if request.method=="POST":                      # shows balance when evenly split among a number of people
        sum=request.form['sum']
        people=request.form['people']
        split = float(sum)/int(people)

        return jsonify({'sum': sum, 'split' : split})

#route to complete notification
@app.route('/completenotif', methods=['POST'])
def completeNotif():
    if request.method=="POST":
        id=request.form['id']
        sender=request.form['sender']

        notif = Notifications.query.filter_by(id=id).first()
        if notif.complete == False:
            notif.complete = True
            db.session.commit()

            confirm = notif.content + " has been paid for by " + current_user.name          # if notification is ticked, create confirmation notification string

            db.session.add(Notifications(confirm,True,current_user.id,sender))              # create new notification with confirmation string that will show on creator's account
            db.session.commit()

            db.session.delete(notif)                # delete original notification
            db.session.commit()
        else:
            db.session.delete(notif)                # when comfirmation notification ticked by creator, it is just deleted as it has a status of True already
            db.session.commit()
        
        return jsonify({'complete': notif.complete, 'id' : id}) """