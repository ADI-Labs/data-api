from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/docs/Documentation')
def main():
    return render_template("index.html")

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/housing')
def housing():
    return render_template('housing.html')

@app.route('/dining')
def dining():
    return render_template('dining.html')

if __name__ == '__main__':
    app.run()
