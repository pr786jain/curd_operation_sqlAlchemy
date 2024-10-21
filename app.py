from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Flask app and database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model definition
class Todo(db.Model):  
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Routes
@app.route('/' , methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is product page'

@app.route('/delete/<int:sno>')
def delete(sno):  # Add sno as a function argument
    todo = Todo.query.filter_by(sno=sno).first()  # Fetch the actual Todo instance
    if todo:
        db.session.delete(todo)  # Delete the found todo instance
        db.session.commit()  # Commit the changes to the database
    return redirect('/')

@app.route('/update/<int:sno>' , methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
       title=request.form['title']
       desc= request.form['desc']
       todo = Todo.query.filter_by(sno=sno).first()
       db.session.add(todo)
       db.session.commit()
       return redirect('/')
       
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


# Main entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created within the app context
        print("Tables created successfully!")  # Confirm table creation
    
    app.run(debug=True)
