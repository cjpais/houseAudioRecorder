toggle = $("#recToggle");
page = $("#page")[0];
recInfo = $('#recInfo')[0];
recName = $('#recName');
recTime = $('#recTime')[0];
serverStatus = {running: false};

$("#listbtn").click(function(e) {
    self.parent.location = "/ls";
});

$("#tagbtn").click(function(e) {

});

toggle.click(function(e) {
	e.preventDefault();
	// get button string
	act = (serverStatus.running) ? "stop" : "start";
    console.log(act);
    // send rename first
    if (renameMutex && serverStatus.running) {
        applyRename();
        clearTimeout(renameTimeout);
    }

	$.ajax({
	    type: "POST",
	    url: "/toggle/",
	    data: {action: act},
	    success: updateSync 
	});
});

renameTimeout = null;
renameMutex = false;
recName.on('input', function(e) {
    if (renameMutex) {
        clearTimeout(renameTimeout);
    }
    renameMutex = true;
    renameTimeout = setTimeout(applyRename, 1000);
});

function applyRename() {
    console.log(recName[0].value);
    $.ajax({
        type: "POST",
        url: "/name/",
        data: {name: recName[0].value, id: serverStatus.id},
        success: function () {
            renameMutex = false;
        }
    });
}

// this will set things to be visible or invisible depending on state
function setVisibility(isRecording) {
    if (isRecording) {
        toggle[0].innerHTML = "Stop Recording";
        recInfo.hidden = false;
        
        setGreenBackground(page);
    } else {
        toggle[0].innerHTML = "Start Recording";
        recInfo.hidden = true;

        setRedBackground(page);
    }
}


// function to synchronize state with the server
// this is to be called every second or so.
function updateSync() {
    $.ajax({
        type: "POST", 
        url: "/status/",
        data: {},
        success: function (data) {
            if (!renameMutex) {
                recName[0].value = data["name"];
            }

            serverStatus = data;
            setVisibility(data.running);
        }
    });
}
// call the update function every 10 seconds
updateSync();
var updateInterval = window.setInterval(updateSync, 10000);



var timerInterval = window.setInterval(function() {
    // set the time
    if (serverStatus.running) {
        var timeDelta = (Date.now() / 1000) - serverStatus.time;
        if (timeDelta < 0) timeDelta = 0;
        var seconds = Math.floor(timeDelta) % 60;
        var minutes = Math.floor(timeDelta / 60);
    
        var timeString = minutes + ":";
        if (seconds < 10) {
            timeString += "0";
        }
        timeString += seconds + "." + Math.floor(timeDelta * 10) % 10;

	    recTime.innerHTML = timeString;
    }
}, 25);






//            __              __              
//           /  \            /  \      
//           \  /            \  /
//            --              --
//
//      __            /              __
//       |           /_              | 
//        \                         /
//         ==                     ==
//         |   ------------------  |
//           \ |  |  |  |  |  | | /
//             ------------------ 









