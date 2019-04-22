import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BokehVizComponent } from './bokeh-viz.component';

describe('BokehVizComponent', () => {
  let component: BokehVizComponent;
  let fixture: ComponentFixture<BokehVizComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BokehVizComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BokehVizComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
