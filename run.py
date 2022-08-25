import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')




if __name__ =="__main__":
    app.run(debug=True)