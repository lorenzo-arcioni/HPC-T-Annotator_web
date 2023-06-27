from flask import Flask, request, send_file, render_template
from creator import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wlm = request.form['workload']

        if wlm == 'Slurm':
            account_name = request.form['Slurm_account_name']
            serial_part = request.form['Slurm_serial_part']
            parallel_part = request.form['Slurm_parallel_part']
            Nproces = request.form['Slurm_Nproces']
            Nthread = request.form['Slurm_Nthread']
            Time = request.form['Time']
            Mproces = request.form['Mproces']

        elif wlm == 'HTCondor':
            pass
        else:
            pass

        diamond = 1 if request.form['annotation_software'] == 'Diamond' else 0
        tool = request.form['tool']
        database = request.form['DB_path']
        inputfile = request.form['IF_path']
        outformat = request.form['outformat']
        binary = request.form['BI_path']

        fill_readbase(processes, threads, inputfile, outformat, diamond, tool, binary, database)
        

        return send_file('./read.py', as_attachment=True)

    return open("index.html", "r").read()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

