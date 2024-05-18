import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { ISingleGameFilters } from '../../../Interfaces/IdatasetFilters';
import { DataService } from '../../data-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-single-game-filters',
  standalone: true,
  imports: [
    FormsModule,
    MatCardModule,
    MatSelectModule,
    MatSliderModule,
    MatButtonModule,
    FormsModule,
    CommonModule,
  ],
  templateUrl: './single-game-filters.component.html',
  styleUrl: './single-game-filters.component.css',
})
export class SingleGameFiltersComponent {
  public onInventoryChange(event: any): void {
    this.filters.inventory = event;
    this.selsectedInventoryOptions = event.value;
  }

  public onActionsChange(event: any): void {
    this.filters.action = event;
    this.selsectedActionsOptions = event.value;
  }

  public afterApply: boolean = false;
  public disabled: boolean = false;
  public gamesOptions: string[] = [];
  public inventoryOptions: string[] = [];
  public actionsOptions: string[] = [];
  public afterSelectTask: boolean = false;
  public afterSelectGame: boolean = false;
  public selsectedInventoryOptions: string[] = [];
  public selsectedActionsOptions: string[] = [];

  @Output() filterChanged: EventEmitter<ISingleGameFilters> =
    new EventEmitter<ISingleGameFilters>();

  public filters: ISingleGameFilters = {
    selectedTask: '',
    game: '',
    inventory: [],
    action: [],
  };

  ngOnInit(): void {}
  constructor(public dataService: DataService) {}

  public analyze(): void {
    console.log(this.filters);
    this.filterChanged.emit(this.filters);
  }

  public onTaskChange(taskName: string): void {
    this.getListOfGames();
  }

  public onGameChange(game: Event): void {
    this.getListOfInventoryAndActions();
  }

  private getListOfInventoryAndActions() {
    if (!this.filters.game || !this.filters.selectedTask) return;
    this.clearListOfInventoryAndActions();
    this.dataService
      .getSingleInventoryList(this.filters.selectedTask, this.filters.game)
      .subscribe(
        (data: any) => {
          console.log(data);
          console.log(data.actions);
          this.inventoryOptions = data.actions;
          this.actionsOptions = data.inventory;
          this.afterSelectGame = true;
        },
        (error) => {
          console.error('Error cant load the list of games:', error);
        },
      );
  }

  private getListOfGames(): void {
    if (!this.filters.selectedTask) return;
    this.gamesOptions = [];

    this.dataService.getSingleGameList(this.filters.selectedTask).subscribe(
      (data: string[]) => {
        this.gamesOptions = data;
        this.afterSelectTask = true;
      },
      (error) => {
        console.error('Error cant load the list of games:', error);
      },
    );
  }

  private clearListOfInventoryAndActions(): void {
    this.inventoryOptions = [];
    this.actionsOptions = [];
    this.selsectedInventoryOptions = [];
    this.selsectedActionsOptions = [];
  }
}
