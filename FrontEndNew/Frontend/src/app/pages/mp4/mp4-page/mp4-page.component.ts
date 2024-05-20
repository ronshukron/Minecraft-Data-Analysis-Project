import {
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  ViewChild,
} from '@angular/core';
import { DataService } from '../../data-service';
import * as JSZip from 'jszip';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

@Component({
  selector: 'app-mp4-page',
  standalone: true,
  imports: [],

  templateUrl: './mp4-page.component.html',
  styleUrl: './mp4-page.component.css',
})
export class Mp4PageComponent implements OnInit, OnDestroy {
  @ViewChild('videoPlayer') videoPlayer?: ElementRef;
  private zip?: JSZip;

  constructor(public dataService: DataService) {}

  ngOnInit(): void {
    this.fetchAndExtractZip();
  }

  ngOnDestroy(): void {
    if (this.zip) {
      this.zip = undefined;
    }
  }

  async fetchAndExtractZip(): Promise<void> {
    const zipUrl = 'assets/mp4/attachment.zip';
    const response = await fetch(zipUrl);
    const zipData = await response.arrayBuffer();
    this.zip = await (JSZip.loadAsync(zipData) as unknown as JSZip);
    const mp4File = this.zip.file(
      'cheeky-cornflower-setter-02e496ce4abb-20220421-093149.mp4',
    );
    if (mp4File) {
      const mp4Data = await mp4File.async('blob');
      this.displayVideo(mp4Data);
    } else {
      console.error('MP4 file not found in ZIP.');
    }
  }

  displayVideo(mp4Data: Blob): void {
    if (!this.videoPlayer) return;
    const videoElement = this.videoPlayer.nativeElement;
    const player = videojs(videoElement, {});
    player.src(window.URL.createObjectURL(mp4Data));
  }
}
