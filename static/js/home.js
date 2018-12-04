
// From StackOverflow
String.prototype.format = function () {
  let i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] !== 'undefined' ? args[i++] : '';
  });
};

let submit = () => {

    // get text from
    let b1 = $(`#b1`).val();
    let b2 = $(`#b2`).val();
    let b3 = $(`#b3`).val();
    let b4 = $(`#b4`).val();

    // Clear current map div
    let mapDiv = $(`#result_map`);
    mapDiv.empty();

    // make ajax call with jquery, returns map URL
    $.ajax({
        url: "/{}/{}/to/{}/{}/".format(b1, b2, b3, b4),
        type: 'GET',
        // add image with map url to div
        success(response) {
            let map_url = response;
            let img = document.createElement(`img`);
            img.src = map_url;
            mapDiv.append(img);
        },
        // display error text
        error() {
            mapDiv.append(`Error occurred when processing the request`);
        }
    });
};