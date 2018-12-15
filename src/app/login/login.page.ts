import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { NavController, AlertController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss']
})
export class LoginPage implements OnInit {
  user: string;
  password: string;

  constructor(public alertCtrl: AlertController, public navCtrl: NavController) { }

  login() {
    if (this.user === '111' && this.password === '111') {
       this.goToDashboard();
    } else {
       this.loginFailedAlert();
    }
  }

  async loginFailedAlert() {
    const alert = await this.alertCtrl.create({
      header: 'LOGIN MISLUKT',
      subHeader: '',
      message: 'Je werknemersnummer en/of wachtwoord was nrect ingevoerd.',
      buttons: ['Probeer opnieuw'],
      cssClass: 'loginAlert'
    });
    await alert.present();
  }

  ngOnInit() {
  }

  goToDashboard() {
    this.navCtrl.navigateForward('dashboard');
  }

}
