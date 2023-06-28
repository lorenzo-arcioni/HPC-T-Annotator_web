from flask import Flask, request, send_file, render_template
from creator import *
import random
import string
import os
import subprocess as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        tmp_dir = 'tmp_' + ''.join(random.choices(string.ascii_lowercase, k=10))
        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        wlm = request.form['workload'].lower()

        if wlm == 'slurm':
            account_name = request.form['Slurm_account_name']
            serial_part = request.form['Slurm_serial_part']
            parallel_part = request.form['Slurm_parallel_part']
            process = request.form['Slurm_Nproces']
            threads = request.form['Slurm_Nthread']
            Time = request.form['Time']
            Mprocess = request.form['Mproces']

        elif wlm == 'htcondor':
            pass
        else:
            pass

        diamond = 1 if request.form['annotation_software'] == 'Diamond' else 0
        tool = request.form['tool']
        database = request.form['DB_path']
        inputfile = request.form['IF_path']
        outformat = request.form['outformat']
        binary = request.form['BI_path']

        # python3 creator.py -p $processes -i "$inputfile" -f "$outfmt" -T $tool -t $threads -d "$database" -b "$binary" -w "$wlm" -D $diamond

        sp.call("python3 creator.py -p {} -i {} -f {} -T {} -t {} -d {} -b {} -w {} -D {}".format(process, inputfile, outformat, tool, threads, database, binary, wlm, diamond), shell=True)
        

        return send_file('./read.py', as_attachment=True)

    return open("index.html", "r").read()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

