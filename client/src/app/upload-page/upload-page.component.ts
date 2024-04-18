import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { PredictionService } from '../_services/prediction.service';
import { LoadingComponent } from '../loading/loading.component';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-upload-page',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, LoadingComponent],
  templateUrl: './upload-page.component.html',
  styleUrl: './upload-page.component.scss'
})
export class UploadPageComponent implements OnInit{
  uploadForm! : FormGroup;
  previewFile! : Blob;
  predictedFileURL! : string | ArrayBuffer | null;
  previewFileURL! : string | ArrayBuffer | null;
  range_value : number=0.8;
  isImageLoaded! : Subject<boolean>;
  
  constructor(private formBuilder : FormBuilder, private predictionService : PredictionService){
    this.isImageLoaded = new Subject<boolean>();
  }

  ngOnInit(): void {
    this.uploadForm = this.formBuilder.group({
      image : [null],
      link : [null],
      threshold : [this.range_value, Validators.required]
    }, {
      validators : [this.isFieldFilled()]
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

  //checks if at least one field is filled
  isFieldFilled() :  ValidatorFn {
    return (controls : AbstractControl) : ValidationErrors | null => {
      const image = controls.get("image")?.value ;
      const link = controls.get("link")?.value ;

      if (image || link){
        return {'isFilled' : true}
      }
      return null;
  }}

  //detects link blur to preview image
  onLinkBlur(event : any)  :void {
    this.previewFileURL = event.target.value;
  }


  //detects file selection to preview image
  onFileSelected(event : any) : void{
    this.previewFile = event.target.files[0]
    this.previewFileURL = URL.createObjectURL(this.previewFile);
  }


  //sends form to server
  submitForm() : void{
    this.predictionService.predict_image(this.uploadForm, this.previewFile)
    .pipe()
    .subscribe((blob : Blob) => {
        this.predictedFileURL = URL.createObjectURL(blob);
        this.isImageLoaded.next(true);
    })

  }
}
