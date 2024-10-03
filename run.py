from app import create_app

app = create_app()

@app.after_request
def nosniffSecurity(response):
    """
    This will add the noSniff header to all response right before it gets sent
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
