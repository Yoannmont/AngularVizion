import { AsyncPipe, CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { PredictionService } from '../_services/prediction.service';
import { LoadingComponent } from '../loading/loading.component';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-upload-page',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, LoadingComponent, AsyncPipe],
  templateUrl: './upload-page.component.html',
  styleUrl: './upload-page.component.scss'
})
export class UploadPageComponent implements OnInit{
  uploadForm! : FormGroup;
  previewFile! : Blob;
  predictedFileURL! : string | ArrayBuffer | null;
  previewFileURL! : string |ArrayBuffer | null;
  range_value : number=0.8;
  isImageLoaded! : Subject<boolean>;
  
  constructor(private formBuilder : FormBuilder, private predictionService : PredictionService){
    this.isImageLoaded = new Subject<boolean>();
  }

  ngOnInit(): void {
    this.uploadForm = this.formBuilder.group({
      image : [null, Validators.required],
      link : [null, Validators.required],
      threshold : [this.range_value, Validators.required]
    })

      //reset image if link is filled
     this.uploadForm.controls['link'].valueChanges.subscribe(value => {
      if (value) {
        this.uploadForm.controls['image'].reset(null);
      }
    });

    //reset link if image is filled
    this.uploadForm.controls['image'].valueChanges.subscribe(value => {
      if (value) {
        this.uploadForm.controls['link'].reset(null);
      }
    });
  }

  selectFile(event : any) : void{
    this.previewFile = event.target.files[0]
    this.previewFileURL = URL.createObjectURL(this.previewFile);



  }



  submitForm() : void{
    this.predictionService.predict_image(this.uploadForm, this.previewFile)
    .pipe()
    .subscribe((blob : Blob) => {
        this.predictedFileURL = URL.createObjectURL(blob);
        this.isImageLoaded.next(true);

    })

  }
}