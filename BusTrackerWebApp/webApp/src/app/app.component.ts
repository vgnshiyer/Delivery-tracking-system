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
    
    let mapmarkers1 = [73.00621032714844,19.114029215761995];
    let mapmarkers2 = [73.00981521606445,19.073637115022702];
    this.InitMap(mapmarkers1,mapmarkers2);
    this.timerSubscription = timer(0, 5000).pipe(
      map(() => {
        this.test();
      })
    ).subscribe();
  }

  InitMap(coords1: any,coords2: any){
    let coords = [19.0330, 73.0297];
    let mapid = L.map('map').setView(coords, 12);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJheDI1MDciLCJhIjoiY2t4azgyOXBxNmRwaDJ1cTNjMGRqcjF3ZCJ9.0pJi--39nsT8km17AeiY3g'
    }).addTo(mapid);
    // coord 1
    var geojson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"marker-color":"#6b9cd1","marker-size":"medium","marker-symbol":""},"geometry":{"type":"Point","coordinates":coords1}}]};
    //using geojson with leaflet
    L.geoJSON(geojson).addTo(mapid);
    // coord 2
    var geojson = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"marker-color":"#6b9cd1","marker-size":"medium","marker-symbol":""},"geometry":{"type":"Point","coordinates":coords2}}]};
    L.geoJSON(geojson).addTo(mapid);
  }

  CallApi(){
    this.apiService.GetCoords();
  }

  test(){
    console.log("calling again and again");
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }
}
