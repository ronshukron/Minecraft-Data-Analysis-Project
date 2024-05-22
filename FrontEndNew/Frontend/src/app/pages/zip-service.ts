// src/app/services/zip.service.ts
import { Injectable } from '@angular/core';
import JSZip from 'jszip';
import { from, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ZipService {
  constructor() {}

  extractZip(file: File): Observable<any> {
    const zip = new JSZip();
    return from(zip.loadAsync(file)).pipe(
      map((zip) => {
        const jsonFile = zip.file('data.json');
        if (!jsonFile) {
          throw new Error('JSON file not found in the zip.');
        }
        return jsonFile.async('string');
      }),
      map(async (jsonString) => {
        const jsonData = JSON.parse(await jsonString);
        Object.keys(jsonData).forEach((key) => {
          if (
            typeof jsonData[key] === 'string' &&
            jsonData[key].startsWith('/9j/')
          ) {
            jsonData[key] = `data:image/jpeg;base64,${jsonData[key]}`;
          }
        });
        return jsonData;
      }),
    );
  }
}
