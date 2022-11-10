var sendMessage = function (ws) {
    var message = $('#CHAT').val(),
	name = $('#name').val();
    ws.send(JSON.stringify({type: "message", message: message, name: name}));
    $('#CHAT').val('');
};

$().ready(function() {
    var href = window.location.href.split("//")[1],  // https://domain.com:4000/
        ws = new WebSocket("ws://" + href + "chat");
    ws.onopen = function () {
        ws.send('{"init": "init", "type": "conn"}');
    };
    ws.onmessage = function (evt) {
        var data = JSON.parse(evt.data);
        if (data['type'] === 'message') {
	    console.log(data);
            $("#messages").append($(
                '<li>' +
                    '<span>' + data["time"] + ':&nbsp;</span>' +
		    '<span style="color:blue;">' + data["name"] + ':&nbsp;</span>' +
                    '<span style="color:green;">'+ data["message"] + '</span>' +
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
