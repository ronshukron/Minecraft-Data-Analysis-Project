import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule } from '@angular/material/button';
import { ISingleGameFilters } from '../../../Interfaces/IdatasetFilters';
import { DataService } from '../../data-service';
import { CommonModule } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';
import { iTask } from '../../../Interfaces/Itask';

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
  public afterApply: boolean = false;
  public disabled: boolean = false;
  public gamesOptions: string[] = [];

  public afterSelectTask: boolean = false;
  public afterSelectGame: boolean = false;

  private unsubscribeList: Subject<void> = new Subject<void>();
  public inventoryOptions: string[] = [];

  public actionsOptions: iTask[] = [];
  public actionOptionsDict: { name: string; action: string }[] = [];

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

  ngOnDestroy(): void {
    this.unsubscribeList.next();
    this.unsubscribeList.complete();
  }

  public analyze(): void {
    this.filterChanged.emit(this.filters);
  }

  public onTaskChange(taskName: string): void {
    this.getListOfGames();
  }

  public onGameChange(game: Event): void {
    this.getListOfInventoryAndActions();
  }

  public onInventoryChange(list: string[]): void {
    this.filters.inventory = list;
  }

  private getListOfInventoryAndActions() {
    if (!this.filters.game || !this.filters.selectedTask) return;
    this.clearListOfInventoryAndActions();
    this.dataService
      .getSingleInventoryList(this.filters.selectedTask, this.filters.game)
      .pipe(takeUntil(this.unsubscribeList))
      .subscribe(
        (data: any) => {
          this.inventoryOptions = data.inventory;
          this.inventoryOptions = data.inventory.sort((a: string, b: string) =>
            a > b ? 1 : -1,
          );
          this.actionsOptions = data.actions;
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

    this.dataService
      .getSingleGameList(this.filters.selectedTask)
      .pipe(takeUntil(this.unsubscribeList))
      .subscribe(
        (data: string[]) => {
          this.gamesOptions = data;
          this.afterSelectTask = true;
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

  private clearListOfInventoryAndActions(): void {
    this.afterSelectGame = false;
    this.inventoryOptions = [];
    this.actionsOptions = [];
    this.filters.action = [];
    this.filters.inventory = [];
  }
}
