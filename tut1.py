from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/about")
def hello():
    name= "Rishabh"
    return render_template('about.html',name1=name)

app.run(debug=True)