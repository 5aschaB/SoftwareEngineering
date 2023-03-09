from datetime import datetime

from flask_login import UserMixin

from src import bcrypt, db


# a model of a user account for the database
class UserAccountTable(UserMixin, db.Model):
    __tablename__='user_account_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    tokenGenerationTime = db.Column(db.DateTime, nullable=False)
    emailVerificationStatus = db.Column(db.Boolean, default=False)
    emailVerifiedTime = db.Column(db.DateTime)
    roleType = db.Column(db.String(15), nullable=False)
    is_admin = is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, tokenGenerationTime, emailVerificationStatus, emailVerifiedTime, roleType, is_admin):
        self.email=email
        self.password=bcrypt.generate_password_hash(password)
        self.tokenGenerationTime=tokenGenerationTime
        self.emailVerificationStatus=emailVerificationStatus
        self.emailVerifiedTime=emailVerifiedTime
        self.roleType=roleType
        self.is_admin = is_admin


# a model of project metrics for the database
class projectMetricsTable(db.Model):
    __tablename__='project_metrics_table'
    projectid = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer, db.CheckConstraint('budget>1 AND budget<11'))
    deadline = db.Column(db.DateTime)
    completeness = db.Column(db.Integer, db.CheckConstraint('completeness>1 AND completeness<11'))
    teamSize = db.Column(db.Integer, db.CheckConstraint('teamSize>1 AND teamSize<11'))
    teamMorale = db.Column(db.Integer, db.CheckConstraint('teamMorale>1 AND teamMorale<11'))
    teamWellness = db.Column(db.Integer, db.CheckConstraint('teamWellness>1 AND teamWellness<11'))
    timeframe = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('user_account_table.id'))

    def __init__(self, budget, deadline, completeness, teamSize, teamMorale, teamWellness, timeframe, userid):
        self.budget=budget
        self.deadline=deadline
        self.completeness=completeness
        self.teamSize=teamSize
        self.teamMorale=teamMorale
        self.teamWellness=teamWellness
        self.timeframe=timeframe
        self.userid=userid

# a model of subprocesses for the database
class subprocessTable(db.Model):
    __tablename__='subprocess_table'
    subprocessid = db.Column(db.Integer, primary_key=True)
    subprocessName = db.Column(db.String(100))
    cycleid = db.Column(db.Integer, db.ForeignKey('cycle_table.cycleid'))
    employeesRequired = db.Column(db.Integer, nullable=False)
    costPerUnitTime = db.Column(db.Float)
    completeness = db.Column(db.Integer)

    def __init__(self, subprocessName, cycleid, employeesRequired, costPerUnitTime, completeness):
        self.subprocessName=subprocessName
        self.cycleid=cycleid
        self.employeesRequired=employeesRequired
        self.costPerUnitTime=costPerUnitTime
        self.completeness=completeness

# a model of a cycle for the database
class cycleTable(db.Model):
    __tablename__='cycle_table'
    cycleid = db.Column(db.Integer, primary_key=True)
    cycleRepeats = db.Column(db.Integer)
    projectid = db.Column(db.Integer, db.ForeignKey('project_metrics_table.projectid'))

    def __init__(self, cycleRepeats, projectid):
        self.cycleRepeats=cycleRepeats
        self.projectid=projectid

# a model of probabilities for the database
class probabilitiesTable(db.Model):
    __tablename__='probabilities_table'
    probabilityid = db.Column(db.Integer, primary_key=True)
    subprocessid = db.Column(db.Integer, db.ForeignKey('subprocess_table.subprocessid'))
    timeframe = db.Column(db.Integer, db.ForeignKey('project_metrics_table.timeframe'))
    probability = db.Column(db.Float, nullable=False)

    def __init__(self, subprocessid, timeframe, probability):
        self.subprocessid=subprocessid
        self.timeframe=timeframe
        self.probability=probability

# a model of a subprocess's predecessor for the database
class subprocessPredecessorTable(db.Model):
    __tablename__='subprocess_predecessor_table'
    subprocessBefore = db.Column(db.Integer, primary_key=True)
    subprocessAfter = db.Column(db.Integer, primary_key=True)

# a model of a cycle's predecessor for the database
class cyclePredecessorTable(db.Model):
    __tablename__='cycle_predecessor_table'
    cycleBefore = db.Column(db.Integer, primary_key=True)
    cycleAfter = db.Column(db.Integer, primary_key=True)

# a model of git commits for the database
class gitCommitsTable(db.Model):
    __tablename__='git_commits_table'
    commitid = db.Column(db.Integer, primary_key=True)
    projectid = db.Column(db.Integer, db.ForeignKey('project_metrics_table.projectid'))
    timeframe = db.Column(db.Integer, db.ForeignKey('project_metrics_table.timeframe'))
    numOfCommits = db.Column(db.Integer)
    repoName = db.Column(db.String(100))

    def __init__(self, projectid, timeframe, numOfCommits, repoName):
        self.projectid=projectid
        self.timeframe=timeframe
        self.numOfCommits=numOfCommits
        self.repoName=repoName