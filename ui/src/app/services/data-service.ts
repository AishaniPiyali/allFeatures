import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private _dataUrl: string = 'http://localhost:8000';
  public cartItems: any = []; // Array to hold items added to the cart

  constructor(private http: HttpClient) { }

  getData(): Observable<any> {
    return this.http.get<[]>(this._dataUrl + '/myFirstCollection');
  }

  getProductsByCategory(id: any): Observable<any> {
    return this.http.get(this._dataUrl + '/myFirstCollection/' + id + '/products');
  }

  postOrder(order: any): Observable<any> {
    return this.http.post<any>(this._dataUrl + '/orders', order);
  }
}
