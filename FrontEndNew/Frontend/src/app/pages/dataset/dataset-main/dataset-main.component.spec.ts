import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetMainComponent } from './dataset-main.component';

describe('DatasetMainComponent', () => {
  let component: DatasetMainComponent;
  let fixture: ComponentFixture<DatasetMainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatasetMainComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DatasetMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
