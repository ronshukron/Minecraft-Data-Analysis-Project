import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { IDatasetFilters } from '../../../Interfaces/IdatasetFilters';
import { DatasetFiltersComponent } from '../dataset-filters/dataset-filters.component';
import { DataService } from '../../data-service';
import {
  IDataset,
  IDatasetImages,
  IStats,
  IStats_new,
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
  public afterApply_image: boolean = false;
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
    this.afterApply_image = false;
    this.afterApply = true;
    this.dataSetToShow.images = [];
    this.dataSetToShow.avg = 0;
    (this.dataSetToShow.minMax = { min: 0, max: 100 }),
      (this.dataSetToShow.stdDeviation = 0);
    this.dataService.getDataSetFilters(filters).subscribe(
      (data: getIDataset) => {
        console.log(data);
        console.log(data.states);
        console.log(data.images);
        this.dataSetToShow.states = data.states;
        let image: IDatasetImages;
        for (image of data.images) {
          if (image) {
            this.dataSetToShow.images.push(arrayBufferToBase64(image.data));
          }
        }
        this.afterApply_image = true;
      },
      (error) => {
        console.error('Error fetching data:', error);
      },
    );
  }
}
