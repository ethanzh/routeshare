
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
    let sharedMapDiv = $(`#shared_result_map`);
    mapDiv.empty();
    sharedMapDiv.empty();

    // make ajax call with jquery, returns map URL
    $.ajax({
        url: "/{}/{}/to/{}/{}/".format(b1, b2, b3, b4),
        type: 'GET',
        dataType: "json",
        // add image with map url to div
        success(data) {
            let map_url = data[`map_url`];
            let img = document.createElement(`img`);
            img.src = map_url;
            mapDiv.append(img);

            let shared_map_url = data[`shared_url`];
            let shared_img = document.createElement(`img`);
            shared_img.src = shared_map_url;
            sharedMapDiv.append(shared_img);
        },
        // display error text
        error() {
            mapDiv.append(`Error occurred when processing the request`);
        }
    });
};