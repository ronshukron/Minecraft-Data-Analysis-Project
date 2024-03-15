import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './pages/navbar/navbar/navbar.component';
import { DatasetMainComponent } from './pages/dataset/dataset-main/dataset-main.component';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [RouterOutlet, NavbarComponent, DatasetMainComponent],
})
export class AppComponent {
  title = 'final-project';
}
