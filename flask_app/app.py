from flask import Flask
from views.main_views import main_bp
from views.result_views import result_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    app.run(debug=True)