import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {

  private readonly BASE_URL : string = 'http://localhost:5000';
  constructor(private httpClient : HttpClient) { }

  predict_image(form : FormGroup) : Observable<any> {
    
    if (form.contains('image')){
      const headers = new HttpHeaders().set('Content-Type', 'mulipart/form-data')
      return this.httpClient.post<any>(this.BASE_URL + '/predict', {'file' : form.controls['image'].value}, {'headers' : headers});
    }
    else{
      console.log(form.controls['link'])
      const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
      return this.httpClient.post<any>(this.BASE_URL + '/predict', {link : form.controls['link'].value}, {'headers' : headers});
    }
  }

}
