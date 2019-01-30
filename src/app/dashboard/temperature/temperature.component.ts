import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.scss']
})
export class TemperatureComponent implements OnInit {

  //  Temperature variables
  temperatureData: any;
  temperatureTimestamp: string;
  humidityAverage = 0;
  temperatureAverage = 0;
  //  For spinner
  dataLoaded = false;

  constructor(private db: AngularFireDatabase) {
      this.getTemperatureData();
      this.getAverageTemperatureForToday();
  }
  /**
   * Get latest temperature data
   */
  private getTemperatureData() {
    this.db.list('/temperature', ref => ref
    .orderByChild('timestamp')
    .limitToLast(1))
    .valueChanges()
    .subscribe(data => {
        data.forEach(entry => {
            this.temperatureTimestamp = entry['timestamp'];
            this.temperatureData = entry['temperature_sensors'];
            });
            this.dataLoaded = true;
    });
  }

  getAverageTemperatureForToday() {
    const today = new Date().toLocaleDateString();
    this.db.list('/temperature', ref => ref
        .orderByChild('timestamp')
        .limitToLast(96))
        .valueChanges()
        .subscribe(entries => {
            entries.forEach(entry => {
                entry['temperature_sensors'].forEach(data => {
                    this.humidityAverage += data['humidity'];
                    this.temperatureAverage += data['temperature'];
                });
            });
        this.humidityAverage = this.humidityAverage / 288;
        this.temperatureAverage = this.temperatureAverage / 288;
    });
  }

  ngOnInit() {
  }

}
