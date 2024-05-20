import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { IDatasetFilters } from '../../../Interfaces/IdatasetFilters';
import { DatasetFiltersComponent } from '../dataset-filters/dataset-filters.component';
import { DataService } from '../../data-service';
import {
  IDatasetData,
  IDatasetImages,
  IStats,
  IStats_new,
  getIDataset,
} from '../../../Interfaces/Idataset';
import { arrayBufferToBase64 } from '../../../utilityFunctions/arrayBufferToBase64';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-dataset-main',
  standalone: true,
  templateUrl: './dataset-main.component.html',
  styleUrl: './dataset-main.component.css',
  imports: [DatasetFiltersComponent, MatProgressSpinnerModule],
})
export class DatasetMainComponent implements OnInit {
  public afterApply: boolean = false;
  public afterApply_image: boolean = false;
  public loading: boolean = false;

  public data: IDatasetData = {
    images: [],
    stats: [],
  };

  private filters: IDatasetFilters = {
    datasetSize: 10,
    selectedTask: '',
    inventory: [],
    action: [],
    key: [],
  };

  constructor(public dataService: DataService) {}

  ngOnInit(): void {}

  public onFilterChanged(filters: IDatasetFilters) {
    if (!filters) return;
    this.filters = filters;
    this.restart_args();
    this.loading = true;
    this.dataService.getDataSetDataGraphAndStatistics(filters).subscribe(
      (data: getIDataset) => {
        this.data.stats = data.stats;
        this.setImageFromAPI(data);
        this.afterApply = true;
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching data:', error);
      },
    );
  }

  private restart_args(): void {
    this.afterApply = false;
    this.data.stats = [];
    this.data.images = [];
  }

  private setImageFromAPI(data: getIDataset): void {
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
}

// public onFilterChanged(filters: IDatasetFilters) {
//   if (!filters) return;
//   console.log(filters);
//   this.afterApply_image = false;
//   this.afterApply = true;
//   this.dataSetToShow.images = [];
//   this.dataSetToShow.avg = 0;
//   (this.dataSetToShow.minMax = { min: 0, max: 100 }),
//     (this.dataSetToShow.stdDeviation = 0);
//   this.dataService.getDataSetFilters(filters).subscribe(
//     (data: getIDataset) => {
//       console.log(data);
//       console.log(data.stats);
//       console.log(data.images);
//       this.dataSetToShow.states = data.stats;
//       let image: IDatasetImages;
//       for (image of data.images) {
//         if (image) {
//           this.dataSetToShow.images.push(arrayBufferToBase64(image.data));
//         }
//       }
//       this.afterApply_image = true;
//     },
//     (error) => {
//       console.error('Error fetching data:', error);
//     },
//   );
// }
