from flask import Flask

app = Flask(__name__)


@app.route('/Ss')
def support_system():
    return 'Support_System.html'


if __name__ == '__main__':
    app.run()


