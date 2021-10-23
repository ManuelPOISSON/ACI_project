var map = L.map('map').setView([48.1125, -1.6474], 13);
var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
const points1 = [
    [48.1125, -1.6474, 0.5],
    [48.11, -1.6474, 1],
    [48.12, -1.64, 0.2],
    [48.1125, -1.65, 0.75],
];
const points2 = [
    [48.1125, -1.6474, 0.75],
    [48.11, -1.6474, 0.75],
    [48.12, -1.64, 0.5],
    [48.1125, -1.65, 0.4],
];
const points3 = [
    [48.1125, -1.6474, 0.5],
    [48.11, -1.6474, 0.2],
    [48.12, -1.64, 0.5],
    [48.1125, -1.65, 0.2],
];
const points = [points1, points2, points3];
const heat = L.heatLayer(points1, { maxZoom: 13, radius: 75, blur: 50 });
heat.addTo(map);

const slider = document.getElementById("slider");
const timeText = document.getElementById("timeText");

function updateMap(value) {
    timeText.innerHTML = value;
    heat.setLatLngs(points[value]);
}
updateMap(slider.value); // Initial init

slider.oninput = function() {
    updateMap(this.value);
}
