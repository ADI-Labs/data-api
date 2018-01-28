# from click import echo
from flask import Flask, render_template, current_app
# from unittest import TestLoader, TextTestRunner
# from tests.test_basics_app import BasicsTest

app = Flask(__name__)


# @app.cli.command()
# def test():
#     echo("Testing...")
#     suite = TestLoader().loadTestsFromTestCase(BasicsTest)
#     TextTestRunner().run(suite)


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
