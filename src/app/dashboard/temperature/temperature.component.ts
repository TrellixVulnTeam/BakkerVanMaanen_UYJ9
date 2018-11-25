import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';

@Component({
  selector: 'app-temperature',
  templateUrl: './temperature.component.html',
  styleUrls: ['./temperature.component.scss']
})
export class TemperatureComponent implements OnInit {

  //  Temperature variables
  temperature: number;
  humidity: number;
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
    .subscribe(data => data.forEach(entry => {
      //  First object in the list is has the highest timestamp
      //  We can also sort by id, fix!
      this.temperature = entry['temperature'];
      this.humidity = entry['humidity'];
      this.temperatureTimestamp = entry['timestamp'];
      this.dataLoaded = true;
    }));
  }

  ngOnInit() {
  }

}
