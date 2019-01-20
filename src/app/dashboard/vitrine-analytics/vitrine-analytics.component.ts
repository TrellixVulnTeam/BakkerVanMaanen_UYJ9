import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { AngularFireDatabase } from 'angularfire2/database';

export interface Vitrine {
    productName: string;
    productCount: number;
}

@Component({
  selector: 'app-vitrine-analytics',
  templateUrl: './vitrine-analytics.component.html',
  styleUrls: ['./vitrine-analytics.component.scss']
})

export class VitrineAnalyticsComponent implements OnInit {

  vitrineChart: Chart;
  dataLoaded = false;
  vitrineTimestamp: string;
  vitrineLabels = [];
  vitrineDates = [];
  vitrineData = [];
  vitrineCount = [];
  constructor(private db: AngularFireDatabase) {
      this.getVitrineData();
  }

  getVitrineData() {
      this.db.list('/vitrine', ref => ref
      .orderByChild('timestamp')
      .limitToLast(10))
      .valueChanges()
      .subscribe(data => {
          for (const labels of data[data.length - 1]['products']) {
              this.vitrineLabels.push(labels['product_name']);
          }
          data.forEach(entry => {
            this.vitrineDates.push(entry['timestamp']);
            this.vitrineTimestamp = entry['timestamp'];
            entry['products'].forEach(products => {
                if (!products['available']) {
                    this.vitrineData.push(products['product_name']);
                }
            });
         });
            Object.entries(this.countVitrineProducts(this.vitrineData)).forEach(
                ([key, value]) => this.vitrineCount.push(value)
            );
      });
      this.dataLoaded = true;
  }

  countVitrineProducts (vitrine: string[]) {
    return vitrine.reduce((prev, curr) => (prev[curr] = ++prev[curr] || 1, prev), {});
  }

  createVitrineChart() {
    const ctx = document.getElementById('vitrineChart');
    this.vitrineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: this.vitrineLabels,
            datasets: [{
                backgroundColor: ['blue', 'red', 'green', 'orange'],
                data: this.vitrineCount,
            }]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Vitrine producten activiteit',
                fontColor: 'white',
                fontSize: 15
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: 'FFF',
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: 'FFF',
                    }
                }]
            }
        }
    });
    this.dataLoaded = true;
  }

  ngOnInit() {
      this.createVitrineChart();
  }

}
