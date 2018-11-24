import { Component, OnInit } from '@angular/core';
import { AngularFireList, AngularFireDatabase, AngularFireObject } from 'angularfire2/database';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
  //  Database reference
  dbRef: AngularFireList<any>;
  productStates: any;

  //  For spinner
  dataLoaded = false;

  //  Temperature variables
  temp: number;
  humidity: number;
  tempTimestamp: string;

  constructor(private db: AngularFireDatabase) {
    this.dbRef = this.db.list('/');
    this.loadProductStates();
    this.loadTempData();
  }

  private loadProductStates() {
    this.productStates = this.db.list('/vitrine/products_states').snapshotChanges();
  }

  private loadTempData() {
    this.db.object('/temp').valueChanges().subscribe(data => {
      this.temp = data['temperature'];
      this.humidity = data['humidity'];
      this.tempTimestamp = data['timestamp'];
      this.dataLoaded = true;
    });
  }

  ngOnInit() {
  }

}
