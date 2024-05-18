import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleGameFiltersComponent } from './single-game-filters.component';

describe('SingleGameFiltersComponent', () => {
  let component: SingleGameFiltersComponent;
  let fixture: ComponentFixture<SingleGameFiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SingleGameFiltersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SingleGameFiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
