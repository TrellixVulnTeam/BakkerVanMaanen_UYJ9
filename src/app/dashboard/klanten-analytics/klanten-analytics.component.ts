import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
@Component({
  selector: 'app-klanten-analytics',
  templateUrl: './klanten-analytics.component.html',
  styleUrls: ['./klanten-analytics.component.scss']
})
export class KlantenAnalyticsComponent implements OnInit {

  klantenChart: Chart;
  dataLoaded = false;

  constructor() {}

  createKlantenChart() {
    const ctx = document.getElementById('klantenChart');
    this.klantenChart = new Chart(ctx, {
        type: 'line',
        responsive: true,
        data: {
            datasets: [{
                label: 'X Coordinaten',
                data: [38, 33, 31, 30, 39, 32, 35, 40],
                borderColor: '#3e95cd',
                fill: true
            }, {
                label: 'Y Coordinaten',
                data: [38, 33, 31, 30, 39, 32, 35, 40],
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
            }
        }
    });
    this.dataLoaded = true;
  }

  ngOnInit() {
      this.createKlantenChart();
  }
}
