import { Routes } from '@angular/router';
import { First } from './components/first/first';
import { ItemDetails } from './components/item-details/item-details';

export const routes: Routes = [
    { path: 'first', component: First },
    { path: 'item-details/:idInfo', component: ItemDetails},
    { path: '', redirectTo: '/first', pathMatch: 'full' },
];
