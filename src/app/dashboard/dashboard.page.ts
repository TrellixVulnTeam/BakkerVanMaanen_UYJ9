import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {
 analyticsMode = false;
 phoneMode = true;

 constructor() { }

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
