$(function () {
    $("#center-text").on("click", function () {
        $.get("/color/json", function (data) {
            alert(data);
        });
    });
});
