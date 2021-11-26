from app import create_app

app_obj = create_app()

if __name__ == '__main__':
    app_obj.run(debug=True)
