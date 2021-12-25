import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  host = "apisvc:5000";
  path = "/message";
  coords=[];
  constructor( private http : HttpClient) { }

  GetCoords() {
    this.http.get<any>(this.host + this.path).subscribe(
      res => {
        console.log("response:",res);
        this.coords = res;
      })
  }
}
