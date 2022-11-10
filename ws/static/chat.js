var intervalId,
    timeoutId,
    sec = 1000,
    minute = sec * 60,
    period = 5 * sec,
    duration = period * 60, my_ws;

JSON.stringify = JSON.stringify || function (obj) {
    var t = typeof (obj);
    if (t != "object" || obj === null) {
        // simple data type
        if (t == "string") obj = '"'+obj+'"';
        return String(obj);
    }
    else {
        // recurse array or object
        var n, v, json = [], arr = (obj && obj.constructor == Array);
        for (n in obj) {
            v = obj[n]; t = typeof(v);
            if (t == "string") v = '"'+v+'"';
            else if (t == "object" && v !== null) v = JSON.stringify(v);
            json.push((arr ? "" : '"' + n + '":') + String(v));
        }
        return (arr ? "[" : "{") + String(json) + (arr ? "]" : "}");
    }
};

var sendMessage = function (ws) {
    var message = $('#CHAT').val();
    ws.send(JSON.stringify({type: "message", message: message}));
    $('#CHAT').val('');
};

$(document).ready(function() {
    var href = window.location.href.split("//")[1],
        ws = new WebSocket("ws://" + href + "chat");
    ws.onopen = function () {
        ws.send('{"init": "init", "type": "conn"}');
    };
    ws.onmessage = function (evt) {
        console.log(evt.data);
        var data = JSON.parse(evt.data);
        if (data['type'] === 'message') {
            $("#messages").append($(
                '<li>' +
                    '<span>' + data["time"] + ':&nbsp;</span>' +
                    '<span>'+ data["message"] + '</span>' +
                '</li>'
            ));
        }
    };
    $('#CHAT').on('keypress', function (e) {
        if ((e.keyCode == 10 || e.keyCode == 13) && e.ctrlKey) { sendMessage(ws); }
    });
    $('#SEND_MESSAGE').click(function () {
        sendMessage(ws);
    });
});
