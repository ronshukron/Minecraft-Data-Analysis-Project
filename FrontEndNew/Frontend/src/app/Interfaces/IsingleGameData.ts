import { IDatasetImages, IStats } from './Idataset';

export interface IsingleGameDataFromAPI {
  images: Array<IDatasetImages>;
  data_points: Array<IStats>;
}
export interface IsingleGameData {
  images: string[];
  data_points: Array<IStats>;
}
