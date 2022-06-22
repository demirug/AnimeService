$(document).ready(function () {
    $("#review > button").click(function () {

        var text = CKEDITOR.instances.id_text.getData();

        if(text.length === 0) return;

        var formdata = new FormData();
        formdata.append("season", season_pk);
        formdata.append("text", text);

        var rqs = request("/api/v1/movie/review/", "POST", formdata);
        var answer = JSON.parse(rqs.responseText);

        if(rqs.status === 400) {
            // Show all errors in modal
            var modal = new MainModal().setTitle("Error").addFooterCloseButton();
            for (var i in answer) {
                for(var j = 0; j < answer[i].length; j++) {
                    modal.addToBody("<p>" + answer[i][j] + "</p>");
                }
            }

            modal.show();
        } else if(rqs.status === 201) {
            CKEDITOR.instances.id_text.setData("");
            // Add review
            var htmlObject = $("<p>" + username + ": " + answer.text + " | Date: " + answer.datetime + "</p>");
            $('#review-list').prepend(htmlObject);
            $('body, html').animate({ scrollTop: $(htmlObject).offset().top }, 1000);
        }
    });
})