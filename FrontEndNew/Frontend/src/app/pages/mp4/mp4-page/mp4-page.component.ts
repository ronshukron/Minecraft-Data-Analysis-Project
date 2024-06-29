import {
  Component,
  ElementRef,
  Input,
  OnDestroy,
  OnInit,
  ViewChild,
  input,
} from '@angular/core';
import { DataService } from '../../data-service';
import JSZip from 'jszip';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
@Component({
  selector: 'app-mp4-page',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule],
  templateUrl: './mp4-page.component.html',
  styleUrl: './mp4-page.component.css',
})
export class Mp4PageComponent implements OnInit, OnDestroy {
  videoSrc: string | ArrayBuffer | null = null;
  public fileName: string = '';
  public loading: boolean = false;
  public videoUrl: string = '';
  public message: string = '';
  videos: any;

  constructor(public dataService: DataService) {}

  async ngOnInit() {
    try {
      console.log(this.dataService.gameName);
      const videoBlob = await this.extractVideo();
      this.videoSrc = URL.createObjectURL(videoBlob);
    } catch (error) {
      console.error('Error extracting video:', error);
    }
  }
  ngOnDestroy(): void {}

  async extractVideo(): Promise<Blob> {
    this.loading = true;
    try {
      this.message = 'Fetching MP4 data...';
      console.log('Fetching MP4 data...');
      const blob = await this.dataService.getMP4Data().toPromise(); // Assuming getMP4Data returns an Observable<Blob>
      this.message = 'MP4 data fetched successfully';
      console.log('MP4 data fetched successfully');

      const zip = await JSZip.loadAsync(blob);
      console.log('Zip content:', Object.keys(zip.files));

      const mp4FileName = Object.keys(zip.files).find((filename) =>
        filename.endsWith('.mp4'),
      );

      if (!mp4FileName) {
        this.message = 'MP4 file not found in the zip content';
        throw new Error('MP4 file not found in the zip content');
      }
      (this.message = 'MP4 file found in zip content:'), mp4FileName;
      console.log('MP4 file found in zip content:', mp4FileName);

      const videoFile = zip.file(mp4FileName);
      if (videoFile) {
        console.log('Video file found in zip, extracting...');
        this.message = 'Video file found in zip, extracting...';
        const videoBlob = await videoFile.async('blob');
        console.log('Video file extracted successfully');
        this.message = 'Video file extracted successfully';
        this.loading = false;
        return videoBlob;
      } else {
        this.loading = false;
        this.message = 'Video file not found in the zip';
        throw new Error('Video file not found in the zip');
      }
    } catch (error) {
      this.loading = false;
      console.error('Error during extraction:', error);
      throw error;
    }
  }
}
