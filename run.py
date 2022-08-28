import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Test_data


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context(): # 在藍圖中，要在app.py先建立此shell函式才能在殼層進行操作與測試
    return dict(db=db, User=User, Role=Role, Test_data=Test_data)



if __name__ =="__main__":
    app.run(host='0.0.0.0', port=80, debug=True)