import { Component } from '@angular/core';
import { ReactiveFormsModule, FormControl, FormGroup } from '@angular/forms';
import { DataService } from '../../services/data-service';

@Component({
  selector: 'app-orders',
  imports: [ReactiveFormsModule],
  templateUrl: './orders.html',
  styleUrl: './orders.scss'
})
export class Orders {

  orderForm = new FormGroup({
    customer_name: new FormControl(''),
    customer_address: new FormControl(''),
    items: new FormControl([]) // Initialize with an empty array
  });

  constructor(private dataService: DataService) { }
  ngOnInit() {
    // Initialize the form with default values or fetch from a service if needed
    if (this.dataService.cartItems && this.dataService.cartItems.length > 0) {
      this.orderForm.patchValue({
        items: this.dataService.cartItems
      });
    }
    console.log("Order Form Initialized:", this.orderForm.value);
  }

  submitOrder() {
    console.log("Submitting order:", this.orderForm.value);
    if (this.orderForm.valid) {
      this.dataService.postOrder(this.orderForm.value).subscribe({
        next: (response) => {
          console.log("Order submitted successfully:", response);
          // Optionally, reset the form or navigate to a confirmation page
          this.orderForm.reset();
          this.dataService.cartItems = []; // Clear the cart items after order submission
        },
        error: (error) => {
          console.error("Error submitting order:", error);
        }
      });
    } else {
      console.error("Order form is invalid");
    }
  }
}
