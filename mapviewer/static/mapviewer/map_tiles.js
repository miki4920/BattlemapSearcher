function send_request(element, map_id) {
    let xhttp = new XMLHttpRequest();
    let request_type = element.id;
    if (request_type === "delete") {
        xhttp.open("DELETE", "maps/"+map_id, true)
        xhttp.send();
        xhttp.onload =function(){
        if (xhttp.status === 204) {
            document.getElementById(map_id).remove();
            }
        }
    }
    else if (request_type === "tags") {
       let tags = prompt("Enter Map Tags");
       let description = null;
       let index = null;
       if (!(tags == null || tags === "")) {
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

window.onscroll = function() {addSticky()};
var searchbar = document.getElementById("searchbar");
var sticky = searchbar.offsetTop;
function addSticky() {
  if (window.pageYOffset >= sticky) {
    searchbar.classList.add("sticky")
  } else {
    searchbar.classList.remove("sticky");
  }
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