import { Component, OnInit } from '@angular/core';
import * as Chart from 'chart.js';

@Component({
  selector: 'app-temperature-analytics',
  templateUrl: './temperature-analytics.component.html',
  styleUrls: ['./temperature-analytics.component.scss']
})
export class TemperatureAnalyticsComponent implements OnInit {
  temperatureLineChart: Chart;
  dataLoaded = false;

  constructor() { 
    this.createTemperatureLineChart();
  }

  createTemperatureLineChart() {
      this.temperatureLineChart = new Chart('temperatureLineChart', {
          type: 'line',
          data: ['1', '2', '3'],
          options: {
              scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero: true
                      }
                  }]
              }
          }
      });
      this.dataLoaded = true;
  }

  ngOnInit() {
  }

}
