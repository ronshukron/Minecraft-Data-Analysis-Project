import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ZipOpenComponent } from './zip-open.component';

describe('ZipOpenComponent', () => {
  let component: ZipOpenComponent;
  let fixture: ComponentFixture<ZipOpenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ZipOpenComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ZipOpenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
