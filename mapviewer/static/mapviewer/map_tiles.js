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
        xhttp.open("GET", "maps/"+map_id, true);
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
}

$(document).ready(function(){
  $("#homeicon").on('click touchstart', function() {
      var form = document.getElementById("homeform");
      form.submit();
  });
});