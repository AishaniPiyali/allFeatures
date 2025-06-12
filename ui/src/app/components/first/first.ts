import { Component } from '@angular/core';
import { NgOptimizedImage } from '@angular/common'
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import { DataService } from "../../services/data-service";
import { Router } from '@angular/router';

@Component({
  selector: 'app-first',
  imports: [NgOptimizedImage, MatCardModule, MatChipsModule],
  templateUrl: './first.html',
  styleUrl: './first.scss'
})
export class First {
  
  items: any;

  constructor(private dataService: DataService, private router: Router) {}

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

  viewItemDetails(item: any) {
    this.router.navigate(['/item-details/'+item]);
  }
}
