import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-lights',
  templateUrl: './lights.component.html',
  styleUrls: ['./lights.component.scss']
})
export class LightsComponent implements OnInit {

  lightsTimestamp: string;
  //  For spinner
  dataLoaded = false;
  constructor() { }

  ngOnInit() {
  }

}
