from flask import Flask
from routes.callback import callback_route
from config.config import Config


app = Flask(__name__)
app.config.from_object(Config)


# 註冊路由
app.register_blueprint(callback_route)

if __name__ == "__main__":
    app.run(debug=Config.DEBUG, port=Config.PORT)