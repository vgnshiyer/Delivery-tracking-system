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
      (      res: never[]) => {
        console.log("response:",res);
        this.coords = res;
      })
  }

  GetCoordEvents() {
    let source = new EventSource('http://localhost:5000/messages')
    source.addEventListener('message', message =>{
      console.log(message.data);
      // this.coords = JSON.parse(message.data)
    });
    source.onmessage = (message) => {
      console.log('message recvd');
      console.log(message.data);
    }
    source.onerror = (e) => {
      console.log('connection error');
      console.log(e);
      source.close();
    }
  }
}
