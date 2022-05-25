document.addEventListener('DOMContentLoaded', function(){

    let selector = document.getElementById("episode-selector");

    //If episode selector not exists return
    if (typeof(selector) == 'undefined' && selector == null) return;

    //Getting slug/season to build request url
    let anime_slug = selector.getAttribute("anime");
    let season = selector.getAttribute("season");

    //Getting all episode buttons
    let elements = selector.querySelectorAll("button");

    for(var i = 0; i < elements.length; i++) {
        elements[i].onclick = function () {

            //If clicked button not selected
            if(this.id != "episode-selected") {

                let episode = this.innerText;
                //Do request to API
                json = JSON.parse(request("/api/v1/episode/" + anime_slug + "/" + season + "/" + episode));

                files = []

                for(i = 0; i < json.files.length; i++) {
                    files.push([json.files[i].file, json.files[i].quality.name, parseInt(json.files[i].quality.wight)])
                }

                //Sort video sources by quality
                files.sort(function(a, b){return a[2] - b[2]});

                let old = document.getElementById("episode-selected")

                old.removeAttribute("id");
                old.className = "btn btn-info"

                this.id = "episode-selected"
                this.className = "btn btn-primary"

                playView(files);

            }
        }
    }

});

function playView(files) {
    //Set new video source for player
    var player = videojs('my-video');

    data = []

    for(let i = 0; i < files.length; i++) {
        data[i] = {
            src: files[i][0],
            type: 'video/' + files[i][0].split(".").pop(),
            label: files[i][1]
        }
    }
    player.src(data);
}

function request(url) {
    //Made GET request and return answer
    var request = new XMLHttpRequest();
    request.open( "GET", url, false );
    request.send();
    return request.responseText;
}