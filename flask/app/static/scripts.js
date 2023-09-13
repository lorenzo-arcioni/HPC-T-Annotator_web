document.addEventListener("DOMContentLoaded", function () {
    initPage();
});

function initPage() {
    toggleConfigurationPanel();

    // Verifica se l'elemento con l'id "sub_B" esiste prima di aggiungere l'event listener
    var sub_B_v = document.getElementById("sub_B");
    if (sub_B_v) {
        sub_B_v.addEventListener("click", validateForm);
    }

    // Esegui una verifica simile per gli altri elementi
    var help_add_options_v = document.getElementById("help_add_options");
    if (help_add_options_v) {
        help_add_options_v.addEventListener("click", help_add_options);
    }

    var help_outfmt_v = document.getElementById("help_outfmt");
    if (help_outfmt_v) {
        help_outfmt_v.addEventListener("click", help_outfmt);
    }

    var help_db_path_v = document.getElementById("help_db_path");
    if (help_db_path_v) {
        help_db_path_v.addEventListener("click", help_db_path);
    }

    var help_alignment_v = document.getElementById("help_alignment");
    if (help_alignment_v) {
        help_alignment_v.addEventListener("click", help_alignment);
    }

    var help_workload_v = document.getElementById("help_workload");
    if (help_workload_v) {
        help_workload_v.addEventListener("click", help_workload);
    }
}

function toggleConfigurationPanel() {
    var slurmConfPanel = document.getElementById("slurmConfPanel");
    var noneConfPanel = document.getElementById("noneConfPanel");

    var slurmRadio = document.getElementById("slurm");
    var noneRadio = document.getElementById("none");

    if (slurmRadio && slurmRadio.checked) {
        slurmConfPanel.style.display = "block";
        noneConfPanel.style.display = "none";
    } else if (noneRadio && noneRadio.checked) {
        slurmConfPanel.style.display = "none";
        noneConfPanel.style.display = "block";
    }
}
// Check if all fields are filled
function validateForm(){
    var form = document.querySelector("form");
    var inputs = form.querySelectorAll("input, select");
    var isValid = true;

    for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];

        if (input.offsetParent !== null && input.value.trim() === "" && input.id !== "add_options"){
            isValid = false;
            input.style.backgroundColor = "#BDBDBD";
        }
        else{
            input.style.backgroundColor = ""
        }
    }

    if (!isValid){
        event.preventDefault();
        window.alert("Please fill all field!");
        exit(0)
    }
    // Check if the outformat has the correct format with double quotes
    var outformatInput = document.getElementById("outformat");

    if (!outformatInput.value.match('\".*6.*\"')){
        isValid = false;
        outformatInput.style.backgroundColor = "#BDBDBD";
    } else {
        outformatInput.style.backgroundColor = "";
    }

    if (!isValid){
        event.preventDefault();
        window.alert("There is an error in the outformat.\nRemember the double quotes and the correct spaces.");
        exit(0);
    }

    // Check if the outformat has the correct format with double quotes
    var add_options = document.getElementById("add_options");

    if (add_options.value.match('.*-num_threads.*') || add_options.value.match('.*-p .*') || add_options.value.match('.*-o .*') || add_options.value.match('.*-out .*')){
        isValid = false;
        add_options.style.backgroundColor = "#BDBDBD";
    } else {
        add_options.style.backgroundColor = "";
    }

    if (!isValid){
        event.preventDefault();
        window.alert("There is an error in the additional options.\nRemember that -p, -o, -num_threads and -out options are not allowed.");
        exit(0);
    }
}

function help_add_options(){
    window.alert("In note, only options related to computation are accepted; options indicating the usage of threads and input/output file names are not accepted. So the options -p and -o for diamond or -out and -num_threads for blast are not accepted! \
                \n\n For example, you can specify parameters like \n\n  -evalue 1e-5 -max_target_seqs 10 \n\nfor a BLAST execution or \n\n  --ultra-sensitive -k 10 \n\nfor Diamond execution.");
}
function help_db_path(){
    window.alert("In note, if you are using Diamond as alignment software you have to indicate the full path to .dmnd path; else if you are using BLAST you have to indicate the full path with the prefix of the database (eg. /path/to/nr).");
}
function help_outfmt(){
    window.alert("In note, you can use all available keywords for both Diamond and BLAST. Refer to the software documentation for more informations about keywords.");
}

function help_workload(){
    window.alert("In this section, you can configure the workload manager you wish to use, or you can choose not to use any workload manager.");
}

function help_alignment(){
    window.alert("In this section, you can set the configuration of the annotation software you will be using. It is necessary to provide the binary path of the software, the input file path (in Multi-FASTA format), the reference database path, the output format to be used (for more information on the outformat, refer to the documentation of the alignment software), and any additional options to be passed to the software (for additional options, refer to the documentation of the annotation software). ");
}