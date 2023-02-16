from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# create the database interface
db = SQLAlchemy()

# a model of a user for the database
class UserAccountTable(UserMixin, db.Model):
    __tablename__='user_account_table'
    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    passwordHash = db.Column(db.String(250))
    confirmationToken = db.Column(db.String(100))
    tokenGenerationTime = db.Column(db.DateTime)
    emailVerificationStatus = db.Column(db.Boolean, default=False)
    passwordRecoveryToken = db.Column(db.String(100))
    recoveryTokenTime = db.Column(db.DateTime)
    roleType = db.Column(db.String(15))

    def __init__(self, email, passwordHash, confirmationToken, tokenGenerationTime, emailVerificationStatus, passwordRecoveryToken, recoveryTokenTime, roleType):
        self.email=email
        self.passwordHash=passwordHash
        self.confirmationToken=confirmationToken
        self.tokenGenerationTime=tokenGenerationTime
        self.emailVerificationStatus=emailVerificationStatus
        self.passwordRecoveryToken=passwordRecoveryToken
        self.recoveryTokenTime=recoveryTokenTime
        self.roleType=roleType


# a model of a bill for the database
# it refers to a user and a category
class projectMetricsTable(db.Model):
    __tablename__='project_metrics_table'
    projectid = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    completeness = db.Column(db.Integer)
    teamSize = db.Column(db.Integer)
    teamMorale = db.Column(db.Integer)
    teamWellness = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('user_account_table.id'))

    def __init__(self, projectid, budget, deadline, completeness, teamSize, teamMorale, teamWellness, userid):
        self.projectid=projectid
        self.budget=budget
        self.deadline=deadline
        self.completeness=completeness
        self.teamSize=teamSize
        self.teamMorale=teamMorale
        self.teamWellness=teamWellness
        self.userid=userid

# a model of a bill item for the database
# it refers to a bill
class subprocessTable(db.Model):
    __tablename__='subprocess_table'
    subprocessid = db.Column(db.Integer, primary_key=True)
    subprocessName = db.Column(db.String(100))
    cycleid = db.Column(db.Integer, db.ForeignKey('cycle_table'))
    employeesRequired = db.Column(db.Integer, nullable=False)
    costPerUnitTime = db.Column(db.Float)
    completeness = db.Column(db.Integer)

    def __init__(self, subprocessName, cycleid, employeesRequired, costPerUnitTime, completeness):
        self.subprocessName=subprocessName
        self.cycleid=cycleid
        self.employeesRequired=employeesRequired
        self.costPerUnitTime=costPerUnitTime
        self.completeness=completeness

# a model of a notification for the database
class cycleTable(db.Model):
    __tablename__='cycle_table'
    cycleid = db.Column(db.Integer, primary_key=True)
    cycleRepeats = db.Column(db.Integer)
    projectid = db.Column(db.Integer, db.ForeignKey('project_metrics_table'))

    def __init__(self, cycleRepeats, projectid):
        self.cycleRepeats=cycleRepeats
        self.projectid=projectid

class probabilitiesTable(db.Model):
    __tablename__='probabilities_table'
    subprocessid = db.Column(db.Integer, db.ForeignKey('subprocess_table'))
    timeframe = db.Column(db.Integer, nullable=False)
    probability = db.Column(db.Float, nullable=False)

    def __init__(self, subprocessid, timeframe, probability):
        self.subprocessid=subprocessid
        self.timeframe=timeframe
        self.probability=probability

class subprocessPredecessorTable(db.Model):
    __tablename__='subprocess_predecessor_table'
    subprocessBefore = db.Column(db.Integer, primary_key=True)
    subprocessAfter = db.Column(db.Integer, primary_key=True)

class cyclePredecessorTable(db.Model):
    __tablename__='cycle_predecessor_table'
    cycleBefore = db.Column(db.Integer, primary_key=True)
    cycleAfter = db.Column(db.Integer, primary_key=True)

""" # put some data into the tables
def dbinit():
    user_list = [
        User("Peter", "pbkdf2:sha256:260000$nTUCH94BQfvpuJZY$d406273466c633d0e15646a3995c05675727289866a36e950202f3e978b3b367", "peter@email.com"), 
        User("Petra", "pbkdf2:sha256:260000$6MqlJowMt15iuxPq$1f2ede1e998885dde713bcb1031b02a1ae5430cbd35eb97f1441c251eee507fc", "petra@email.com")
        ]
    db.session.add_all(user_list)

    # find the id of the user Peter and Petra
    peter_id = User.query.filter_by(name="Peter").first().id
    petra_id = User.query.filter_by(name="Petra").first().id

    all_bills = [
        Bills("Nandos",False,13.4,peter_id), 
        Bills("House",False,213.66,peter_id),
        Bills("Uber",False,22.21,petra_id)
        ]
    db.session.add_all(all_bills)

    nandos_id = Bills.query.filter_by(name="Nandos").first().id
    house_id = Bills.query.filter_by(name="House").first().id
    uber_id = Bills.query.filter_by(name="Uber").first().id

    all_items = [
        BillItems("Water",False,60.0,house_id),
        BillItems("Electricity",True,80.47,house_id),
        BillItems("Gas",False,73.19,house_id),
        BillItems("4 Chicken Wings",False,8.4,nandos_id), 
        BillItems("2 Chips",True,5.0,nandos_id),
        BillItems("Trip to London",True,5.76,uber_id),
        BillItems("Trip home from London",False,16.45,uber_id)
        ]
    db.session.add_all(all_items)

    # commit all the changes to the database file
    db.session.commit() """
