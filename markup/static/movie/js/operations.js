function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function request(url, type = "GET") {
    var request = new XMLHttpRequest();
    request.open(type, url, false );
    if(type === "POST") {
        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
    request.send();
    return request.responseText;
}
