import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { IDatasetFilters } from '../../../Interfaces/IdatasetFilters';
import { DataService } from '../../data-service';
import { Subject, takeUntil } from 'rxjs';
import { CommonModule } from '@angular/common';
import { iTask } from '../../../Interfaces/Itask';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-dataset-filters',
  standalone: true,
  imports: [
    MatIconModule,
    MatDialogModule,
    FormsModule,
    MatCardModule,
    MatSelectModule,
    MatSliderModule,
    MatButtonModule,
    CommonModule,
  ],
  templateUrl: './dataset-filters.component.html',
  styleUrl: './dataset-filters.component.css',
})
export class DatasetFiltersComponent implements OnInit {
  public afterApply: boolean = false;
  public disabled: boolean = false;
  public afterSelectTaskAndSize: boolean = false;

  public inventoryOptions: iTask[] = [];
  public inventoryOptionsDict: { name: string; action: string }[] = [];

  public actionsOptions: iTask[] = [];
  public actionOptionsDict: { name: string; action: string }[] = [];

  public keysOptions: string[] = [];

  private unsubscribeList: Subject<void> = new Subject<void>();

  public max: number = 100;
  public min: number = 10;
  public step: number = 10;

  public filters: IDatasetFilters = {
    datasetSize: 10,
    selectedTask: '',
    inventory: [],
    action: [],
    key: [],
  };

  @Output() filterChanged: EventEmitter<IDatasetFilters> =
    new EventEmitter<IDatasetFilters>();

  ngOnInit(): void {}

  constructor(public dataService: DataService) {}

  public analyze(): void {
    this.filterChanged.emit(this.filters);
  }
  public onKeysChange(keysSelectedList: string[]): void {
    this.filters.key = keysSelectedList;
  }
  public onTaskOrDatasetSizeChange(event: string): void {
    this.getListOfInventoryActionsAndKeys();
  }

  private getListOfInventoryActionsAndKeys(): void {
    if (!this.filters.selectedTask) return;
    this.clearListOfInventoryAndActions();
    this.dataService
      .getDataSetFilters(this.filters)
      .pipe(takeUntil(this.unsubscribeList))
      .subscribe(
        (data: any) => {
          this.inventoryOptions = data.actions;
          this.actionsOptions = data.inventory;
          this.keysOptions = data.keys;
          this.afterSelectTaskAndSize = true;
        },
        (error) => {
          console.error('Error cant load the list of games:', error);
        },
      );
  }

  public onActionsChange(tasks: { name: string; action: string }[]) {
    this.actionOptionsDict = tasks;
    this.filters.action = this.dataService.transformToTaskArray(
      this.actionOptionsDict,
    );
    console.log(this.filters.action);
  }

  public onInventoryChange(tasks: { name: string; action: string }[]) {
    this.inventoryOptionsDict = tasks;
    this.filters.inventory = this.dataService.transformToTaskArray(
      this.inventoryOptionsDict,
    );
    console.log(this.filters.inventory);
  }

  private clearListOfInventoryAndActions(): void {
    this.afterSelectTaskAndSize = false;
    this.inventoryOptions = [];
    this.actionsOptions = [];
    this.filters.action = [];
    this.filters.inventory = [];
  }
}
