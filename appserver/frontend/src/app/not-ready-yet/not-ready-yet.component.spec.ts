import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NotReadyYetComponent } from './not-ready-yet.component';

describe('NotReadyYetComponent', () => {
  let component: NotReadyYetComponent;
  let fixture: ComponentFixture<NotReadyYetComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NotReadyYetComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NotReadyYetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
