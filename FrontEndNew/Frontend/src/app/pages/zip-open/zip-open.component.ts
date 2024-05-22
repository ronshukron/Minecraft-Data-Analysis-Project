import { Component } from '@angular/core';
import JSZip from 'jszip';
import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root', // This makes the service available application-wide
})
@Component({
  selector: 'app-zip-open',
  standalone: true,
  imports: [],
  templateUrl: './zip-open.component.html',
  styleUrl: './zip-open.component.css',
})
export class ZipOpenComponent {
  images: string[] = [];

  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        this.extractZipFile(e.target.result);
      };
      reader.readAsArrayBuffer(file);
    }
  }

  async extractZipFile(fileContent: ArrayBuffer) {
    const zip = new JSZip();
    const contents = await zip.loadAsync(fileContent);

    const jsonFile = contents.file('your-json-file.json');
    if (jsonFile) {
      const jsonData = await jsonFile.async('text');
      const parsedData = JSON.parse(jsonData);

      this.images = this.extractImages(parsedData);
    }
  }

  extractImages(data: any): string[] {
    const images: string[] = [];
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const base64Image = data[key];
        images.push(`data:image/jpeg;base64,${base64Image}`);
      }
    }
    return images;
  }
}
