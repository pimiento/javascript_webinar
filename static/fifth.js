$(function () {
    $("#center-text").on("click", function () {
        $.get("/color", function (data) {
            alert(data);
        });
    });
});
