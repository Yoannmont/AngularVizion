import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { PredictionService } from '../_services/prediction.service';

@Component({
  selector: 'app-upload-page',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './upload-page.component.html',
  styleUrl: './upload-page.component.scss'
})
export class UploadPageComponent implements OnInit{
  uploadForm_file! : FormGroup;
  uploadForm_link! : FormGroup;
  constructor(private formBuilder : FormBuilder, private predictionService : PredictionService){}

  ngOnInit(): void {
    this.uploadForm_file = this.formBuilder.group({
      image : [null, Validators.required]
    })
    this.uploadForm_link = this.formBuilder.group({
      link : [null, Validators.required]
    })
  }

  submitForm(form : FormGroup) : void{
    this.predictionService.predict_image(form).subscribe();
  }
}
