import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { provideHttpClient } from '@angular/common/http';

bootstrapApplication(AppComponent, appConfig).catch((err) =>
  console.error(err),
);

platformBrowserDynamic()
  .bootstrapModule(AppComponent)
  .catch((err) => console.error(err));

// bootstrapApplication(AppComponent, {
//   providers: [provideHttpClient()],
// });
// import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
// import { AppComponent } from './app/app.component';

// platformBrowserDynamic().bootstrapModule(AppComponent)
//   .catch(err => console.error(err));
