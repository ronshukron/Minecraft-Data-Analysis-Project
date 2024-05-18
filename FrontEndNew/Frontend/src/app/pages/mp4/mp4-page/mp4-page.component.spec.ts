import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Mp4PageComponent } from './mp4-page.component';

describe('Mp4PageComponent', () => {
  let component: Mp4PageComponent;
  let fixture: ComponentFixture<Mp4PageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Mp4PageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(Mp4PageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
