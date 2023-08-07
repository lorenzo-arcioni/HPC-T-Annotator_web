function initPage() {
    toggleConfigurationPanel();
    document.getElementById("sub_B").addEventListener("click", validateForm);
    document.getElementById("help_add_options").addEventListener("click", help_add_options);
}

document.addEventListener("DOMContentLoaded", function () {
    initPage();
});

function toggleConfigurationPanel() {
    var slurmConfPanel = document.getElementById("slurmConfPanel");
    var htcondorConfPanel = document.getElementById("htcondorConfPanel");
    var noneConfPanel = document.getElementById("noneConfPanel");

    var slurmRadio = document.getElementById("slurm");
    var htcondorRadio = document.getElementById("htcondor");
    var noneRadio = document.getElementById("none");

    if (slurmRadio.checked) {
        slurmConfPanel.style.display = "block";
        htcondorConfPanel.style.display = "none";
        noneConfPanel.style.display = "none";
    } else if (htcondorRadio.checked) {
        slurmConfPanel.style.display = "none";
        htcondorConfPanel.style.display = "block";
        noneConfPanel.style.display = "none";
    } else if (noneRadio.checked) {
        slurmConfPanel.style.display = "none";
        htcondorConfPanel.style.display = "none";
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

    if (add_options.value.match('.*-num_threads.*') || add_options.value.match('.*-p.*') || add_options.value.match('.*-o.*') || add_options.value.match('.*-out.*')){
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
    window.alert("In note, only options related to computation are accepted; options indicating the usage of threads and input/output file names are not accepted. So the options -p and -o for diamond or -out and -num_threads for blast are not accepted!");
}