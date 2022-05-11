import db
for x in db.get_all_app():
    db.run_in_app(x)
