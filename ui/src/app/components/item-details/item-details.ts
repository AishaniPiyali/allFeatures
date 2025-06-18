import { Component, Input } from '@angular/core';
import { DataService } from "../../services/data-service";
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { Router } from '@angular/router';

@Component({
  selector: 'app-item-details',
  imports: [MatChipsModule, MatCardModule],
  templateUrl: './item-details.html',
  styleUrl: './item-details.scss'
})
export class ItemDetails {

  @Input()
  idInfo!: string;

  items: any; // Add this property to hold the items
  cartItems: any = []; // Array to hold items added to the cart

  constructor(private dataService: DataService, private router: Router) { }

  ngOnInit() {
    console.log(this.idInfo);
    this.dataService.getProductsByCategory(this.idInfo).subscribe({
      next: (res) => {
        console.log(res);
        this.items = res;
      },
      error: (err) => {
        console.error(err);
      }
    })
  }

  viewItemDetails(arg0: any) {
    throw new Error('Method not implemented.');
  }

  addToCart(itemId: any) {
    console.log("Adding item to cart:", itemId);
    for (let i = 0; i < this.items.length; i++) {
      if (this.items[i].id === itemId) {
        this.cartItems.push(this.items[i]);
        break;
      }
    }
    this.dataService.cartItems = this.cartItems; // Update the cart items in the data service
    console.log("Current cart items:", this.cartItems);
  }

  placeOrder() {
    console.log("Placing order for item:");
    this.router.navigate(['/orders']);
  }
}
