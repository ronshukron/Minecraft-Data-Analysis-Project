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
import { ZipOpenComponent } from '../../zip-open/zip-open.component';
import { publishFacade } from '@angular/compiler';
import JSZip from 'jszip';
import { Subscription } from 'rxjs';

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
  private sub: Subscription | undefined;

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

  constructor(
    public dataService: DataService,
    public zipService: ZipOpenComponent,
  ) {}

  ngOnInit(): void {}

  ngOnDestroy(): void {
    if (this.sub) this.sub.unsubscribe();
    this.restart_args;
  }

  public onFilterChanged(filters: IDatasetFilters) {
    if (!filters) return;
    this.filters = filters;
    this.restart_args();
    this.loading = true;
    if (this.sub) this.sub.unsubscribe();
    this.sub = this.dataService
      .getDataSetDataGraphAndStatistics(filters)
      .subscribe(
        (data: getIDataset) => {
          this.data.stats = data.stats;
          this.setImageFromAPI(data);
          this.afterApply = true;
          this.loading = false;
        },
        (error) => {
          console.error('Error fetching data from ron graphs:', error);
        },
      );

    this.dataService.getDataSetDataZipGraph(filters).subscribe((blob) => {
      const zip = new JSZip();
      zip.loadAsync(blob).then((contents) => {
        Object.keys(contents.files).forEach((filename) => {
          zip
            .file(filename)
            ?.async('base64')
            .then(
              (base64) => {
                this.createImageElement(base64);
                this.afterApply = true;
                this.loading = false;
              },
              (error) => {
                console.error('Error fetching data from zip:', error);
              },
            );
        });
      });
    });
  }
  public images: HTMLImageElement[] = [];

  createImageElement(base64String: string): void {
    const imageElement = new Image();
    imageElement.src = `data:image/png;base64,${base64String}`;
    this.images.push(imageElement);
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
