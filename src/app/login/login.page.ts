import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss']
})
export class LoginPage implements OnInit {
  user: string;
  passowrd: string;

  constructor(public navCtrl: NavController) { }

  login(){
  if (this.user === "111" && this.password === "111") {
       this.goToDashboard(); 
    } 
  }

  ngOnInit() {
  }

  goToDashboard() {
    this.navCtrl.navigateForward('dashboard');
  }

}
