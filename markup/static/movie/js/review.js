$(document).ready(function () {
    $("#review > button[type=button]").click(function () {

        var text = CKEDITOR.instances.id_text.getData();

        var rqs = request("/api/v1/movie/review/", "POST", "season=" + season_pk + "&text=" + text);
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
            $("#review-list").prepend("<p>" + username + ": " + answer.text + " | Date: " + answer.datetime + "</p>")
        }
    });
})