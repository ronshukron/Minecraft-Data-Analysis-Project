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
  ],
})
export class SingleGameComponent {
  public afterApply: boolean = false;
  public afterApply_image: boolean = true;
  public typeOfTask: string = '';
  dataSetToShow: any;
  // public game: string = '';
  // public gamesOptions: string[] = [];

  constructor(
    public dataService: DataService,
    private router: Router,
  ) {}

  public onFilterChanged(filters: ISingleGameFilters) {
    console.log(filters);
    if (!filters) return;
    // this.restart_args();
    this.typeOfTask = filters.selectedTask;
    // this.dataService.getSingleGameData(filters).subscribe(
    //   (data: getIDataset) => {
    //     this.dataSetToShow.states = data.states;
    //     let image: IDatasetImages;
    //     for (image of data.images) {
    //       if (image) {
    //         this.dataSetToShow.images.push(arrayBufferToBase64(image.data));
    //       }
    //     }
    //     this.afterApply_image = true;
    //   },
    //   (error) => {
    //     console.error('Error fetching data:', error);
    //   },
    // );
    // this.getListOfGames(filters);
  }

  // private getListOfGames(filters: ISingleGameFilters): void {
  //   this.dataService.getSingleGameList(filters).subscribe(
  //     (data: string[]) => {
  //       this.gamesOptions = data;
  //       this.afterApply = true;
  //     },
  //     (error) => {
  //       console.error('Error cant load the list of games:', error);
  //     },
  //   );
  // }

  // private restart_args(): void {
  //   this.afterApply_image = false;
  //   this.dataSetToShow.images = [];
  // }

  public goToMP4Page() {
    console.log(this.typeOfTask);
    this.router.navigateByUrl(`/MP4/${this.typeOfTask}`);
  }
  // public applyFilter(filterValue: string) {
  //   this.filteredGames = this.games.filter(game => game.toLowerCase().includes(filterValue.toLowerCase()));
  // }
}
