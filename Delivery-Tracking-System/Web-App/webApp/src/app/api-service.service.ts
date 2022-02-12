import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {

  host = "apisvc:5000";
  path = "/message";
  coords=[];
  constructor() { }

  GetCoordEvents(url: string): Observable<string> {
    return new Observable<string>((obs: { next: (arg0: any) => void; }) => {
      const source = new EventSource(url);
      source.addEventListener('message', (evt) => {
        // console.log(evt.data);
        obs.next(evt.data);
      });
      source.onerror = (error) => {
        console.log('connection error');
        console.log(error);
        source.close();
      }
    });
    
    // source.addEventListener('message', message =>{
    //   console.log('message recvd (event listener)');
    //   console.log(message)
    //   console.log(message.data);
    //   // return message.data
    //   // this.coords = JSON.parse(message.data)
    // });
    // source.onmessage = (message) => {
    //   console.log('message recvd');
    //   console.log(message.data);
    // }
    // source.onerror = (e) => {
    //   console.log('connection error');
    //   console.log(e);
    //   source.close();
    // }
  }
}
