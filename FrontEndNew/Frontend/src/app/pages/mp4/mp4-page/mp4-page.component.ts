import {
  Component,
  ElementRef,
  Input,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { DataService } from '../../data-service';
import * as JSZip from 'jszip';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
@Component({
  selector: 'app-mp4-page',
  standalone: true,
  imports: [],
  templateUrl: './mp4-page.component.html',
  styleUrl: './mp4-page.component.css',
})
export class Mp4PageComponent implements OnInit, OnDestroy {
  @Input() fileName: string = this.dataService.gameName;
  public loading: boolean = false;
  public videoUrl: string = '';
  constructor(public dataService: DataService) {}
  ngOnInit(): void {
    this.fileName = this.dataService.gameName;
    this.onGameChanged();
  }
  ngOnDestroy(): void {}
  public async onGameChanged() {
    if (!this.fileName) return;
    this.loading = true;
    try {
      const zipFile = await this.dataService.getMP4Data().toPromise();
      const zip = await JSZip.loadAsync(zipFile);
      const file = zip.file(this.fileName);
      if (file) {
        const content = await file.async('blob');
        this.videoUrl = URL.createObjectURL(content);
      } else {
        console.error('File not found in the ZIP archive');
      }
    } catch (error) {
      console.error('Error fetching or extracting ZIP:', error);
    } finally {
      this.loading = false;
    }
  }
}
