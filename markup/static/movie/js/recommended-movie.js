$(document).ready(function () {

    // 50% chance to show recommended anime
    if(Math.floor(Math.random() * 2) === 0) return;

    let answer = request("/api/v1/movie/random/" + anime_slug + "/")

    if(answer.status === 404) return;

    let data = JSON.parse(answer.responseText)

    new MainModal().setTitle("Recommended anime")
        .addToBody("<h5>" + data.name + "</h5>")
        .addToBody("<img style='max-width: 300px' src='" + data.poster + "'/>")
        .addToFooter("<a class='btn btn-primary' href='/anime/" + data.slug + "' target='_blank'>View</a>")
        .addFooterCloseButton()
        .show();
});