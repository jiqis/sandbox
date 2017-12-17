<script language="javascript">

Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
};

Array.prototype.remove = function(obj) {
    var i = this.indexOf(obj);
    if (i > -1) {
        this.splice(i, 1);
    }
};

var black = "rgb(0, 0, 0)";
var gray = "rgb(168, 168, 168)";

var checkedIntersections = [];
var intersection = document.getElementById("intersection");
var checkedIntersectionsHTML = document.getElementById("checked_intersections");

function selectWord(element) {
    if (element.id.substring(0, 6) == "clone_") {
        var clone = element;
        var original = document.getElementById(clone.id.substring(6));
        intersection.removeChild(clone);

        if (element.id.substring(0, 3) != "ph_") {
            original.style.color = black;
        }
    } else {
        var original = element;
        if (original.style.color != gray) {
            var clone = original.cloneNode(true);
            clone.id = "clone_" + original.id;
            clone.innerHTML = clone.innerHTML + " ";
            clone.style.fontWeight = "bold";
            intersection.appendChild(clone);

            if (element.id.substring(0, 3) != "ph_") {
                original.style.color = gray;
            }
        }
    }
}

function checkClick() {
    if (intersection.childNodes.length == 0) {
        alert("An intersection must contain at least one token.");
        return;
    }

    var intersectionElements = [];
    for (var i = 0; i < intersection.childNodes.length; i++) {
        if (intersection.childNodes[i].nodeName == "SPAN") {
            intersectionElements.push(intersection.childNodes[i]);
        }
    }

    var selected = [];
    var newSentence = "";
    for (var i = 0; i < intersectionElements.length; i++) {
        selected.push(intersectionElements[i].id.substring(6));
        newSentence = newSentence + intersectionElements[i].innerHTML;
        selectWord(intersectionElements[i]);
    }
    checkedIntersections.push(selected);
    checkedIntersectionsHTML.innerHTML = newSentence + "</br>" + checkedIntersectionsHTML.innerHTML;
}

function undoClick() {
    if (intersection.childNodes.length == 0) {
        checkedIntersections.pop();
        var rollbackIndex = checkedIntersectionsHTML.innerHTML.indexOf("br>") + 3;
        checkedIntersectionsHTML.innerHTML = checkedIntersectionsHTML.innerHTML.substring(rollbackIndex);
    } else {
        var intersectionElements = [];
        for (var i = 0; i < intersection.childNodes.length; i++) {
            if (intersection.childNodes[i].nodeName == "SPAN") {
                intersectionElements.push(intersection.childNodes[i]);
            }
        }
        for (var i = 0; i < intersectionElements.length; i++) {
            selectWord(intersectionElements[i]);
        }
    }
}

function validateUnselected() {
    if (intersection.childNodes.length != 0) {
        alert("You have not checked-in your current sentence.")
        return false;
    }

    var done = confirm("You have created " + checkedIntersections.length.toString() + " sentences. Is that all?");
    if (!done) {
        return false;
    }

    var intersectionTokenString = "";
    var intersectionSentenceString = "";
    for (var i = 0; i < checkedIntersections.length; i++) {
        for (var j = 0; j < checkedIntersections[i].length; j++) {
            intersectionTokenString += checkedIntersections[i][j];
            intersectionTokenString += ",";
        }
        intersectionTokenString += ";";
    }
    document.getElementById("intersections_token_str").value = intersectionTokenString;

    while (checkedIntersectionsHTML.innerHTML.length > 0) {
        var rollbackIndex = checkedIntersectionsHTML.innerHTML.indexOf("br>") + 3;
        var uncutSentence = checkedIntersectionsHTML.innerHTML.substring(0, rollbackIndex);
        intersectionSentenceString += uncutSentence.substring(0, uncutSentence.lastIndexOf(" "));
        intersectionSentenceString += "|||";
        checkedIntersectionsHTML.innerHTML = checkedIntersectionsHTML.innerHTML.substring(rollbackIndex);
    }
    document.getElementById("intersections_sentence_str").value = intersectionSentenceString;

    return true;
}

window.onkeyup = function(event) {
    if (event.which == 32) { // Space-bar
        checkClick();
    } else if (event.ctrlKey && event.which == 90) { // Ctrl+Z
        undoClick();
    }
};

</script>