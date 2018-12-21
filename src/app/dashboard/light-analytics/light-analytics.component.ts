import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-light-analytics',
  templateUrl: './light-analytics.component.html',
  styleUrls: ['./light-analytics.component.scss']
})
export class LightAnalyticsComponent implements OnInit {

  lightsChart: Chart;
  dataLoaded = false;

  constructor() {}

  createLightsChart() {
    const ctx = document.getElementById('lightsChart');
    this.lightsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Temperatuur', 'Vochtigheid'],
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
      this.createLightsChart();
  }

}
