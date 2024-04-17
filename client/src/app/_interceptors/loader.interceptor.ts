import { HttpInterceptorFn } from '@angular/common/http';
import { LoaderService } from '../_services/loader.service';
import { inject } from '@angular/core';
import { finalize } from 'rxjs';

export const loaderInterceptor: HttpInterceptorFn = (req, next) => {

  //Loading interceptor => shows loading spinner when awaiting HTTP response
  const loaderService = inject(LoaderService);

  loaderService.show();
  return next(req).pipe(finalize(() => loaderService.hide()));

};
