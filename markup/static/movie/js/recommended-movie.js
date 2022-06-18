document.addEventListener('DOMContentLoaded', function(){

    // 50% chance to show recommended anime
    if(Math.floor(Math.random() * 2) === 0) return;

    let episode_selector = document.getElementById("episode-selector");

    //If episode selector not exists return
    if (typeof(episode_selector) == 'undefined' && episode_selector == null) return;

    let slug = episode_selector.getAttribute("anime");

    let answer = JSON.parse(request("/api/v1/movie/random/" + slug))

    // If detail in response -> recommendation not found (404)
    if(answer.detail) return;

    new MainModal().setTitle("Recommended anime")
        .addToBody("<h5>" + answer.name + "</h5>")
        .addToBody("<img style='max-width: 300px' src='" + answer.poster + "'/>")
        .addToFooter("<a class='btn btn-primary' href='" + answer.url + "' target='_blank'>View</a>")
        .addFooterCloseButton()
        .show();
});