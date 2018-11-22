import { Component, OnInit } from '@angular/core';
import { AngularFireList, AngularFireDatabase, AngularFireObject } from 'angularfire2/database';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Vitrine } from '../vitrine';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
  dbRef: AngularFireList<any>;
  vitrine: Observable<any>;
  productStates: any;
  constructor(private db: AngularFireDatabase) {
    this.dbRef = this.db.list('/');
    this.vitrine = this.db.object('/vitrine').valueChanges();
    this.productStates = this.db.list('/vitrine/products_states').snapshotChanges();
    this.db.list('/vitrine/products_states').snapshotChanges().subscribe(e => e.map(b => console.log(b.payload.val())));
  }

  ngOnInit() {
  }

}
