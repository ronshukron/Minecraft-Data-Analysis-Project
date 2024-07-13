export interface IDatasetFilters {
  datasetSize: number;
  selectedTask: string;
  inventory: string[];
  action: { name: string; actions: string[] }[];
  key: string[];
}

export interface ISingleGameFilters {
  selectedTask: string;
  game: string;
  inventory: string[];
  action: { name: string; actions: string[] }[];
}
