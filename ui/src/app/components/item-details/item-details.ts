import { Component, Input } from '@angular/core';
import { DataService } from "../../services/data-service";

@Component({
  selector: 'app-item-details',
  imports: [],
  templateUrl: './item-details.html',
  styleUrl: './item-details.scss'
})
export class ItemDetails {

  @Input()
  idInfo!: string;

  constructor(private dataService: DataService) {}
  ngOnInit() {
    console.log(this.idInfo);
    this.dataService.getProductsByCategory(this.idInfo).subscribe({
      next: (res) => {
        console.log(res);
      },
      error: (err) => {
        console.error(err);
      }
    })
  }
}
