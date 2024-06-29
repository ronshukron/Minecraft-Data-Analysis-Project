import { Injectable, NgModule } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import {
  IDatasetFilters,
  ISingleGameFilters,
} from '../Interfaces/IdatasetFilters';
import { RouterModule } from '@angular/router';
import { getIDataset } from '../Interfaces/Idataset';
import { IsingleGameDataFromAPI } from '../Interfaces/IsingleGameData';
import JSZip from 'jszip';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  public gameName: string = '';
  private url = 'http://132.73.84.50:8080';
  public gameList: Observable<string[]> = of(['game1', 'game2']);
  public invList: Observable<string[]> = of(['game1', 'game2']);
  public actionAndInv: Observable<string[][]> = of([
    ['inv1', 'inv2'],
    ['act1', 'act2'],
  ]);

  constructor(private http: HttpClient) {}

  //////////////////////////////////////////////////////////
  // Dataset page

  // Dataset page fillters
  public getDataSetFilters(filters: IDatasetFilters): Observable<getIDataset> {
    const size =
      filters && filters.datasetSize ? filters.datasetSize : 'defaultSize';
    let apiUrl = `${this.url}/dataset/keys_inventory_actions`;
    const params = new HttpParams()
      .set('task', filters.selectedTask)
      .set('size', size);
    return this.http.get<any>(apiUrl, { params });
  }

  //  Dataset page Ron two images and statistics
  public getDataSetDataGraphAndStatistics(
    filters: IDatasetFilters,
  ): Observable<getIDataset> {
    const size =
      filters && filters.datasetSize ? filters.datasetSize : 'defaultSize';
    let apiUrl = `${this.url}/dataset/timelines_stats`;
    const params = new HttpParams()
      .set('task', filters.selectedTask)
      .set('size', size)
      .set('inventory', filters.inventory.join(','))
      .set('aggregated_actions', filters.action.join(','))
      .set('keys', filters.key.join(','));
    return this.http.get<getIDataset>(apiUrl, { params });
  }

  //  Dataset page Shira zip file with images

  public getDataSetDataZipGraph(filters: any): Observable<any> {
    const size = filters?.datasetSize || 'defaultSize';
    const apiUrl = `${this.url}/dataset/hist`;
    const params = new HttpParams()
      .set('task', filters.selectedTask)
      .set('size', size)
      .set('inventory', filters.inventory.join(','))
      .set('aggregated_actions', filters.action.join(','))
      .set('keys', filters.key.join(','));

    return this.http.get(apiUrl, { params, responseType: 'blob' });
  }

  //////////////////////////////////////////////////////////////////
  // single game page
  //get list of games
  public getSingleGameList(task: string): Observable<string[]> {
    let apiUrl = `${this.url}/single_game/games_list`;
    const paramValue = task;
    const params = new HttpParams().set('task', paramValue);
    return this.http.get<string[]>(apiUrl, { params });
    return this.gameList;
  }

  //get list of invetory and actions filters
  public getSingleInventoryList(task: string, game: string): Observable<any> {
    let apiUrl = `${this.url}/single_game/inventory_actions`;
    const paramValue = task;
    const params = new HttpParams().set('task', paramValue).set('name', game);
    return this.http.get<any>(apiUrl, { params });
  }

  //get all filters return all the data for the graph
  public getSingleGameData(
    filters: ISingleGameFilters,
  ): Observable<IsingleGameDataFromAPI> {
    let apiUrl = `${this.url}/single_game/timelines`;
    const paramValue = filters.selectedTask;
    const params = new HttpParams()
      .set('task', paramValue)
      .set('name', filters.game)
      .set('inventory', filters.inventory.join(','))
      .set('aggregated_actions', filters.action.join(','));
    return this.http.get<IsingleGameDataFromAPI>(apiUrl, {
      params,
    });
  }

  ///////////////////////////////////////////////////////////////

  // mp4 pgae
  public getMP4Data(): Observable<any> {
    const apiUrl = `${this.url}/download`;
    const params = new HttpParams().set('videoPath', this.gameName);
    return this.http.get(apiUrl, { params, responseType: 'blob' });
  }

  // public getMP4Data(): Observable<Blob> {
  //   return this.http.get('assets/video.zip', { responseType: 'blob' });
  // }

  private handleError(error: HttpErrorResponse): Observable<any> {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, ` + `body was: ${error.error}`,
      );
    }
    // Return an observable with a user-facing error message.
    return throwError('Something bad happened; please try again later.');
  }
}
