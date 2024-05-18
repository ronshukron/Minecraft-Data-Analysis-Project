export interface IDatasetFilters {
  datasetSize: number;
  selectedTask: string;
  selectedCategories: string[];
}

export interface ISingleGameFilters {
  selectedTask: string;
  game: string;
  inventory: string[];
  action: string[];
}
