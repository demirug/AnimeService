var episode_pk;

$(document).ready(function () {

    //Getting all episode buttons
    $("#episode-selector > button").click(function () {
        var episode = $(this)
        if(episode.attr("id") != "episode-selected") {

            setEpisodeButton_El(episode);
            setCookie(anime_slug + "@" + season_pk, episode.attr("pk"));
            json = api_request(episode.attr("pk"));
            playEpisode(json);

        }
    });

    let json = parse_GET();
    if(json == undefined) {
        json = parse_Cookie();
        if (json == undefined) {
            let elem = $("#episode-selector > button").first();
            if (elem != undefined) {
                setEpisodeButton_El(elem);
                json = api_request(elem.attr('pk'));
            }
        }
    }
    if(json != undefined) {
        playEpisode(json);
    }
});

function parse_GET() {
    let GET_episode = new URL(window.location.href).searchParams.get("episode");
    if(GET_episode != undefined) {
        let elem = $("#episode-" + GET_episode);
        if(elem.length) {
           setCookie(anime_slug + "@" + season_pk, GET_episode);
           setEpisodeButton_El(elem);
           return api_request(elem.attr("pk"));
        }
    }
    return undefined;
}

function parse_Cookie() {
    let cookie_rs = getCookie(anime_slug + "@" + season_pk);
    if(cookie_rs != undefined) {
        let elem = $("#episode-" + cookie_rs);
        if(elem != undefined) {
           setEpisodeButton_El(elem);
           return api_request(elem.attr('pk'));
        }
    }
    return undefined;
}

function api_request(episode_pk) {
     let rqs = request("/api/v1/movie/episode/" + episode_pk + "/");
     return rqs.status === 200 ? JSON.parse(rqs.responseText) : undefined;
}

function setEpisodeButton_Num(num) {
    //Set episode selected button by episode number
    let element = document.getElementById("episode-" + num);
    if(element == undefined) return;
    setEpisodeButton_El(element);
}

function setEpisodeButton_El(element) {
    //Set episode selected button by element

    if(element == null) return;

    let old = document.getElementById("episode-selected");
    if(old != undefined) {
        old.className = "btn btn-info";
        old.id = "episode-" + old.innerText;
    }

    element.attr("class", "btn btn-primary");
    element.attr("id", "episode-selected");

    episode_pk = element.pk;

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