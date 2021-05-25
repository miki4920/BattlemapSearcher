function send_request(element, map_id, code) {
    let xhttp = new XMLHttpRequest();
    if (code === 0) {
        let temp_input = document.createElement("input");
        temp_input.value = "http://" + window.location.hostname + "/maps/" + map_id;
        document.body.appendChild(temp_input);
        temp_input.select();
        document.execCommand("copy");
        document.body.removeChild(temp_input);
        let temp_value = element.innerHTML;
        element.innerHTML = "Copied";
        setTimeout(function() {
            element.innerHTML = temp_value;
        }, 1000);
    } else if (code === 1) {
        let tags = prompt("Enter Map Tags");
        let description = null;
        let index = null;
        if (!(tags == null || tags === "")) {
            xhttp.open("PUT", "maps/" + map_id, true)
            xhttp.send(tags);
            xhttp.onload = function () {
                if (xhttp.status === 200) {
                    tags = xhttp.response;
                    description = document.getElementById(map_id + " desc").innerHTML;
                    index = description.search("Tags: ") + 6;
                    description = description.substring(0, index) + tags;
                    document.getElementById(map_id + " desc").innerHTML = description;
                }
            }
        }
    } else if (code === 2) {
        xhttp.open("DELETE", "maps/" + map_id, true)
        xhttp.send();
        xhttp.onload = function () {
            if (xhttp.status === 204) {
                document.getElementById(map_id).remove();
            }
        }
    }
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
    if(query_parameters.has("search")) {
         query_parameters.set("search", query_parameters.get("search"));
    }
   else {
        query_parameters.set("search", "");
    }
    if (query_parameters.has("page")) {
        let page = parseInt(query_parameters.get("page"));
        query_parameters.set("page", (page + increment).toString());
    } else {
        query_parameters.set("page", "2");
    }
    window.location = `${location.pathname}?${query_parameters}`;
}

$(document).ready(function () {
    $("#searchicon").on('click touchstart', function () {
        get_search();
    });
});

window.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        get_search();
    }
}, true);

$(document).ready(function () {
    $("#refreshicon").on('click touchstart', function () {
        var seed = Math.floor(Math.random() * 1000) + 1;
        document.cookie = "seed=" + seed.toString();
        location.reload();
    });
});