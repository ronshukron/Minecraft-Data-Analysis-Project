import { Component } from '@angular/core';
import { SingleGameFiltersComponent } from '../single-game-filters/single-game-filters.component';
import { DataService } from '../../data-service';
import {
  IDatasetFilters,
  ISingleGameFilters,
} from '../../../Interfaces/IdatasetFilters';
import { IDatasetImages, getIDataset } from '../../../Interfaces/Idataset';
import { arrayBufferToBase64 } from '../../../utilityFunctions/arrayBufferToBase64';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { Mp4PageComponent } from '../../mp4/mp4-page/mp4-page.component';
import { RouterModule } from '@angular/router';
import { concatAll, filter } from 'rxjs';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {
  IsingleGameData,
  IsingleGameDataFromAPI,
} from '../../../Interfaces/IsingleGameData';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-single-game',
  standalone: true,
  templateUrl: './single-game.component.html',
  styleUrl: './single-game.component.css',
  imports: [
    SingleGameFiltersComponent,
    MatButtonModule,
    Mp4PageComponent,
    RouterModule,
    MatCardModule,
    MatSelectModule,
    MatSliderModule,
    MatButtonModule,
    FormsModule,
    CommonModule,
    MatProgressSpinnerModule,
  ],
})
export class SingleGameComponent {
  public afterApply: boolean = false;
  public loading: boolean = false;
  public afterApply_image: boolean = true;
  private filters: ISingleGameFilters = {
    selectedTask: '',
    game: '',
    inventory: [],
    action: [],
  };
  public data: IsingleGameData = {
    images: [],
    data_points: [],
  };

  constructor(
    public dataService: DataService,
    private router: Router,
  ) {}

  public onFilterChanged(filters: ISingleGameFilters) {
    if (!filters) return;
    this.filters = filters;
    this.dataService.gameName = filters.game;
    this.restart_args();
    this.loading = true;
    this.dataService.getSingleGameData(filters).subscribe(
      (data: IsingleGameDataFromAPI) => {
        this.data.data_points = data.data_points;
        this.setImageFromAPI(data);
        this.afterApply = true;
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching data:', error);
      },
    );
  }

  public goToMP4Page() {
    console.log(this.filters.selectedTask);
    this.router.navigateByUrl(`/MP4/${this.filters.selectedTask}`);
  }

  private setImageFromAPI(data: IsingleGameDataFromAPI): void {
    let dataSetToShow: { images: string[] } = { images: [] };
    let image: IDatasetImages;
    for (image of data.images) {
      if (image && image.data) {
        dataSetToShow.images.push(arrayBufferToBase64(image.data));
      }
    }
    this.data.images.push(...dataSetToShow.images);
    this.afterApply_image = true;
  }

  private restart_args(): void {
    this.afterApply = false;
    this.data.data_points = [];
    this.data.images = [];
  }
}

// public applyFilter(filterValue: string) {
//   this.filteredGames = this.games.filter(game => game.toLowerCase().includes(filterValue.toLowerCase()));
// }
