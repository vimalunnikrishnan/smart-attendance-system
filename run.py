from app import create_app, db   # ✅ import db also

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)