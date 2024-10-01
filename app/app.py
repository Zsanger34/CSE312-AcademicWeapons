from flask import Flask, render_template

app = Flask(__name__)

# Serve the root path with the index.html
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
