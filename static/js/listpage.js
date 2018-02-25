page = $("#page")[0];

$(":button").click(function(e) {
    e.preventDefault();
    
    var conf = confirm("Are you sure you want to delete " + e.target.id);
    
    if (conf) {
        $.ajax({
            type: "POST",
            url: "/delete/",
            data: {id: e.target.id},
            success: function () {
                // remove the row from the table
                e.target.parentElement.parentElement.remove()
            }
        });
    }
});

$(".name").click(function () {
    console.log(this);
});

function updateSync() {
    $.ajax({
        type: "POST",
        url: "/status/",
        data: {},
        success: function (data) {
            if (data.running) setGreenBackground(page);
            else setRedBackground(page);
        }
    });
}

updateSync();
var updateInterval = setInterval(updateSync, 10000);
