function send_request(element, map_id) {
    var xhttp = new XMLHttpRequest();
    var request_type = element.id;
    var response=document.getElementById("response");
    if (request_type === "download") {
        xhttp.onload =function(){
        var filename = "";
        var disposition = xhttp.getResponseHeader('Content-Disposition');
        if (disposition && disposition.indexOf('attachment') !== -1) {
            var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            var matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '');
            }
        }
        var blob = this.response;
	    var a = document.createElement("a");
    	var blobUrl = window.URL.createObjectURL(new Blob([blob], {type: blob.type}));
        document.body.appendChild(a);
        a.style = "display: none";
        a.href = blobUrl;
        a.download = filename ;
        a.click();
	    }
        xhttp.open("GET", "maps/"+map_id+"/picture", true);
        xhttp.responseType = 'blob'
        xhttp.send();
    }

    else if (request_type === "delete") {
        xhttp.open("DELETE", "maps/"+map_id, true)
        xhttp.send();
        xhttp.onload =function(){
        if (xhttp.status === 204) {
            var map_tile = document.getElementById(map_id);
            map_tile.remove();
            }
        }
    }
    else if (request_type === "tags") {
       var tags = prompt("Enter Map Tags", "");
       var description = null;
       var index = null;
       if (!(tags == null || tags == "")) {
            xhttp.open("PUT", "maps/"+map_id, true)
            xhttp.send(tags);
            xhttp.onload =function(){
            if (xhttp.status === 200) {
                tags = xhttp.response;
                description = document.getElementById(map_id + " desc").innerHTML;
                index = description.search("Tags: ")+6;
                description = description.substring(0, index) + tags;
                document.getElementById(map_id + " desc").innerHTML = description;
            }
        }
       }
    }
}

function send_page(increment) {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var form = document.getElementById("searchform");
    var page = document.getElementById("page_id");
    var page_id = 1;
    if (page.value) {
      page_id = parseInt(page.value);
    }
    page_id = page_id + parseInt(increment);
    page.value = page_id;
    form.submit();
}

$(document).ready(function(){
  $("#homeicon").on('click touchstart', function() {
      var form = document.getElementById("searchform");
      var search = document.getElementById("searchbartext");
      search.value = "";
      var page = document.getElementById("page_id");
      page.value = 1;
      form.submit();
  });
});

$(document).ready(function(){
  $("#refreshicon").on('click touchstart', function() {
      var seed = Math.floor(Math.random() * 1000)+1;
      document.cookie = "seed="+seed.toString();
      var form = document.getElementById("searchform");
      form.submit();
  });
});

$('#searchform').submit(function() {
    var search = document.getElementById("searchbartext");
    var previous_value = document.getElementById("previous_value");
    var page = document.getElementById("page_id");
    if (search != previous_value) {
        page.value = 1;
        previous_value = search;
    }
    return true;
});