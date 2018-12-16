import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KlantenComponent } from './klanten.component';

describe('KlantenComponent', () => {
  let component: KlantenComponent;
  let fixture: ComponentFixture<KlantenComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KlantenComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KlantenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
