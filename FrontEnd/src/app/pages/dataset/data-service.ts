import { Injectable, NgModule } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { IDatasetFilters } from '../../Interfaces/IdatasetFilters';
import { RouterModule } from '@angular/router';
import { IDataset, getIDataset } from '../../Interfaces/Idataset';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private apiUrl = 'https://faed-89-139-146-5.ngrok-free.app/api';

  constructor(private http: HttpClient) {}

  public getTest(): Observable<string> {
    const headers = new HttpHeaders()
      .set('Authorization', 'Bearer your-auth-token')
      .set('ngrok-skip-browser-warning', '69420');

    return this.http.get(this.apiUrl, { headers, responseType: 'text' });
  }

  public getData(filters: IDatasetFilters): Observable<getIDataset> {
    const headers = new HttpHeaders()
      .set('Authorization', 'Bearer your-auth-token')
      .set('ngrok-skip-browser-warning', '69420');

    const size =
      filters && filters.datasetSize ? filters.datasetSize : 'defaultSize';

    let apiUrl = `${this.apiUrl}?size=${size}`;

    return this.http.get<getIDataset>(apiUrl, { headers });
  }

  public getDataSetData(data: IDatasetFilters): string[] {
    return ['/images/Demo_graph_1.jpg', '/images/Demo_graph_2.jpg'];
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
