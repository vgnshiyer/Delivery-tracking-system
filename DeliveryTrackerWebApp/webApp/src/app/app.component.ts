import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from './api-service.service';
import { map, Subscription, timer } from 'rxjs';

declare const L: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent  implements OnInit{
  title = 'BusTrackerApp';

  constructor(private apiService: ApiServiceService){
    
  }
  timerSubscription: Subscription = new Subscription;
  ngOnInit() {
    
    let mapmarkers1: Array<any> = [];
    let mapmarkers2 = [73.00981521606445,19.073637115022702];
    let coords = [19.0330, 73.0297];
    let map = L.map('map').setView(coords, 12);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJheDI1MDciLCJhIjoiY2t4azgyOXBxNmRwaDJ1cTNjMGRqcjF3ZCJ9.0pJi--39nsT8km17AeiY3g'
    }).addTo(map);
    // coord 2
    // var geojson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"marker-color":"#6b9cd1","marker-size":"medium","marker-symbol":""},"geometry":{"type":"Point","coordinates":mapmarkers2}}]};
    // L.geoJSON(geojson).addTo(mapid);
    //making api call to get coordinates for vehicle 1
    this.apiService.GetCoordEvents('http://sampleapi:5000/messages').subscribe((message: any) => {
      let res = JSON.parse(message);
      let coords = res.coordinates;
      console.log(coords);
      for (var i = 0; i < mapmarkers1.length; i++) {
        map.removeLayer(mapmarkers1[i]);
      }
      let marker1 = L.marker([coords.longitude,coords.latitude]).addTo(map);
      mapmarkers1.push(marker1);
    });
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }
}
