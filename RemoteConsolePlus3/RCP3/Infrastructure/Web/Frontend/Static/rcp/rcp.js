RCP = {
		websocketServerName : "",
		messages : [],
		reconnectingTimer : undefined,
		paused : false,
		treeRefreshing : false,

		syntaxHighlight : function(json) {
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
		},

		GenerateMessageHtml : function(message){
			messageHtml = message.Data;
			messageHtml += '<a href="javascript:void(0)" onclick="$(this).next().slideToggle(100);" >&#8744;</a>'
				messageHtml += '<pre class="messageInfo">';
			messageHtml += RCP.syntaxHighlight(message.Info);
			messageHtml += "</pre>";
			return messageHtml
		},

		ProcessIncomingMessage : function(evt){
			if(RCP.paused == true)
				return;

			message = JSON.parse(evt.data);
			messageHtml = RCP.GenerateMessageHtml(message);

			messageDiv = $('<div class="messageContainer">').html(messageHtml).appendTo(document.getElementById("messages"))
			RCP.messages.push(messageDiv);

			if(RCP.messages.length > 1000){
				for (var i=0; i<500; i++){
					RCP.messages.shift().remove();
				}
			}
			$(".ui-layout-center").scrollTop($("#messages").height());
		},

		Connect : function(){
			var ws = new WebSocket(RCP.websocketServerName);
			ws.onmessage = RCP.ProcessIncomingMessage
			ws.onclose = function(){ 
				$('body').layout().show("south");
				$("#bottom-information-panel").html("Disconnected. Waiting 1 second before reconnecting...");
				RCP.reconnectingTimer = window.setInterval("javascript:RCP.Reconnect()",1000);
			};
			ws.onopen = function(){ 
				$("#bottom-information-panel").html("Connected.");
				$('body').layout().hide("south");
			};
		},

		Reconnect : function(){
			$("#bottom-information-panel").html("Disconnected. Reconnecting...");
			RCP.Connect();
			window.clearInterval(RCP.reconnectingTimer)
		},

		ClearConsole:function(){
			RCP.messages = [];
			document.getElementById("messages").innerHTML = "";
		},

		FreezeConsole:function(){
			$("#FreezeButton").html(RCP.paused?"Pause":"Run");
			RCP.paused = !RCP.paused;
		},

		OnTreeChanged:function(event, data){
			console.log("OnTreeSelectionChanged", event, data);
			if((data.action == "select_node" || data.action == "deselect_node") 
					&& RCP.treeRefreshing == false){
				console.log(RCP.treeRefreshing);
				var jqxhr = $.post( '../StreamsTree/UpdateTreeSelection', { 
					'sessionId' : RCP.sessionId,
					'selectedNodes' : JSON.stringify(data.selected)
				}).done(function() {
					console.log( "AJAX POS update selection done" );
				});
			}
		},
		
		RefreshTree:function(){
			RCP.treeRefreshing = true;
			$('#jstree').jstree('refresh');
		}
		
}