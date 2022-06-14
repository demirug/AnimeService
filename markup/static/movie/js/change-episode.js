let episode_selector, anime_slug, season;

document.addEventListener('DOMContentLoaded', function(){

    episode_selector = document.getElementById("episode-selector");

    //If episode selector not exists return
    if (typeof(episode_selector) == 'undefined' && episode_selector == null) return;

    //Getting slug/season to build request url
    anime_slug = episode_selector.getAttribute("anime");
    season = episode_selector.getAttribute("season");

    //Getting all episode buttons
    let elements = episode_selector.querySelectorAll("button");

    for(var i = 0; i < elements.length; i++) {
        //To all buttons add onclick action
        elements[i].onclick = function () {

            //If clicked button not selected
            if(this.id != "episode-selected") {

                setEpisodeButton_El(this);
                setCookie(anime_slug + "@" + season, this.innerText)
                json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + this.innerText));
                playEpisode(json);

            }
        }
    }

    //Getting episode number from GET
    let GET_episode = new URL(window.location.href).searchParams.get("episode");

    //If episode exists and positive and not selected yet
    //Do request to get data
    if(GET_episode != null && !isNaN(GET_episode) && parseInt(GET_episode) >= 0 && GET_episode != episode_selector.getAttribute("episode")) {
        json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + GET_episode));
        if(json.detail != null) {
            window.location.replace("/404/");
            return;
        }
        setCookie(anime_slug + "@" + season, GET_episode)
        setEpisodeButton_Num(GET_episode)
    } else {
        let cookie = getCookie(anime_slug + "@" + season)
        if(cookie == undefined) {
           json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + episode_selector.getAttribute("episode")));
        } else {
            json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + cookie));
            if(json.detail != null) {
                 json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + episode_selector.getAttribute("episode")));
            } else {
                setEpisodeButton_Num(cookie)
            }
        }
    }

    playEpisode(json);

});

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
    old.className = "btn btn-info";
    old.id = "episode-" + old.innerText;

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