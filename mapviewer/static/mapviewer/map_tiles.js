function send_request(element, map_id) {
    //TODO: Refactor how sending requests work
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
    //TODO: Add a handling for request type "Forge"
}

function get_search() {
    const query_parameters = new URLSearchParams(location.search);
    const search = document.getElementById("searchbartext").value;
    query_parameters.set("search", search);
    query_parameters.set("page", "1");
    window.location = `${location.pathname}?${query_parameters}`;
}

function send_page(increment) {
    const query_parameters = new URLSearchParams(location.search);
    query_parameters.set("search", query_parameters.get("search"));
    if(query_parameters.has("page")) {
        let page = parseInt(query_parameters.get("page"));
        query_parameters.set("page", (page+increment).toString());
    }
    else {
        query_parameters.set("page", "2");
    }
    window.location = `${location.pathname}?${query_parameters}`;
}

$(document).ready(function(){
  $("#searchicon").on('click touchstart', function() {
      get_search();
  });
});

window.addEventListener("keydown", function(event) {
    if(event.key === "Enter") {
        get_search();
    }
}, true);

$(document).ready(function(){
  $("#refreshicon").on('click touchstart', function() {
      var seed = Math.floor(Math.random() * 1000)+1;
      document.cookie = "seed="+seed.toString();
      location.reload();
  });
});