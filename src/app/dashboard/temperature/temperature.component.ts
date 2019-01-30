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
  //  For spinner
  dataLoaded = false;

  constructor(private db: AngularFireDatabase) {
      this.getTemperatureData();
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
            entry['temperature_sensors'].forEach(sensor => {
                if (sensor['temperature'] < 20 || sensor['temperature'] > 26) {
                    // push
                }
            });
            this.dataLoaded = true;
        });
    });
  }

  ngOnInit() {
  }

}
