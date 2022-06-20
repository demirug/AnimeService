let episode_selector, anime_slug, anime_pk, season_pk;

document.addEventListener('DOMContentLoaded', function(){

    episode_selector = document.getElementById("episode-selector");

    //If episode selector not exists return
    if (typeof(episode_selector) == 'undefined' && episode_selector == null) return;

    //Getting slug/season to build request url
    anime_slug = episode_selector.getAttribute("anime");
    anime_pk = episode_selector.getAttribute("pk")
    season_pk = episode_selector.getAttribute("season");

    //Getting all episode buttons
    let elements = episode_selector.querySelectorAll("button");

    for(var i = 0; i < elements.length; i++) {
        //To all buttons add onclick action
        elements[i].onclick = function () {

            //If clicked button not selected
            if(this.id != "episode-selected") {

                setEpisodeButton_El(this);
                setCookie(anime_slug + "@" + season_pk, this.getAttribute("pk"))
                json = api_request(this.getAttribute("pk"))
                playEpisode(json);

            }
        }
    }

    let json = parse_GET();
    if(json == undefined) {
        json = parse_Cookie();
        if (json == undefined) {
            let elem = document.querySelector("#episode-selector > button");
            if (elem != undefined) {
                setEpisodeButton_El(elem)
                json = api_request(elem.getAttribute('pk'));
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
        let elem = document.getElementById("episode-" + GET_episode)
        if(elem != undefined) {
           setCookie(anime_slug + "@" + season_pk, GET_episode)
           setEpisodeButton_El(elem)
           return api_request(elem.getAttribute('pk'));
        }
    }
    return undefined;
}

function parse_Cookie() {
    let cookie_rs = getCookie(anime_slug + "@" + season_pk)
    if(cookie_rs != undefined) {
        let elem = document.getElementById("episode-" + cookie_rs)
        if(elem != undefined) {
           setEpisodeButton_El(elem)
           return api_request(elem.getAttribute('pk'));
        }
    }
    return undefined;
}

function api_request(anime_pk) {
     return JSON.parse(request("/api/v1/movie/episode/" + anime_pk).responseText)
}

function setEpisodeButton_Num(num) {
    //Set episode selected button by episode number
    let element = document.getElementById("episode-" + num);
    if(element == undefined) return
    setEpisodeButton_El(element)
}

function setEpisodeButton_El(element) {
    //Set episode selected button by element
    episode_selector.setAttribute("episode", element.innerText);

    if(element == null) return;

    let old = document.getElementById("episode-selected");
    if(old != undefined) {
        old.className = "btn btn-info";
        old.id = "episode-" + old.innerText;
    }
    element.id = "episode-selected";
    element.className = "btn btn-primary";

}

function playEpisode(json) {
        files = []

        for(let i = 0; i < json.files.length; i++) {
            files.push([json.files[i].file, json.files[i].quality.name, parseInt(json.files[i].quality.wight), json.files[i].quality.default])
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