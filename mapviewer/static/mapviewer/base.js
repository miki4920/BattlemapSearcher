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