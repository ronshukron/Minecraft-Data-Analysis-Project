import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { IDatasetFilters } from '../../../Interfaces/IdatasetFilters';
import { DatasetFiltersComponent } from '../dataset-filters/dataset-filters.component';
import { DataService } from '../data-service';
import {
  IDataset,
  IDatasetImages,
  IStats,
  getIDataset,
} from '../../../Interfaces/Idataset';
import { arrayBufferToBase64 } from '../../../utilityFunctions/arrayBufferToBase64';

@Component({
  selector: 'app-dataset-main',
  standalone: true,
  templateUrl: './dataset-main.component.html',
  styleUrl: './dataset-main.component.css',
  imports: [DatasetFiltersComponent],
})
export class DatasetMainComponent implements OnInit {
  public afterApply: boolean = false;
  // public images: Array<IDatasetImages> = [];
  public data: string = 'no data';
  // public imageSrc: string = 'no image here';

  public dataSetToShow: IDataset = {
    images: [],
    states: [],
    avg: 0,
    stdDeviation: 0,
    minMax: { min: 0, max: 100 },
  };

  constructor(public dataService: DataService) {}

  ngOnInit(): void {}

  public onFilterChanged(filters: IDatasetFilters) {
    if (!filters) return;
    console.log(filters);

    this.afterApply = true;

    this.dataService.getData(filters).subscribe(
      (data: getIDataset) => {
        this.dataSetToShow.avg = data.avg;
        this.dataSetToShow.minMax = data.minMax;
        this.dataSetToShow.stdDeviation = data.stdDeviation;
        let image: IDatasetImages;
        for (image of data.images) {
          if (image) {
            this.dataSetToShow.images.push(arrayBufferToBase64(image.data));
          }
        }
        this.dataSetToShow.states = data.states;
      },
      (error) => {
        console.error('Error fetching data:', error);
      },
    );
  }
}
