import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TemperatureAnalyticsComponent } from './temperature-analytics.component';

describe('TemperatureAnalyticsComponent', () => {
  let component: TemperatureAnalyticsComponent;
  let fixture: ComponentFixture<TemperatureAnalyticsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TemperatureAnalyticsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TemperatureAnalyticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
