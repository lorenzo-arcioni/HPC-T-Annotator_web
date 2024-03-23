from app import app
from flask import Flask, request, send_file, render_template
import random
import string
import os
import subprocess as sp
import shutil as sh
import time

@app.route("/index.html", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():

    # Use os.getenv("key") to get environment variables
    app_name = os.getenv("APP_NAME")

    if app_name:
        #return open("./app/html/index.html", "r").read()
        return render_template('index.html')

    return "Hello from Flask"

@app.route('/contacts.html')
def contacts():
    # Contacts page
    return render_template("contacts.html")

@app.route('/help.html')
def help():
    # Help page
    return render_template("help.html")

@app.route('/start.html', methods=['GET', 'POST'])
def start():
    # Start page

    def fill_startbase(data_dic):

        # Open the start.sh file in write mode
        with open("./start.sh", "w") as start:
            
            # Write the shebang line
            start.write("#!/bin/bash" + '\n\n')

            if data_dic['wlm'] == 'slurm':

                start.write("#SBATCH --job-name=PA_proc_start" + '\n')
                start.write("#SBATCH --output=general.out" + '\n')
                start.write("#SBATCH --error=general.err" + '\n')
                start.write("#SBATCH --nodes=1" + '\n')
                start.write("#SBATCH --ntasks=1" + '\n')
                start.write("#SBATCH --cpus-per-task=1" + '\n')
                start.write("#SBATCH --mem=5GB" + '\n')
                start.write("#SBATCH --time=01:00:00" + '\n')
                start.write("#SBATCH --partition=" + data_dic['serial_part'] + '\n\n')
                start.write(open("../bases/start_base.txt").read().format(data_dic['inputfile'], 
                                                                        data_dic['processes'], 
                                                                        data_dic['threads'], 
                                                                        data_dic['outformat'], 
                                                                        data_dic['diamond'], 
                                                                        data_dic['tool'], 
                                                                        data_dic['binary'], 
                                                                        data_dic['database']))
            elif data_dic['wlm'] == 'htcondor':
                pass

            elif data_dic['wlm'] == 'None':
                start.write(open("../bases/start_base.txt").read().format(data_dic['inputfile'], 
                                                                        data_dic['processes'], 
                                                                        data_dic['threads'], 
                                                                        data_dic['outformat'], 
                                                                        data_dic['diamond'], 
                                                                        data_dic['tool'], 
                                                                        data_dic['binary'], 
                                                                        data_dic['database']))
            start.close()

    def fill_readbase(data_dic):

        wlm_header = ""

        if data_dic['wlm'] == 'slurm':

            wlm_header =  "#SBATCH --account=" + data_dic['account_name'] + '\n' \
                        + "#SBATCH --partition=" + data_dic['parallel_part'] + '\n' \
                        + "#SBATCH --nodes=1" + '\n' \
                        + "#SBATCH --ntasks-per-node=1" + '\n' \
                        + "#SBATCH --time=" + data_dic['time'] + ":00:00" + '\n' \
                        + "#SBATCH --mem=" + data_dic['memory_per_process'] + 'GB' + '\n' \
                        + "#SBATCH --output=general.out" + '\n' \
                        + "#SBATCH --error=general.err" + '\n'
            
        elif data_dic['wlm'] == 'htcondor':
            pass

        elif data_dic['wlm'] == 'None':
            pass
        
        with open("./read.py", 'w') as read:

            if not (data_dic['outformat'].endswith("\"") and data_dic['outformat'].startswith("\"")):
                data_dic['outformat'] = "\"" + data_dic['outformat'] + "\""

            read.write(open("../bases/read_base.txt").read().format(data_dic["outformat"],
                                                                    data_dic["diamond"],
                                                                    data_dic["binary"],
                                                                    data_dic["database"],
                                                                    data_dic["tool"],
                                                                    data_dic["threads"],
                                                                    data_dic["processes"],
                                                                    data_dic["wlm"],
                                                                    wlm_header.replace("\n", "\\n"),
                                                                    data_dic['add_options'],
                                                                    data_dic['add_options'],
                                                                   ))
            read.close()
    
    def fill_controlscriptbase(data_dic):

        # Open the control_script.sh file in write mode
        with open("./control_script.sh", "w") as control:
            # Write the shebang line
            control.write("#!/bin/bash\n\n")

            if data_dic['wlm'] == 'slurm':
                
                control.write("#SBATCH --job-name=PA_proc-control" + '\n')
                control.write("#SBATCH --output=control.out" + '\n')
                control.write("#SBATCH --error=control.err" + '\n')
                control.write("#SBATCH --nodes=1" + '\n')
                control.write("#SBATCH --ntasks=1" + '\n')
                control.write("#SBATCH --cpus-per-task=1" + '\n')
                control.write("#SBATCH --mem=8GB" + '\n')
                control.write("#SBATCH --time=02:00:00" + '\n')
                control.write("#SBATCH --partition=" + data_dic['serial_part'] + '\n\n')

                # Open the controlscript_base.txt file in read mode
                with open("../bases/controlscript_base.txt", "r") as f:
                    # Read the contents of controlscript_base.txt and format it with "sbatch"
                    base = f.read().format("#If my running time > 1 hours\n"+
	                                       "        if [ $(( end_time - start_time )) -gt 3600 ]\n"+
                                           "        then\n"+
                                           "        #Launch my clone\n"+
                                           "            sbatch ./control_script.sh\n"+
                                           "            exit 0\n"+
                                           "        fi\n\n")
                    # Write the formatted contents to control_script.sh
                    control.write(base)
                    f.close()
            
            elif data_dic['wlm'] == 'htcondor':
                pass

            else:
                # Open the controlscript_base.txt file in read mode
                with open("../bases/controlscript_base.txt", "r") as f:
                    # Read the contents of controlscript_base.txt and format it with "bash"
                    base = f.read().format("")
                    # Write the formatted contents to control_script.sh
                    control.write(base)
                    f.close()

            control.close()


    if request.method == 'POST':
        
        tmp_dir = 'tmp_' + ''.join(random.choices(string.ascii_lowercase, k=10))

        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        data_dic = dict()
        
        data_dic['tmp_system_path'] = tmp_dir
        
        
        data_dic['wlm'] = request.form.get('workload_manager').lower()
        
        if data_dic['wlm'] == 'slurm':
            data_dic['account_name'] = request.form.get('Slurm_account_name')
            data_dic['serial_part'] = request.form.get('Slurm_serial_part')
            data_dic['parallel_part'] = request.form.get('Slurm_parallel_part')
            data_dic['processes'] = request.form.get('Slurm_Nprocess')
            data_dic['threads'] = request.form.get('Slurm_Nthreads')
            data_dic['time'] = request.form.get('Slurm_time')
            data_dic['memory_per_process'] = request.form.get('Slurm_Mprocess')

        elif data_dic['wlm'] == 'htcondor':
            pass
        else:
            data_dic['wlm'] = 'None'
            data_dic['processes'] = request.form.get('Nprocess')
            data_dic['threads'] = request.form.get('threads')
        
        data_dic['diamond'] = 1 if request.form.get('annotation_software') == 'diamond' else 0
        data_dic['tool'] = request.form.get('tool')
        data_dic['database'] = request.form.get('DB_path')
        data_dic['inputfile'] = request.form.get('IF_path')
        data_dic['outformat'] = request.form.get('outformat')
        data_dic['binary'] = request.form.get('BI_path')
        data_dic['add_options'] = request.form.get('add_options')
        
        
        fill_startbase(data_dic)
        fill_readbase(data_dic)
        fill_controlscriptbase(data_dic)

        sp.run("chmod +x start.sh && chmod +x read.py && chmod +x control_script.sh", shell=True)
        sp.run("cp ../time_calculator.py .", shell=True)
        sp.run("cp ../splitter.py .", shell=True)

        tar_name = "hpc-t-annotator_" +  time.strftime("%Y.%m.%d-%H.%M.%S") + ".tar"

        sp.run(f"tar -cf {tar_name} read.py start.sh control_script.sh time_calculator.py splitter.py", shell=True)

        tar = open(f"./{tar_name}", "r")
        tar.seek(0)

        os.chdir("../")
        sh.rmtree(tmp_dir)

        return send_file(tar, as_attachment=True, attachment_filename=tar_name, mimetype='text/plain')
    
    return render_template("start.html")

@app.route('/architecture.html')
def architecture():
    # Help page
    return render_template("architecture.html")


@app.route('/download.html')
def download():
    # Help page
    return render_template("download.html")
