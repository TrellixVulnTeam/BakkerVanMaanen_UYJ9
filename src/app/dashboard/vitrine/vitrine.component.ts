import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';

@Component({
  selector: 'app-vitrine',
  templateUrl: './vitrine.component.html',
  styleUrls: ['./vitrine.component.scss']
})
export class VitrineComponent implements OnInit {

  //  Vitrine variables
  vitrineState: any;
  vitrineCount: any;
  vitrineTimestamp: string;
  //  For spinner
  dataLoaded = false;

  constructor(private db: AngularFireDatabase) {
    this.getVitrineState();
  }

  /**
   * Get latest vitrine state
   */
  private getVitrineState() {
    this.db.list('/vitrine', ref => ref
    .orderByChild('timestamp')
    .limitToLast(1))
    .valueChanges().
    subscribe(data => data
      .forEach(entry => {
        this.vitrineState = entry['products'];
        this.vitrineTimestamp = entry['timestamp'];
        this.vitrineCount = entry['product_count'];
        this.dataLoaded = true;
    }));
  }

  ngOnInit() {
  }

}
