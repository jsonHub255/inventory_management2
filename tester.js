function calculateDaysBetweenDates(begin, end) {
    var beginDate = new Date(begin);
    var endDate = new Date(end);
    var diff = endDate.getTime() - beginDate.getTime();
    return diff / (1000 * 60 * 60 * 24);
}
// find all images without alternate text
// and give them a red border
function process() {    
    var images = document.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        var image = images[i];
        if (image.alt == "") {
            image.style.border = "2px solid red";
        }
    }
}