from app import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

with app.app_context():
    db.drop_all()
    db.create_all()