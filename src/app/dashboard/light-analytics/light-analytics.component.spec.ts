import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LightAnalyticsComponent } from './light-analytics.component';

describe('LightAnalyticsComponent', () => {
  let component: LightAnalyticsComponent;
  let fixture: ComponentFixture<LightAnalyticsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LightAnalyticsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LightAnalyticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
