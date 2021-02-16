function searchItem() {
  var filter = document.getElementById("searchItem").value.toUpperCase();
  var items = document.getElementById("itemTable").getElementsByTagName("tr");

  // Loop through all items, hide those that don't match the search query
  for (var i = 1; i < items.length; i++) { // Skip header

        var name = items[i].getElementsByTagName("td")[0]; // item name field
        var nameValue = name.textContent || name.innerText;

        var location = items[i].getElementsByTagName("td")[2]; // item location field
        var locationValue = location.textContent || location.innerText;

        var type = items[i].getElementsByTagName("td")[6]; // item type field
        var typeValue = type.textContent || type.innerText;

        if (nameValue.toUpperCase().indexOf(filter) > -1 ||
            typeValue.toUpperCase().indexOf(filter) > -1 ||
            locationValue.toUpperCase().indexOf(filter) > -1) {

          items[i].style.display = "";

        } else {

          items[i].style.display = "none";

        }
    }
}

function checkFocus() {
    var element = document.getElementById("searchItem");
    var empty = (element.value == "")
    element.classList.toggle("notEmpty", !empty)
}

function show(id, show) {
    document.getElementById(id).classList.toggle("hidden", !show);
}
