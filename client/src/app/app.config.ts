import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { HttpClient, provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { loaderInterceptor } from './_interceptors/loader.interceptor';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes), 
    provideHttpClient(withFetch(), withInterceptors([loaderInterceptor])),
    importProvidersFrom(TranslateModule.forRoot(
      {
        loader: {
          provide : TranslateLoader,
          useFactory : HttpLoaderFactory, 
          deps:[HttpClient]},
        defaultLanguage: 'en',
        
      }
    ))
   ]
};

export function HttpLoaderFactory(http : HttpClient) : TranslateHttpLoader{
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}