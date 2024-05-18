import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetFiltersComponent } from './dataset-filters.component';

describe('DatasetFiltersComponent', () => {
  let component: DatasetFiltersComponent;
  let fixture: ComponentFixture<DatasetFiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatasetFiltersComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DatasetFiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
