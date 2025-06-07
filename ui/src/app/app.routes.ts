import { Routes } from '@angular/router';
import { First } from './components/first/first';

export const routes: Routes = [
    { path: 'first', component: First },
    { path: '', redirectTo: '/first', pathMatch: 'full' },
];
