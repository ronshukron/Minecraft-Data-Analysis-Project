export interface getIDataset {
  images: Array<IDatasetImages>;
  states: Array<IStats>;
  avg: number;
  stdDeviation: number;
  minMax: IminMax;
}

export interface IDataset {
  images: Array<string>;
  states: Array<IStats>;
  avg: number;
  stdDeviation: number;
  minMax: IminMax;
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
  avg: number;
  min: number;
  max: number;
  stdDeviation: number;
}
