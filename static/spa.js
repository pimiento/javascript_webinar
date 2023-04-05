var send_log = function (level, message) {
    $.post("/api/log/", {level: level, message: message})
        .done( function (result) {
            console.log("SUCCESS: " + result);
        })
        .fail( function (result) {
            console.log(result);
            alert("FAIL: send_log");
        });
};

var set_notify = function (delta, message) {
    // delta — activate notification delta seconds later
    // message — just a text
    var when = new Date();
    when.setSeconds(when.getSeconds() + delta);
    $.post("/api/notify/", {ts: when.toISOString(), message: message})
        .done( function () {n
            send_log("INF", "set notification: " + when + " -- " + message);
        })
        .fail( function (result) {
            alert("FAIL: " + result);
            send_log("ERR", result);
        });
}

var read_notifications = function () {
    $.get("/api/ts/", function (result) {
        send_log("DBG", "Got current date data: " + $.param(result));
        $.get("/api/notify/", {"ts": result["ts"]})
            .done(function (notifications) {
                send_log("INF", "got " + notifications.length + " notifications");
                let container = $("#notifications");
                container.empty();
                for (const note in notifications) {
                    container.append(
                        '<p class="notification">'
                            + '<span class="notification_ts">'
                            + notifications[note]["ts"]
                            + ':&nbsp;</span><span class="notification_message">'
                            + notifications[note]["message"]
                            + '</span></p>'
                    );
                }
            });
    });
}

$(document).ready(function () {
    var timerId = setInterval(read_notifications, 3000);
    $("#set-notify-form").submit(function (e) {
        let data, form;
        e.preventDefault();
        form = $(this);
        data = form.serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        this.reset();
        set_notify(data["sec"], data["message"]);
    });
});
