var BTN_PARAMS = null;

$(document).ready(function() {
    $("#musicBTN").click(function() {
        BTN_PARAMS = 'music';
        let e = document.getElementById("content");
        let child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }

        $.ajax({
            url: "pagination/",
            context: document.body,
            success: function(response) {
                $("#content").html(response);
            }
        });
    });
    $("#videoBTN").click(function() {
        BTN_PARAMS = 'video';
        let e = document.getElementById("content");
        let child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }

        $.ajax({
            url: "pagination/",
            context: document.body,
            success: function(response) {
                $("#content").html(response);
            }
        });
    });
    $("#allBTN").click(function() {
        BTN_PARAMS = null;
        let e = document.getElementById("content");
        let child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }

        let deferred1 =$.ajax({
            url: "pagination/",
            context: document.body,
            success: function(response) {
                $("#content").html(response);
            }
        });
        deferred1.done(function(response2) {
            console.log("Pages loaded correctly");
    });
});


});


