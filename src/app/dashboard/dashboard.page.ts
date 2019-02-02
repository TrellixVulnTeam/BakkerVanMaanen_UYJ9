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
 currentNotificationKeys = [];
 newNotifications = false;
 noNewNotifications: String = 'No new notifications';

 constructor(private db: AngularFireDatabase) {
     this.getNotificationKeys();
 }

 playSoundNotification() {
     const audio = new Audio();
     audio.src = '../../assets/sound.mp3';
     audio.load();
     audio.play();
 }

 getNotifications() {
     this.db.list('/notifications', ref => ref
         .orderByChild('seen')
         .equalTo(false)
         .limitToLast(5))
         .valueChanges()
         .subscribe(entries => {
             if (entries.length === 0) {
                this.newNotifications = false;
             } else {
                this.notificationList = entries;
                this.newNotifications = true;
                this.playSoundNotification();
             }
         });
 }

 getNotificationKeys() {
     this.db.list('/notifications', ref => ref
         .orderByChild('seen')
         .equalTo(false)
         .limitToLast(5))
         .snapshotChanges()
         .subscribe(entries => {
             entries.map(payload => {
                this.currentNotificationKeys.push(payload['key']);
             });
             this.getNotifications();
         });
 }

 updateNotificationsSeen() {
     for (const notification of this.currentNotificationKeys) {
        this.db.object('/notifications/' + notification)
            .update({ seen: true });
     }
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
    console.log(this.newNotifications);
  }

}
