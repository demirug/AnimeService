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

            var date = new Date(answer.datetime)

            // Add review
            var htmlObject = $("                    <div class=\"card mb-4\">\n" +
                "                      <div class=\"card-body\">\n" +
                "                        " + answer.text + "\n" +
                "                        <div class=\"d-flex justify-content-between\">\n" +
                "                          <div class=\"d-flex flex-row align-items-center\">\n" +
                "                            <img src=\"" + user_logo + "\" alt=\"avatar\" width=\"25\" height=\"25\" />\n" +
                "                            <p class=\"small mb-0 ms-2\">" + username + "</p>\n" +
                "                          </div>\n" +
                "                            <time class=\"small mb-0 ms-2 text-center\">" + `${$.datepicker.formatDate("M d", date)}, ${date.getFullYear()} at ${date.getHours()}:${date.getMinutes()}` + "</time>\n" +
                "                        </div>\n" +
                "                      </div>\n" +
                "                    </div>")
            $('#review-list').prepend(htmlObject);
            $('body, html').animate({ scrollTop: $(htmlObject).offset().top }, 300);
        }
    });
})