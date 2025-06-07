import { Component } from '@angular/core';
import { NgOptimizedImage } from '@angular/common'
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import { DataService } from "../../services/data-service";

@Component({
  selector: 'app-first',
  imports: [NgOptimizedImage, MatCardModule, MatChipsModule],
  templateUrl: './first.html',
  styleUrl: './first.scss'
})
export class First {
  longText = `The Shiba Inu is the smallest of the six original and distinct spitz breeds of dog
  from Japan. A small, agile dog that copes very well with mountainous terrain, the Shiba Inu was
  originally bred for hunting.`;
  items: any;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.dataService.getData().subscribe({
      next: (res) => {
        console.log(res);
        this.items = res;
        console.log(typeof(this.items));
      },
      error: (err) => {
        console.error(err);
      }
    })
  }
}
