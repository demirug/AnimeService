document.addEventListener('DOMContentLoaded', function(){

    let subscribe = document.getElementById("subscribe");
    let request_path = subscribe.getAttribute("path");

    let sub_btn = document.getElementById("sub");
    let unsub_btn = document.getElementById("unsub");

    subscribe.querySelectorAll("button").forEach(btn => {
        btn.addEventListener('click', function(event) {


            data = JSON.parse(post_rqs(request_path));
            if(data.status) {
                unsub_btn.style.display = null;
                sub_btn.style.display = "none";
            } else {
                unsub_btn.style.display = "none";
                sub_btn.style.display = null;
            }
        });
    })
});

function post_rqs(url) {
    var request = new XMLHttpRequest();
    request.open( "POST", url, false );
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.send();
    return request.responseText
}
