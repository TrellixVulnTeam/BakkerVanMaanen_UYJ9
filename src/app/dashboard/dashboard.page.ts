import { Component, OnInit } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
 analyticsMode = false;
 phoneMode = true;
 showNotifications = false;
 notificationList = {};
 constructor(private db: AngularFireDatabase) {
     this.getNotifications();
 }

 getNotifications() {
     this.db.list('/notifications', ref => ref
         .orderByChild('timestamp')
         .limitToLast(5))
         .valueChanges()
         .subscribe(entries => {
            this.notificationList = entries;
         });
 }

 toggleNotifications() {
     if (this.showNotifications === true) {
         this.showNotifications = false;
     } else if (this.showNotifications === false) {
         this.showNotifications = true;
     }
 }

  toggleView(mode: number) {
      if (mode === 1) {
          this.analyticsMode = true;
          this.phoneMode = false;
      }
      if (mode === 0) {
          this.phoneMode = true;
          this.analyticsMode = false;
      }
  }
  ngOnInit() {
  }

}
