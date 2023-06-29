from flask import Flask, request, send_file, render_template
from creator import *
import random
import string
import os
import subprocess as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    def fill_startbase(data_dic):
        """
        Fills the start base of the process with the given parameters.
        
        Parameters:
        - processes: The number of processes to be used.
        - threads: The number of threads to be used.
        - inputfile: The input file to be processed.
        - outformat: The output format of the process.
        - diamond: The diamond parameter of the process.
        - tool: The tool to be used in the process.
        - binary: The binary file to be used in the process.
        - database: The database for the process.
        - wlm: The workload manager for the process.
        """

        # Open the start.sh file in write mode
        with open("./start.sh", "w") as start:
            
            # Write the shebang line
            start.write("#!/bin/bash" + '\n\n')

            if data_dic['wlm'] == 'slurm':

                start.write("SBATCH --job-name=PA_proc_start" + '\n')
                start.write("SBATCH --output=general.out" + '\n')
                start.write("SBATCH --error=general.err" + '\n')
                start.write("#SBATCH --nodes=1" + '\n')
                start.write("#SBATCH --ntasks=1" + '\n')
                start.write("#SBATCH --cpus-per-task=1" + '\n')
                start.write("#SBATCH --mem=10GB" + '\n')
                start.write("#SBATCH --time=04:00:00" + '\n')
                start.write("#SBATCH --partition=" + data_dic['serial_part'] + '\n\n')
                start.write(""" inputfile="{}"
                                processes={}
                                threads={}
                                outformat={}
                                diamond={}
                                tool="{}"
                                binary="{}"
                                database="{}
                            """.format(data_dic['inputfile'], 
                                       data_dic['processes'], 
                                       data_dic['threads'], 
                                       data_dic['outformat'], 
                                       data_dic['diamond'], 
                                       data_dic['tool'], 
                                       data_dic['binary'], 
                                       data_dic['database']).replace("\t", ""))
            start.close()

    def fill_readbase(data_dic):
        """
        Fills the read base of the process with the given parameters.
        
        Parameters:
        - processes: The number of processes to be used.
        - threads: The number of threads to be used.
        - inputfile: The input file to be processed.
        - outformat: The output format of the process.
        - diamond: The diamond parameter of the process.
        - tool: The tool to be used in the process.
        - binary: The binary file to be used in the process.
        - database: The database for the process.
        - wlm: The workload manager for the process.
        """

        pass

    if request.method == 'POST':

        tmp_dir = 'tmp_' + ''.join(random.choices(string.ascii_lowercase, k=10))
        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        data_dic = dict()

        data_dic['wlm'] = request.form['workload'].lower()

        if wlm == 'slurm':
            data_dic['account_name'] = request.form['Slurm_account_name']
            data_dic['serial_part'] = request.form['Slurm_serial_part']
            data_dic['parallel_part'] = request.form['Slurm_parallel_part']
            data_dic['process'] = request.form['Slurm_Nproces']
            data_dic['threads'] = request.form['Slurm_Nthread']
            data_dic['time'] = request.form['Time']
            data_dic['memory_per_process'] = request.form['Mproces']

        elif wlm == 'htcondor':
            pass
        else:
            pass

        data_dic['diamond'] = 1 if request.form['annotation_software'] == 'Diamond' else 0
        data_dic['tool'] = request.form['tool']
        data_dic['database'] = request.form['DB_path']
        data_dic['inputfile'] = request.form['IF_path']
        data_dic['outformat'] = request.form['outformat']
        data_dic['binary'] = request.form['BI_path']

        # python3 creator.py -p $processes -i "$inputfile" -f "$outfmt" -T $tool -t $threads -d "$database" -b "$binary" -w "$wlm" -D $diamond

        fill_startbase(data_dic)

        #sp.call("python3 creator.py -p {} -i {} -f {} -T {} -t {} -d {} -b {} -w {} -D {}".format(process, inputfile, outformat, tool, threads, database, binary, wlm, diamond), shell=True)

        #sp.call("tar -xzf hpc-annotator.tar.gz read.py start.sh control_script.sh", shell=True)
        

        return send_file('./start.sh', as_attachment=True)

    return open("index.html", "r").read()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

