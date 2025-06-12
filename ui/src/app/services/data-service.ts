import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private _dataUrl: string = 'http://localhost:8000/myFirstCollection';

  constructor(private http: HttpClient) { }

  getData(): Observable<any> {
    return this.http.get<[]>(this._dataUrl);
  }

  getProductsByCategory(id: any): Observable<any> {
    return this.http.get(this._dataUrl + '/' + id + '/products');
  }
}
