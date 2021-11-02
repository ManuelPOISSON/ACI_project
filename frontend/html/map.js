var map = L.map('map').setView([48.1125, -1.6474], 13);
var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);
const heat = L.heatLayer([], { maxZoom: 13, radius: 75, blur: 50 });
heat.addTo(map);

const slider = document.getElementById("slider");
const timeText = document.getElementById("timeText");

const now = new Date;
slider.max = now.getHours();

function reqListener () {
    if (this.readyState == 4 && this.status == 200) {
        var layer = [];
        this.response.forEach(element => {
            layer.push([element.lat, element.lng, element.lvl]);
        });
        heat.setLatLngs(layer);
    }
}

function updateMap(value) {
    var hours = parseInt(value);
    timeText.innerHTML = hours + "h";
    var start = new Date();
    start.setHours(hours, 0, 0, 0);
    var end = new Date();
    end.setHours(hours + 1, 0, 0, 0);

    var req = new XMLHttpRequest();
    req.responseType = 'json';
    req.onload = reqListener;
    req.open("get", "http://127.0.0.1:8000/map?start=" + start.toISOString().slice(0, 19).replace('T', ' ') + "&end=" + end.toISOString().slice(0, 19).replace('T', ' '), true);
    req.send();
      
}
updateMap(slider.value); // Initial init

slider.oninput = function() {
    updateMap(this.value);
}
