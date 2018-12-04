
// From StackOverflow
String.prototype.format = function () {
  let i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] !== 'undefined' ? args[i++] : '';
  });
};

let submit = () => {

    let b1 = document.getElementById(`b1`).value;
    let b2 = document.getElementById(`b2`).value;
    let b3 = document.getElementById(`b3`).value;
    let b4 = document.getElementById(`b4`).value;

    // make ajax call with jquery, returns map URL
    $.ajax({
        url: "/{}/{}/to/{}/{}/".format(b1, b2, b3, b4),
        success: function(response){
            let mapDiv = $(`#result_map`);
            mapDiv.empty();
            let map_url = response;

            let img = document.createElement("img");    // Create with DOM
            img.src = map_url;

            mapDiv.append(img);
        }
    });
};