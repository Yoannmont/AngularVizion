import { Routes } from '@angular/router';
import { UploadPageComponent } from './upload-page/upload-page.component';
import { AboutPageComponent } from './about-page/about-page.component';

export const routes: Routes = [
  { path: '', component: UploadPageComponent },
  {path:'about', component : AboutPageComponent},
];
