var messages = [];
var needUpdate = false;
var reconnectingTimer = undefined;
var paused = false;

function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function GenerateMessageHtml(message){
	messageHtml = message.Data;
	messageHtml += '<a href="javascript:void(0)" onclick="$(this).next().slideToggle(100);" >&#8744;</a>'
	messageHtml += '<pre class="messageInfo">';
	messageHtml += syntaxHighlight(message.Info);
	messageHtml += "</pre>";
	return messageHtml
}

function ProcessIncomingMessage(evt){
	if(paused == true)
		return;
	
	message = JSON.parse(evt.data);
	messageHtml = GenerateMessageHtml(message);
	
	messageDiv = $('<div class="messageContainer">').html(messageHtml).appendTo(document.getElementById("messages"))
    messages.push(messageDiv);
    if(messages.length > 2000){
    	for (var i=0; i<1000; i++){
        	first = messages.shift();
        	first.remove();
        	delete(first); 
    	}
    }
    $(".ui-layout-center").scrollTop($("#messages").height());
}
function Connect(websocketPath){
    var ws = new WebSocket(websocketPath);
    ws.onmessage = ProcessIncomingMessage
    document.getElementById("system").innerHTML = "";
    ws.onclose = function(){ 
        document.getElementById("system").innerHTML = "<br>Disconnected. Reconnectiong...";
        window.scrollTo(0,document.body.scrollHeight);
        reconnectingTimer = window.setInterval("javascript:Reconnect()",1000);
    };
}
function Reconnect(){
	Connect();
	window.clearInterval(reconnectingTimer)
}
function ClearConsole(){
	messages.forEach(function(msgDive){
		msgDive.remove();
		delete(first);
	});
	messages = [];
	document.getElementById("messages").innerHTML = "";
}
function FreezeConsole(){
	document.getElementById("FreezeButton").innerHTML = paused?"Pause":"Run";
	paused = !paused;
}