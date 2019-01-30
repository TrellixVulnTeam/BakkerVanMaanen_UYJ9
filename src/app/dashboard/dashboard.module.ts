import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { DashboardPage } from './dashboard.page';
import { TemperatureComponent } from './temperature/temperature.component';
import { VitrineComponent } from './vitrine/vitrine.component';
import { TemperatureAnalyticsComponent } from './temperature-analytics/temperature-analytics.component';
import { VitrineAnalyticsComponent } from './vitrine-analytics/vitrine-analytics.component';
import { KlantenAnalyticsComponent } from './klanten-analytics/klanten-analytics.component';
import { KlantenComponent } from './klanten/klanten.component';

const routes: Routes = [
  {
    path: '',
    component: DashboardPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  declarations: [
      DashboardPage,
      KlantenComponent,
      TemperatureComponent,
      VitrineComponent,
      TemperatureAnalyticsComponent,
      VitrineAnalyticsComponent,
      KlantenAnalyticsComponent
  ]
})
export class DashboardPageModule {}
