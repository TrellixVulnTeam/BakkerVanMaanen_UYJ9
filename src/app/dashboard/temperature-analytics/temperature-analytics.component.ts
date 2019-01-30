import { Component, AfterViewInit } from '@angular/core';
import * as Chart from 'chart.js';
import * as ChartAnnotation from 'chartjs-plugin-annotation';
import { AngularFireDatabase } from 'angularfire2/database';
@Component({
  selector: 'app-temperature-analytics',
  templateUrl: './temperature-analytics.component.html',
  styleUrls: ['./temperature-analytics.component.scss']
})
export class TemperatureAnalyticsComponent implements AfterViewInit {
  temperatureLineChart: Chart;
  humidityLineChart: Chart;
  temperatureMonthData: number[] = [];
  humidityMonthData: number[] = [];
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
                this.temperatureDates.push(entry['timestamp'].substr(0, 19));
                entry['temperature_sensors'].forEach(sensors => {
                   this.humidityMonthData.push(sensors['humidity']);
                   this.temperatureMonthData.push(sensors['temperature']);
                });
            this.dataLoaded = true;
            });
        });
  }


  createTemperatureLineChart() {
    const ctx = document.getElementById('temperatureLineChart');
    this.temperatureLineChart = new Chart(ctx, {
        type: 'line',
        responsive: true,
        data: {
            labels: this.temperatureDates,
            backgroundColor: '#FFF',
            datasets: [{
                label: 'Temperature',
                data: this.temperatureMonthData,
                borderColor: '#3e95cd',
                fill: true
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
                text: 'AVERAGE TEMPERATURE',
                fontColor: 'white',
                fontSize: 20
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: '#FFF',
                        stepSize: 5,
                    },
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'white',
                        stepSize: 5,
                    },
                }]
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            annotation: {
                annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: 21,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 4
                }, {
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: 16,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 4
                }]
            }
        },
        plugins: [ChartAnnotation]
    });
  }

  createHumidityLineChart() {
    const ctx = document.getElementById('humidityLineChart');
    this.humidityLineChart = new Chart(ctx, {
        type: 'line',
        responsive: true,
        data: {
            labels: this.temperatureDates,
            backgroundColor: '#FFF',
            datasets: [{
                label: 'Humidity',
                labelColor: 'white',
                data: this.humidityMonthData,
                borderColor: '#c45850',
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
                text: 'AVERAGE HUMIDITY',
                fontColor: 'white',
                fontSize: 20
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: '#FFF',
                        stepSize: 10,
                    },
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'white',
                        stepSize: 10,
                    },
                }]
            },
            annotation: {
                annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: 50,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 4
                }, {
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: 40,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 4
                }]
            },
            plugins: [ChartAnnotation]
        }
    });
  }

  ngAfterViewInit() {
     this.createTemperatureLineChart();
     this.createHumidityLineChart();
  }

}
