function show(id, show) {
    document.getElementById(id).classList.toggle("hidden", !show);
}

function checkFocus() {
    var element = document.getElementById("searchItem");
    var empty = (element.value == "")
    element.classList.toggle("notEmpty", !empty)
}

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

function update_item(id) {

    var item = document.getElementById("item_" + id)
    var item_href = document.getElementById("item_" + id + "_href")
    var item_isMagic = document.getElementById("item_" + id + "_isMagic")

    document.getElementById("update_name").value = item.cells[0].textContent
    document.getElementById("update_description").value = item.cells[1].textContent
    document.getElementById("update_location").value = item.cells[2].textContent
    document.getElementById("update_price").value = parseFloat(item.cells[3].textContent.replace(",",""))
    document.getElementById("update_weight").value = parseFloat(item.cells[4].textContent.replace(",",""))
    document.getElementById("update_quantity").value = parseInt(item.cells[5].textContent)
    document.getElementById("update_type").value = item.cells[6].textContent
    if (item.cells[7].textContent == "Yes") {
        document.getElementById("update_isMagic").checked = true
    } else {
        document.getElementById("update_isMagic").checked = false
    }
    if (item_href != null) {
        document.getElementById("update_href").value = item_href.href
    } else {
        document.getElementById("update_href").value = ""
    }

    document.getElementById("update_item_form").action = "/update/" + id

    show("update_item", true)
}

function sell_item(id) {

    var item = document.getElementById("item_" + id)
    var item_quantity = parseInt(item.cells[5].textContent)

    document.getElementById("sell_name").textContent = item.cells[0].textContent
    document.getElementById("sell_available").textContent = "Available units: " + parseInt(item.cells[5].textContent)
    document.getElementById("sell_price").textContent = "Price per unit: " + item.cells[3].textContent + " g"

    document.getElementById("sell_quantity").max = parseInt(item.cells[5].textContent)

    document.getElementById("sell_item_form").action = "/sell/" + id

    show("sell_item", true)
}

function delete_item(id) {

    var item = document.getElementById("item_" + id)
    var item_quantity = parseInt(item.cells[5].textContent)

    document.getElementById("delete_name").textContent = item.cells[0].textContent

    document.getElementById("delete_item_form").action = "/delete/" + id

    show("delete_item", true)
}

function update_checkbox_value(id) {
    document.getElementById("item_" + id).value = document.getElementById("quantity_" + id).value
}

function bulk_sell_item() {

    var sell_table = document.getElementById("sell_table");
    sell_table.innerHTML = ""   // Certify that table is empty
    var form = document.forms["sell_items_form"]

    var sell_total = 0
    var quantity_total = 0

    for (var item of form) {

        if (!item.checked) {
            continue
        }

        var id = item.name.split("_")[1]

        var row = sell_table.insertRow()

        // Adding quantity
        var quantity = document.getElementById("quantity_" + id).valueAsNumber
        var cell = row.insertCell()
        var text = document.createTextNode(quantity)
        cell.appendChild(text)

        // Adding name
        var name = document.getElementById("name_" + id).textContent
        cell = row.insertCell()
        text = document.createTextNode(name)
        cell.appendChild(text)

        // Adding price
        var price = document.getElementById("price_" + id).textContent
        cell = row.insertCell()
        text = document.createTextNode(price)
        cell.appendChild(text)

        quantity_total += quantity
        sell_total += (quantity * parseFloat(price.replace(",", "")))
    }

    if (quantity_total > 0) {

        // Creating table header
        var head = sell_table.createTHead()
        var row = head.insertRow()

        var th = document.createElement("th")
        var text = document.createTextNode("Quantity")
        th.appendChild(text)
        row.appendChild(th)

        th = document.createElement("th")
        text = document.createTextNode("Item")
        th.appendChild(text)
        row.appendChild(th)

        th = document.createElement("th")
        text = document.createTextNode("Price / Unit")
        th.appendChild(text)
        row.appendChild(th)

        document.getElementById("sell_price_total").textContent = "Selling " + quantity_total + " items for a total of: " + Intl.NumberFormat('en-IN').format(sell_total) + " g"

        show("bulk_sell_item", true)

    }
}
