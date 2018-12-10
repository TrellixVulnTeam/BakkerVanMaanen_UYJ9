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
        this.temperatureData = data[0]['temperature_sensors']
        this.temperatureTimestamp = data[0]['timestamp']
        this.dataLoaded = true;
    });  
  }

  ngOnInit() {
  }

}
