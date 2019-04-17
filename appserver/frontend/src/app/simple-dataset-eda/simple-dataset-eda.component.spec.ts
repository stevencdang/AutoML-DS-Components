import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SimpleDatasetEdaComponent } from './simple-dataset-eda.component';

describe('SimpleDatasetEdaComponent', () => {
  let component: SimpleDatasetEdaComponent;
  let fixture: ComponentFixture<SimpleDatasetEdaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SimpleDatasetEdaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SimpleDatasetEdaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
