$(document).ready(function () {

    let sub_btn = $("#sub");
    let unsub_btn = $("#unsub");

    $("#subscribe > button").click(function () {

        data = JSON.parse(request("/api/v1/movie/subscribe/", "POST", "anime=" + anime_pk).responseText);

        if(data.subscribe) {
            unsub_btn.show();
            sub_btn.hide();
        } else {
            unsub_btn.hide();
            sub_btn.show();
        }
    });
});

