import { Component, OnInit } from '@angular/core';
import * as Chart from 'chart.js';
import { AngularFireDatabase } from 'angularfire2/database';
@Component({
  selector: 'app-temperature-analytics',
  templateUrl: './temperature-analytics.component.html',
  styleUrls: ['./temperature-analytics.component.scss']
})
export class TemperatureAnalyticsComponent implements OnInit {
  temperatureLineChart: Chart;
  temperatureMonthData = [];
  humidityMonthData: any;
  temperatureTimestamp: string;
  dataLoaded = false;
  chartLabels = ['Temperature, Vochtigheid'];
  constructor(private db: AngularFireDatabase) {
  }

  getTemperatureMonthData() {
    this.db.list('/temperature', ref => ref
        .orderByChild('timestamp')
        .limitToLast(30))
        .valueChanges()
        .subscribe(data => {
            data.forEach(entry => {
                this.temperatureTimestamp = entry['timestamp'];
                this.temperatureMonthData.push(entry['temperature_sensors']);
                // this.humidityMonthData =  entry['temperature_sensors'];
                console.log(this.temperatureMonthData);
            });
        });
  }


  createTemperatureLineChart() {
    const ctx = document.getElementById('temperatureLineChart');
    this.temperatureLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: this.chartLabels,
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: ['rgba(255, 99, 132, 0.2)',
                                  'rgba(54, 162, 235, 0.2)',
                                  'rgba(255, 206, 86, 0.2)',
                                  'rgba(75, 192, 192, 0.2)',
                                  'rgba(153, 102, 255, 0.2)',
                                  'rgba(255, 159, 64, 0.2)'],
                borderColor: ['rgba(255,99,132,1)',
                              'rgba(54, 162, 235, 1)',
                              'rgba(255, 206, 86, 1)',
                              'rgba(75, 192, 192, 1)',
                              'rgba(153, 102, 255, 1)',
                              'rgba(255, 159, 64, 1)'],
                borderWidth: 1
            }]
        },
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
    this.getTemperatureMonthData();
    this.createTemperatureLineChart();
  }

}
