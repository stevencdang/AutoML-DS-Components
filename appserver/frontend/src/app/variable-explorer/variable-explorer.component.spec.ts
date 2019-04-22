import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VariableExplorerComponent } from './variable-explorer.component';

describe('VariableExplorerComponent', () => {
  let component: VariableExplorerComponent;
  let fixture: ComponentFixture<VariableExplorerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VariableExplorerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VariableExplorerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
