import { Routes } from '@angular/router';
import { First } from './components/first/first';
import { ItemDetails } from './components/item-details/item-details';
import { Orders } from './components/orders/orders';

export const routes: Routes = [
    { path: 'first', component: First },
    { path: 'item-details/:idInfo', component: ItemDetails},
    { path: 'orders', component: Orders },
    { path: '', redirectTo: '/first', pathMatch: 'full' },
];
