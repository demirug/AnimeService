document.addEventListener('DOMContentLoaded', function(){

    let subscribe = document.getElementById("subscribe");

    let sub_btn = document.getElementById("sub");
    let unsub_btn = document.getElementById("unsub");

    subscribe.querySelectorAll("button").forEach(btn => {
        btn.addEventListener('click', function(event) {


            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/v1/movie/subscribe/", false );
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.send("anime=" + anime_pk);

            data = JSON.parse(xhr.responseText);

            if(data.subscribe) {
                unsub_btn.style.display = null;
                sub_btn.style.display = "none";
            } else {
                unsub_btn.style.display = "none";
                sub_btn.style.display = null;
            }
        });
    })
});

