import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VitrineAnalyticsComponent } from './vitrine-analytics.component';

describe('VitrineAnalyticsComponent', () => {
  let component: VitrineAnalyticsComponent;
  let fixture: ComponentFixture<VitrineAnalyticsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VitrineAnalyticsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VitrineAnalyticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
