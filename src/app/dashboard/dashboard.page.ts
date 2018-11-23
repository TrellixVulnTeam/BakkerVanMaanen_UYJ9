import { Component, OnInit } from '@angular/core';
import { AngularFireList, AngularFireDatabase, AngularFireObject } from 'angularfire2/database';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Vitrine } from '../vitrine';
import { Temperature } from '../temperature';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
  dbRef: AngularFireList<any>;
  vitrine: Observable<any>;
  productStates: any;
  tempData: Observable<any>;
  temp: number;
  humidity: number;
  tempTimestamp: string;
  constructor(private db: AngularFireDatabase) {
    this.dbRef = this.db.list('/');
    this.vitrine = this.db.object('/vitrine').valueChanges();
    this.productStates = this.db.list('/vitrine/products_states').snapshotChanges();
    this.db.object('/temp').valueChanges().subscribe(data => {
      this.temp = data['temperature'];
      this.humidity = data['humidity'];
      this.tempTimestamp = data['timestamp'];
    });
  }

  ngOnInit() {
  }

}
