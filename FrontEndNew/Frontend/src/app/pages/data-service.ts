import { Injectable, NgModule } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {
  IDatasetFilters,
  ISingleGameFilters,
} from '../Interfaces/IdatasetFilters';
import { RouterModule } from '@angular/router';
import { IDataset, getIDataset } from '../Interfaces/Idataset';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private url = 'https://minecraft-analysis-422617.oa.r.appspot.com';
  public gameList: Observable<string[]> = of(['game1', 'game2']);
  public invList: Observable<string[]> = of(['game1', 'game2']);
  public actionAndInv: Observable<string[][]> = of([
    ['inv1', 'inv2'],
    ['act1', 'act2'],
  ]);

  constructor(private http: HttpClient) {}

  // Dataset page
  public getDataSetData(filters: IDatasetFilters): Observable<getIDataset> {
    const size =
      filters && filters.datasetSize ? filters.datasetSize : 'defaultSize';
    let apiUrl = `${this.url}?size=${size}?task=${filters.selectedTask}`;
    return this.http.get<getIDataset>(apiUrl);
  }

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

  // single game page
  //get all filters return all the data for the graph
  public getSingleGameData(
    filters: ISingleGameFilters,
  ): Observable<getIDataset> {
    let apiUrl = `${this.url}/single_game/all_data`;
    const paramValue = filters.selectedTask;
    const params = new HttpParams()
      .set('task', paramValue)
      .set('game', filters.game);
    // .set('inventory', filters.inventory)
    // .set('actions', filters.action)
    return this.http.get<getIDataset>(apiUrl, { params });
  }

  //get list of games
  public getSingleGameList(task: string): Observable<string[]> {
    let apiUrl = `${this.url}/single_game/games_list`;
    const paramValue = task;
    const params = new HttpParams().set('task', paramValue);
    return this.http.get<string[]>(apiUrl, { params });
    return this.gameList;
  }

  //get list of invetory and actions
  public getSingleInventoryList(task: string, game: string): Observable<any> {
    let apiUrl = `${this.url}/single_game/inventory_actions`;
    const paramValue = task;
    const params = new HttpParams().set('task', paramValue).set('name', game);
    return this.http.get<any>(apiUrl, { params });
    return this.actionAndInv;
  }

  //mp4 pgae
  public getMP4Data(): Observable<any> {
    let url = 'https://minecraft-analysis-422617.oa.r.appspot.com/download';
    const paramValue =
      'data/10.0/cheeky-cornflower-setter-02e496ce4abb-20220421-093149.mp4';
    const params = new HttpParams().set('videoPath', paramValue);
    return this.http.get<any>(url, { params });
  }

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

// public getTest(): Observable<string> {
//   const headers = new HttpHeaders()
//     .set('Authorization', 'Bearer your-auth-token')
//     .set('ngrok-skip-browser-warning', '69420');

//   return this.http.get(this.apiUrl, { headers, responseType: 'text' });
// }

// single game page
// public getSingleGameData(
//   filters: ISingleGameFilters,
// ): Observable<getIDataset> {
//   const headers = new HttpHeaders()
//     .set('Authorization', 'Bearer your-auth-token')
//     .set('ngrok-skip-browser-warning', '69420');

//   let apiUrl = `${this.apiUrl}?task=${filters.selectedTask}`;

//   return this.http.get<getIDataset>(apiUrl, { headers });
// }

// public getSingleInventoryList(task: string, game:string): Observable<string[]> {
//   let apiUrl = `${this.apiUrl}/get-video-paths`;
//   const paramValue = task + '.json';
//   const params = new HttpParams().set('jsonFile', paramValue);
//   return this.http.get<string[]>(apiUrl, { params });
// }
