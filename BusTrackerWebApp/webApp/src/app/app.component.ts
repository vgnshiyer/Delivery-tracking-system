import { Component, OnInit } from '@angular/core';
declare const L: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent  implements OnInit{
  title = 'BusTrackerApp';

  ngOnInit() {
    let coords = [73.00689697265625, 19.111920635169675];
    let map = L.map('map').setView([42.35, -71.08], 3);
    var geojson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[73.00621032714844,19.114029215761995],[73.0066394805908,19.113542622627477],[73.01118850708008,19.09898471586908],[73.01178932189941,19.09825475923873],[73.01183223724365,19.097281478722696],[73.01226139068604,19.097119264746816],[73.01234722137451,19.094969914555854],[73.01187515258789,19.091482230326],[73.01105976104736,19.09103612587957],[73.00282001495361,19.078788061593617],[73.00243377685547,19.073880470433167],[72.99762725830078,19.074448298334378],[72.99818515777588,19.079274756925756],[73.0006742477417,19.083087154220646],[73.00539493560791,19.090387244538764],[73.0058240890503,19.096510960921176],[73.00080299377441,19.112447782838753],[73.00586700439453,19.113907567612614]]}}]};
    //using geojson with leaflet
    
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJheDI1MDciLCJhIjoiY2t4azgyOXBxNmRwaDJ1cTNjMGRqcjF3ZCJ9.0pJi--39nsT8km17AeiY3g'
    }).addTo(map);
    let marker = L.marker([42.35, -71.08]).addTo(map);
    L.geoJSON(geojson).addTo(map);
  }
}
