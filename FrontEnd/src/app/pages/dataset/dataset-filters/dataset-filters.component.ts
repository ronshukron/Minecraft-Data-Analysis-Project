import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { IDatasetFilters } from '../../../Interfaces/IdatasetFilters';

@Component({
  selector: 'app-dataset-filters',
  standalone: true,
  imports: [
    FormsModule,
    MatCardModule,
    MatSelectModule,
    MatSliderModule,
    MatButtonModule,
  ],
  templateUrl: './dataset-filters.component.html',
  styleUrl: './dataset-filters.component.css',
})
export class DatasetFiltersComponent implements OnInit {
  @Output() filterChanged: EventEmitter<IDatasetFilters> =
    new EventEmitter<IDatasetFilters>();

  public filters: IDatasetFilters = {
    datasetSize: 10,
    selectedTask: '',
    selectedCategories: [],
  };
  disabled: boolean = false;
  public max: number = 100;
  public min: number = 10;
  public step: number = 10;

  ngOnInit(): void {}

  public analyze(): void {
    // console.log(this.filters.selectedTask);
    // console.log(this.filters.selectedCategories);
    // console.log(this.filters.datasetSize);
    this.filterChanged.emit(this.filters);
  }
  onCategorySelectionChange(event: any): void {
    this.filters.selectedCategories = event.value;
  }
}
