import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class LoaderService {
    //Handles loading spinner 
    isLoading = new Subject<boolean>();
    show() {
        this.isLoading.next(true);
    }
    hide() {
        this.isLoading.next(false);
    }
}