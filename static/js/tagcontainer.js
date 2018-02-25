allTags = [];

function clickFunction(clickEvent) {
    var clickedtag = clickEvent.target.innerHTML;

    var tag;
    // search for the string in all tags
    for (var i = 0; i < allTags.length; i++) {
        if (allTags[i].name == clickedtag) {
            tag = allTags[i];
            break;
        }
    }

    tag.isSelected = !tag.isSelected;
    console.log(tag.element);
    $.ajax({
        type: "POST",
        url: "/tag/",
        data: {tagId: tag.id, recId: serverStatus.id},
        success: function() {}
    });

    if (tag.isSelected) {
        tag.element.classList.add("tag-selected");
    } else {
        tag.element.classList.remove("tag-selected");
    }

}

function showSearchResults(results) {
    for (var i = 0; i < allTags.length; i++) {
        var found = false;
        for (var j = 0; j < results.length; j++) {
            if (results[j].name == allTags[i].name) {
                found = true;
                break;
            }
        }
        if (!found) {
            allTags[i].element.style.display = "none";
        } else {
            allTags[i].element.style.display = "inline-block";
        }
    }
}

// this function will highlight the current tags set
function setRecordingTags(tags) {
    for (var i = 0; i < allTags.length; i++) {
        var found = false;
        for (var j = 0; j < tags.length; j++) {
            if (tags[j].name == allTags[i].name) {
                found = true;
                break;
            }
        }
        if (!found) {
            allTags[i].isSeleted = false;
            allTags[i].element.style.background = "#00000000";
        } else {
            allTags[i].isSelected = true;
            allTags[i].element.style.background = "#33B5E5FF";
        }
    }
}

// input:
// A list of objects with name and id
// 
// Effect:
//  will create an element for each member of that list
//  will fill the container with those elements
function populateContainer(container, tags) {
    allTags = tags;
    container.className = "tag-container";
    container.innerHTML = "";

    // create and add tags
    for (var i = 0; i < tags.length; i++) {
        tags[i].isSelected = false;
        var elem = document.createElement("a");
        tags[i].element = elem;
        elem.className = "tag";
        elem.addEventListener("click", clickFunction);
        elem.innerHTML = tags[i].name;
        container.appendChild(elem);
    }

}

function loadAllTags() {
    $.ajax({
        type: "POST",
        url: "/tags/",
        data: {},
        success: function(data) {
            populateContainer(document.getElementById("tags"), data);
        }
    });
}
loadAllTags();

// SEARCH BOX JQUERY STUFF
// !!!
//
$("#tagSearch").on("input", function() {
    var searchTerm = document.getElementById("tagSearch").value;
    $.ajax({
        type: "POST", 
        url: "/tags/search/",
        data: {"query": searchTerm},
        success: function (data) {
            showSearchResults(data);
        }
    });
});

// enter key
$("#tagSearch" ).on("keydown", function(e) {
    if(e.which == 13) {
        var searchTerm = document.getElementById("tagSearch").value;
        $.ajax({
            type: "POST",
            url: "/tag/",
            data: {tagName: searchTerm},
            success: function (data) {
                //setRecordingTags(data);
            }
        });
        document.getElementById("tagSearch").value = "";
        loadAllTags();
        return false;
    }
});
