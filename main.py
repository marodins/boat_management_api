from portfolio_api.app import app_create


app = app_create()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

    