import { Routes } from '@angular/router';
import { AuthComponent } from './pages/auth/auth';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { ShoppingListComponent } from './pages/shopping-list/shopping-list';
import { UploadComponent } from './pages/upload/upload';
import { CartComponent } from './pages/cart/cart';

export const routes: Routes = [
  { path: '', component: AuthComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'shopping-list', component: ShoppingListComponent },
  { path: 'upload', component: UploadComponent },
  { path: 'cart', component: CartComponent },
];
