from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    headlines = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Note(sno={self.sno}-{str(self.headlines)}"



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        headlines = request.form['headlines']
        description = request.form['description']
        note = Note(headlines=headlines, description=description, date=datetime.utcnow())
        db.session.add(note)
        db.session.commit()
    allNotes = Note.query.all()
    return render_template('index.html', allNotes=allNotes)

@app.route('/delete/<int:sno>')
def delete(sno):
    note = Note.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

# if __name__ == '__main__':
#     app.run(port=5000, host="0.0.0.0")
