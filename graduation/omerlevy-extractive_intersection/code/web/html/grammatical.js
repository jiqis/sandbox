<script language="javascript">

function validateGrammar() {
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

function annotate(sentenceElement, enable) {
    var sentence = sentenceElement.name.substring(0, sentenceElement.name.length - 5);
    var table = document.getElementById(sentence);
    if (enable) {
        table.style.backgroundColor = "#CCDDF8";
        document.getElementById(sentence + ":True").style.fontWeight = "bold";
        document.getElementById(sentence + ":False").style.fontWeight = "";
    } else {
        table.style.backgroundColor = "#FFCCE3";
        document.getElementById(sentence + ":True").style.fontWeight = "";
        document.getElementById(sentence + ":False").style.fontWeight = "bold";
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

window.onload = submitEmptyForm();

</script>