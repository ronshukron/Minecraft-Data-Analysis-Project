export interface IDatasetFilters {
  datasetSize: number;
  selectedTask: string;
  inventory: string[];
  action: string[];
  key: string[];
}

export interface ISingleGameFilters {
  selectedTask: string;
  game: string;
  inventory: string[];
  action: string[];
}
