import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProblemCreatorComponent } from './problem-creator.component';

describe('ProblemCreatorComponent', () => {
  let component: ProblemCreatorComponent;
  let fixture: ComponentFixture<ProblemCreatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProblemCreatorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProblemCreatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
