from flask import Flask, request, send_file, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wlm = request.form['workload']
        contenuto = f"Il nome inserito è: {wlm}"
        with open('file.txt', 'w') as f:
            f.write(contenuto)
        return send_file('file.txt', as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

