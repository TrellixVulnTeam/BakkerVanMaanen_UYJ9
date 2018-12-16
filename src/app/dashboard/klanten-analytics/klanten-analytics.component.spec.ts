import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KlantenAnalyticsComponent } from './klanten-analytics.component';

describe('KlantenAnalyticsComponent', () => {
  let component: KlantenAnalyticsComponent;
  let fixture: ComponentFixture<KlantenAnalyticsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KlantenAnalyticsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KlantenAnalyticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
