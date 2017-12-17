<script language="javascript">

Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}

Array.prototype.remove = function(obj) {
    var i = this.indexOf(obj);
    if (i > -1) {
        this.splice(i, 1);
    }
}

var aligned = [];
var selected = [];
var disabled = [];
var groups = GROUPS;

function selectWord(selectedElement) {
    var group = groups[selectedElement.id];
    for (var i = 0; i < group.length; i++) {
        e = document.getElementById(group[i]);
        if (!disabled.contains(e)) {
            if (selected.contains(e)) {
                selected.remove(e);
                e.style.backgroundColor = "white";
            } else {
                selected.push(e);
                e.style.backgroundColor = "yellow";
            }
        }
    }
}

function alignClick() {
    if (isValidAlignment(selected)) {
        aligned.push(selected);
        for (var i = 0; i < selected.length; i++) {
            var e = selected[i];
            e.style.backgroundColor = getColor(aligned.length - 1);
            e.style.color = "black";
            disabled.push(e);
        }
        selected = [];
    } else {
        alert("An alignment must contain at least one token from each sentence.");
    }
}

function getColor(i) {
    var red = 0;
    var green = 0;
    var blue = 0;

    var col1 = 255;
    var col2 = 208 - 16 * Math.floor(i / 6);
    var col3 = 160 - 48 * Math.floor(i / 6);

    switch (i % 6) {
        case 1:
            red = col1;
            green = col3;
            blue = col2;
            break;
        case 2:
            red = col3;
            green = col1;
            blue = col2;
            break;
        case 3:
            red = col1;
            green = col2;
            blue = col3;
            break;
        case 4:
            red = col3;
            green = col2;
            blue = col1;
            break;
        case 5:
            red = col2;
            green = col1;
            blue = col3;
            break;
        case 0:
            red = col2;
            green = col3;
            blue = col1;
            break;
    }

    red = getColorString(red);
    green = getColorString(green);
    blue = getColorString(blue);

    return "#" + red + green + blue;
}

function getColorString(color) {
    var s = color.toString(16);
    if (s.length == 1) {
        s = "0" + s;
    }
    return s;
}

function isValidAlignment(alignment) {
    s1 = false;
    s2 = false;
    for (var i = 0; i < alignment.length; i++) {
        var c = alignment[i].id[1];
        if (c == "1") {
            s1 = true;
        } else if (c == "2") {
            s2 = true;
        } else {
            alert("HORRIBLE BUG!");
            alert("id=" + alignment[i].id);
        }
    }
    return s1 && s2;
}

function undoClick() {
    if (selected.length == 0) {
        var lastAlignment = aligned.pop();
        for (var i = 0; i < lastAlignment.length; i++) {
            var e = lastAlignment[i];
            e.style.backgroundColor = "white";
            e.style.color = "black";
            disabled.remove(e);
        }
    } else {
        for (var i = 0; i < selected.length; i++) {
            var e = selected[i];
            e.style.backgroundColor = "white";
            e.style.color = "black";
        }
        selected = [];
    }
}

function validateAlignments() {
    var done = confirm("You have marked " + aligned.length.toString() + " alignments. Is that all?");
    if (!done) {
        return false;
    }

    var alignmentString = "";
    for (var i = 0; i < aligned.length; i++) {
        for (var j = 0; j < aligned[i].length; j++) {
            alignmentString += aligned[i][j].id;
            alignmentString += ",";
        }
        alignmentString += ";";
    }
    document.getElementById("alignments").value = alignmentString;
    return true;
}

window.onkeyup = function(event) {
    if (event.which == 32) { // Space-bar
        alignClick();
    } else if (event.ctrlKey && event.which == 90) { // Ctrl+Z
        undoClick();
    }
};

</script>