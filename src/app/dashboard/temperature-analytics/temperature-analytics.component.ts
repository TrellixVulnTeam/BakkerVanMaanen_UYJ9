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
  humidityMonthData = [];
  temperatureDates = [];
  temperatureTimestamp: string;
  dataLoaded = false;
  chartLabels = ['Temperature, Vochtigheid'];

  constructor(private db: AngularFireDatabase) {
    this.getTemperatureMonthData();
  }

  getTemperatureMonthData() {
    this.db.list('/temperature', ref => ref
        .orderByChild('timestamp')
        .limitToLast(20))
        .valueChanges()
        .subscribe(data => {
            data.forEach(entry => {
                this.temperatureTimestamp = entry['timestamp'];
                this.temperatureDates.push(entry['timestamp']);
                entry['temperature_sensors'].forEach(sensors => {
                   this.humidityMonthData.push(sensors['humidity']);
                   this.temperatureMonthData.push(sensors['temperature']);
                });
            });
        });
        this.dataLoaded = true;
  }


  createTemperatureLineChart() {
    const ctx = document.getElementById('temperatureLineChart');
    this.temperatureLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: this.temperatureDates,
            backgroundColor: '#FFF',
            datasets: [{
                label: 'Temperature',
                data: this.temperatureMonthData,
                borderColor: 'white',
            }, {
                label: 'Humidity',
                labelColor: 'black',
                data: this.humidityMonthData,
                borderColor: 'black',
            }]
        },
        options: {
            legend: {
                labels: {
                    fontColor: 'white',
                    fontSize: 15
                }
            },
            title: {
                display: true,
                text: 'Average Humidity and Temperature',
                fontColor: 'white'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: '#FFF',
                        stepSize: 10,
                        beginAtZero: true
                    },
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'white',
                        stepSize: 10,
                        beginAtZero: true
                    },
                }]
          }
        }
    });
    this.dataLoaded = true;
  }

  ngOnInit() {
     if (this.dataLoaded) {
         this.createTemperatureLineChart();
     }
  }

}
