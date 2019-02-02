import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase  } from 'angularfire2/database';

@Component({
  selector: 'app-klanten',
  templateUrl: './klanten.component.html',
  styleUrls: ['./klanten.component.scss']
})
export class KlantenComponent implements OnInit {

  //  Klanten variables
  klantenCount: number;
  klantenIdleTime: number;
  klantenTimestamp: string;
  //  For spinner
  dataLoaded = false;

  constructor(private db: AngularFireDatabase) {
      this.getKlantenData();
  }

  /**
   * Get latest klanten data
   */
  private getKlantenData() {
    this.db.list('/klanten', ref => ref
    .orderByChild('timestamp')
    .limitToLast(1))
    .valueChanges()
    .subscribe(data => data.forEach(entry => {
        this.klantenTimestamp = entry['timestamp'];
        this.klantenCount = entry['klanten_count'];
        this.klantenIdleTime = entry['klanten_idle_time'];
        this.dataLoaded = true;
    }));
  }

  ngOnInit() {}
 }
