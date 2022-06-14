document.addEventListener('DOMContentLoaded', function(){

    let subscribe = document.getElementById("subscribe");
    let request_path = subscribe.getAttribute("path");

    let sub_btn = document.getElementById("sub");
    let unsub_btn = document.getElementById("unsub");

    subscribe.querySelectorAll("button").forEach(btn => {
        btn.addEventListener('click', function(event) {


            data = JSON.parse(request(request_path, "POST"));
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

