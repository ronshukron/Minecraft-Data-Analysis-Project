export interface getIDataset {
  images: Array<IDatasetImages>;
  stats: Array<IStats>;
}

export interface IDatasetData {
  images: string[];
  stats: Array<IStats>;
}

export interface IminMax {
  min: number;
  max: number;
}
export interface IDatasetImages {
  data: number[];
  type: string;
}

export interface IStats {
  name: string;
  average: number;
  min: number;
  max: number;
  std_deviation: number;
}

// export interface IStats {
//   crafts: IStats_new;
//   mines: IStats_new;
//   uses: IStats_new;
//   walks: IStats_new;
// }

export interface IStats_new {
  avg: number;
  min: number;
  max: number;
  stdDeviation: number;
}
