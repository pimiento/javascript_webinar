$(document).ready(function () {
    var update = function () {
        $.ajax({
            "url": "/dice/json",
        }).done(function (data) {
            $("#dice_value")
                .text(data["dice_value"]);
        });
        $.ajax({
            "url": "/color/json",
        }).done(function (data) {
            $("#dice_value")
                .css({
                    "color": "rgb(" + data["fg_value"].join(",") + ")",
                    "background-color": "rgb(" + data["bg_value"].join(",") + ")",
                });
        });
    };
    update();
    $("#roll").bind("click", update);
    $("#dice_value").css({
        "font-size": "300px",
        "padding-left": "50%",
        "padding-right": "50%",
    });
});
