import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { DashboardPage } from './dashboard.page';
import { TemperatureComponent } from './temperature/temperature.component';
import { VitrineComponent } from './vitrine/vitrine.component';
import { LightsComponent } from './lights/lights.component';

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
  declarations: [DashboardPage, TemperatureComponent, VitrineComponent, LightsComponent]
})
export class DashboardPageModule {}
