<script language="javascript">

var prerequisites = PREREQUISITES;
var equals = EQUALS;

var white = "rgb(255, 255, 255)";
var gray = "rgb(217, 217, 217)";

function validateEntailments() {
    var allFormElements = document.getElementById("formic").elements;

    for (var i = 0; i < allFormElements.length; i++) {
        if (allFormElements[i].type == "radio") {
            var radioElement = allFormElements[i].name;
            var checked = false;
            var allRadioOptions = document.getElementsByName(radioElement);

            for (var j = 0; j < allRadioOptions.length; j++) {
                if (allRadioOptions[j].checked) {
                    checked = true;
                }
            }

            if (!checked) {
                alert("Missing annotations!");
                return false;
            }
        }
    }

    return true;
}

function annotate(entailment, enable) {
    if (enable) {
        enableSelects(entailment.name, true);
    } else {
        enableSelects(entailment.name, false);
    }

    var table = document.getElementById(entailment.name);
    if (enable == null) {
        table.style.backgroundColor = gray;
        document.getElementById(entailment.name + ":True").style.fontWeight = "";
        document.getElementById(entailment.name + ":False").style.fontWeight = "";
        document.getElementById(entailment.name + ":NA").style.fontWeight = "bold";
    } else if (enable) {
        table.style.backgroundColor = "#CCDDF8";
        document.getElementById(entailment.name + ":True").style.fontWeight = "bold";
        document.getElementById(entailment.name + ":False").style.fontWeight = "";
        document.getElementById(entailment.name + ":NA").style.fontWeight = "";
    } else {
        table.style.backgroundColor = "#FFCCE3";
        document.getElementById(entailment.name + ":True").style.fontWeight = "";
        document.getElementById(entailment.name + ":False").style.fontWeight = "bold";
        document.getElementById(entailment.name + ":NA").style.fontWeight = "";
    }

    checkPrerequisites(entailment.name.replace(">", "?").replace("<", "?"));
}

function checkPrerequisites(entailmentName) {
    if (entailmentName in prerequisites) {
        var prerequisiteEntailments = prerequisites[entailmentName];

        enableChildren = !((getRadioValue(entailmentName.replace("?", ">")) == "False" || getRadioValue(entailmentName.replace("?", ">")) == "NA") &&
                           (getRadioValue(entailmentName.replace("?", "<")) == "False" || getRadioValue(entailmentName.replace("?", "<")) == "NA"));

        for (var i = 0; i < prerequisiteEntailments.length; i++) {
            enableEverything(prerequisiteEntailments[i].replace("?", ">"), enableChildren);
            enableEverything(prerequisiteEntailments[i].replace("?", "<"), enableChildren);
            checkPrerequisites(prerequisiteEntailments[i]);
        }
    }
}

function enableEverything(entailmentName, enable) {
    var element = document.getElementById(entailmentName);
    if ((enable && (element.style.backgroundColor == gray)) || (!enable && (element.style.backgroundColor != gray))) {
        element.style.backgroundColor = (enable ? white : gray);
        enableRadios(entailmentName, enable);
        enableSelects(entailmentName, enable);
    }
}

function enableSelects(entailmentName, enable) {
    var allSelects = document.getElementsByTagName("select");
    for (var i = 0; i < allSelects.length; i++) {
        if (allSelects[i].name.indexOf(entailmentName) == 0) {
            allSelects[i].disabled = !enable;
        }
    }
}

function enableRadios(entailmentName, enable) {
    var allRadios = document.getElementsByName(entailmentName);
    for (var i = 0; i < allRadios.length; i++) {
        if (!enable && allRadios[i].value == "NA") {
            allRadios[i].checked = true;
        } else {
            allRadios[i].checked = false;
        }
        allRadios[i].disabled = !enable;
    }

    document.getElementById(entailmentName + ":True").style.fontWeight = "";
    document.getElementById(entailmentName + ":False").style.fontWeight = "";
}

function getRadioValue(entailmentName) {
    var allRadios = document.getElementsByName(entailmentName);
    for (var i = 0; i < allRadios.length; i++) {
        if (allRadios[i].checked) {
            return allRadios[i].value;
        }
    }
    return null;
}

function init() {
    annotateEquals();
    submitEmptyForm();
}

function annotateEquals() {
    for (var i = 0; i < equals.length; i++) {
        var allRadios = document.getElementsByName(equals[i]);
            for (var j = 0; j < allRadios.length; j++) {
            if (allRadios[j].value == "True") {
                allRadios[j].checked = true;
                annotate(allRadios[j], true);
            }
        }

        var table = document.getElementById(equals[i]);
        table.style.visibility = "hidden";
        table.style.display = "none";
    }
}

function submitEmptyForm() {
    var allFormElements = document.getElementById("formic").elements;

    for (var i = 0; i < allFormElements.length; i++) {
        if (allFormElements[i].type == "radio") {
            var radioElement = allFormElements[i].name;
            var checked = false;
            var allRadioOptions = document.getElementsByName(radioElement);

            for (var j = 0; j < allRadioOptions.length; j++) {
                if (allRadioOptions[j].checked) {
                    checked = true;
                }
            }

            if (!checked) {
                return;
            }
        }
    }

    document.forms["formic"].submit();
}

</script>