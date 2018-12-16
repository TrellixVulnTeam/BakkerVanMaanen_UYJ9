import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { DashboardPage } from './dashboard.page';
import { TemperatureComponent } from './temperature/temperature.component';
import { VitrineComponent } from './vitrine/vitrine.component';
import { LightsComponent } from './lights/lights.component';
import { LightAnalyticsComponent } from './light-analytics/light-analytics.component';
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
  declarations: [DashboardPage, TemperatureComponent, VitrineComponent, LightsComponent, LightAnalyticsComponent, TemperatureAnalyticsComponent, VitrineAnalyticsComponent, KlantenAnalyticsComponent, KlantenComponent]
})
export class DashboardPageModule {}
