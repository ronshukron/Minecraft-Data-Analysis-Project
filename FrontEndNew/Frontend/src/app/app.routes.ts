import { Routes } from '@angular/router';
import { DatasetMainComponent } from './pages/dataset/dataset-main/dataset-main.component';
// import { AppComponent } from './app.component';
import { AboutComponent } from './pages/about/about.component';
import { SingleGameComponent } from './pages/singleGame/single-game/single-game.component';
import { Mp4PageComponent } from './pages/mp4/mp4-page/mp4-page.component';

export const routes: Routes = [
  { path: 'Dataset', component: DatasetMainComponent, title: 'Dataset Page' },
  { path: 'About', component: AboutComponent, title: 'About Page' },
  {
    path: 'SingleGame',
    component: SingleGameComponent,
    title: 'Single Game Page',
  },
  {
    path: 'MP4',
    component: Mp4PageComponent,
    title: 'Mp4 Page',
  },

  //   { path: '', component: AppComponent, title: 'Home Page' },
];
// path: 'Dataset', component: DatasetMainComponent
// path: '', component: AppComponent
