import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {
  //handles image prediction HTTP request
  private readonly BASE_URL : string = 'http://localhost:5000';
  constructor(private httpClient : HttpClient) { }

  predict_image(form : FormGroup, file : Blob, lang : string) : Observable<any> {
    const formData = new FormData();
    formData.append('threshold', form.controls['threshold'].value)
    formData.append('lang', lang);
    
    if (form.controls['image'].value !== null){
      formData.append('file', file);
      const headers = new HttpHeaders()
      return this.httpClient.post(this.BASE_URL + '/predict', formData, {headers : headers, responseType : "blob"});
    }
    else{
      formData.append("link", form.controls['link'].value)
      const headers = new HttpHeaders()
      return this.httpClient.post(this.BASE_URL + '/predict', formData, {headers: headers, responseType : "blob"});
    }
  }

}
