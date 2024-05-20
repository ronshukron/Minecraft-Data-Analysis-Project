import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { DatasetMainComponent } from '../../dataset/dataset-main/dataset-main.component';
import { RouterModule } from '@angular/router';
import { AboutComponent } from '../../about/about.component';
import { SingleGameComponent } from '../../singleGame/single-game/single-game.component';
import { Mp4PageComponent } from '../../mp4/mp4-page/mp4-page.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [
    MatToolbarModule,
    DatasetMainComponent,
    RouterModule,
    AboutComponent,
    SingleGameComponent,
    Mp4PageComponent,
  ],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {}
