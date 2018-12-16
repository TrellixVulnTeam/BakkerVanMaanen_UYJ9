import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase  } from 'angularfire2/database';

@Component({
  selector: 'app-klanten',
  templateUrl: './klanten.component.html',
  styleUrls: ['./klanten.component.scss']
})
export class KlantenComponent implements OnInit {

  //  Temperature variables
  klantenCount: number;
  klantenIdleTime: number;
  klantenTimestamp: string;
  //  For spinner
  dataLoaded = false;

  constructor(private db: AngularFireDatabase) {
      this.getKlantenData();
      console.log(this.klantenIdleTime);
  }

  /**
   * Get latest temperature data
   */
  private getKlantenData() {
    this.db.list('/klanten', ref => ref
    .orderByChild('timestamp')
    .limitToLast(1))
    .valueChanges()
    .subscribe(data => data.forEach(entry => {
        this.klantenTimestamp = entry['timestamp'];
        this.klantenCount = entry['klanten_data']['klanten_count'];
        this.klantenIdleTime = entry['klanten_data']['klanten_idle_time'];
        this.dataLoaded = true;
    }));
  }

  ngOnInit() {

  }
 }
