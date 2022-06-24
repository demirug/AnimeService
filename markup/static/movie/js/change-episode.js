$(document).ready(function () {

    $("#seasons").change(function () {
        var href = $(this).find("option:selected").attr("href");
        if(href != undefined) {
            window.location.href = href;
        }
    })

    $("#episodes").change(function () {
        var episode = $(this).find("option:selected");
         setCookie(anime_slug + "@" + season_pk, episode.attr("value"));
         json = api_request(episode.attr("pk"));
         playEpisode(json);
    })

    let json = parse_GET();
    if(json == undefined) {
        json = parse_Cookie();
        if (json == undefined) {
            let elem = $("#episodes > option").first();
            if (elem.length) {
                elem.attr("selected", "")
                json = api_request(elem.attr('pk'));
            }
        }
    }
    if(json != undefined) {
        playEpisode(json);
    }
});

function parse_GET() {
    let GET_episode = new URL(window.location.href).searchParams.get("e");
    if(GET_episode != undefined) {
        let elem = $("#episodes > option[value='" + GET_episode + "']");
        if(elem.length) {
           setCookie(anime_slug + "@" + season_pk, GET_episode);
           $(elem).attr("selected", "")
           return api_request(elem.attr("pk"));
        }
    }
    return undefined;
}

function parse_Cookie() {
    let cookie_rs = getCookie(anime_slug + "@" + season_pk);
    if(cookie_rs != undefined) {
        let elem = $("#episodes > option[value='" + cookie_rs + "']");
        if(elem.length) {
           elem.attr("selected", "")
           return api_request(elem.attr('pk'));
        }
    }
    return undefined;
}

function api_request(episode_pk) {
     let rqs = request("/api/v1/movie/episode/" + episode_pk + "/");
     return rqs.status === 200 ? JSON.parse(rqs.responseText) : undefined;
}

function playEpisode(json) {
        files = []

        for(let i = 0; i < json.files.length; i++) {
            files.push([json.files[i].file, json.files[i].quality.name, parseInt(json.files[i].quality.wight), json.files[i].quality.default]);
        }

        //Sort video sources by quality
        files.sort(function(a, b){return a[2] - b[2]});

        playView(files);
}

function playView(files) {
    //Set new video source for player
    var player = videojs('my-video');

    data = []

    for(let i = 0; i < files.length; i++) {
        data[i] = {
            src: files[i][0],
            type: 'video/' + files[i][0].split(".").pop(),
            label: files[i][1],
            selected: files[i][3]
        }
    }
    player.src(data);
}