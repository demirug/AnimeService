document.addEventListener('DOMContentLoaded', function(){

    let avatar = document.getElementById("avatar");
    let upload = document.getElementById("upload");

    let form = document.getElementById("user_form");
    let avatar_input = document.getElementById("id_avatar");

    avatar.addEventListener("mouseenter", function( event ) {
       avatar.style.display = "none";
       upload.style.display = "block";
    });

    upload.addEventListener("mouseleave", function( event ) {
           upload.style.display = "none";
           avatar.style.display = "block";
    });

    upload.addEventListener("click", function ( event ) {
        avatar_input.click();
    });

    avatar_input.addEventListener("change", function ( event ) {
        form.submit();
    });

});