var chatSocket = null;
const url = (window.location.protocol === 'https:' ? "wss://" : "ws://") + window.location.host + '/ws/chat/'
var username = null;

$(document).ready(function () {
    username = JSON.parse(document.getElementById('username').textContent);
    startWebSocket()

    let form = document.getElementById('chat_form')
    form.addEventListener('submit', function(e) {
        e.preventDefault()

        let message = e.target.message.value
        if(message.replace(/ /g,'').length === 0) return;
        if(chatSocket != null && chatSocket.readyState == 1) {
            chatSocket.send(JSON.stringify({
                'message': message
            }))

            form.reset()
        }
    })

});

function startWebSocket() {

    chatSocket = new WebSocket(url)
    chatSocket.onmessage = handleMessage
    chatSocket.onclose = function(){
        chatSocket = null
        setTimeout(startWebSocket, 1000)
    }
}

function handleMessage(event) {
    let data = JSON.parse(event.data)
    console.log(data)

    if(data.type == "chat") {
        let messages = document.getElementById('messages')
        if(data.username == username) {
            messages.insertAdjacentHTML('beforeend', '<div class="media ml-auto mb-3"><div class="media-body"><div class="bg-primary rounded py-2 px-3 mb-2"><p class="text-small mb-0 text-white">' + data.message + '</p></div></div></div></div>')
        } else {
            messages.insertAdjacentHTML('beforeend', '<div class="media mb-3"><img src="' + data.avatar + '" alt="user" width="50" class="rounded-circle"><div class="media-body ml-3"><div class="bg-light rounded py-2 px-3 mb-2"><p class="text-small mb-0 text-muted">' + data.message + '</p></div></div></div></div>')
        }

    }

}