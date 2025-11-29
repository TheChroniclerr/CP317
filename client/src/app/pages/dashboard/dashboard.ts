import { Component } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { Auth } from '@angular/fire/auth';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'],
  imports: [RouterModule, MatButtonModule, CommonModule],
})
export class DashboardComponent {
  menuOpen = false;

  userName: string = '';
  userPfp: string = '';

  constructor(private router: Router, private auth: Auth) {
    const user = this.auth.currentUser;

    if (user) {
      // Full name from signup
      this.userName = user.displayName || 'User';

      // Random avatar
      const randomId = Math.floor(Math.random() * 70) + 1;
      this.userPfp = `https://i.pravatar.cc/150?img=${randomId}`;
    }
  }

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }

  logout() {
    this.menuOpen = false;
    this.router.navigate(['/']);
  }
}
