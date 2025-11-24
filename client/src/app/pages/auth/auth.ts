import { Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-auth',
  standalone: true,
  templateUrl: './auth.html',
  styleUrls: ['./auth.css'],
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ]
})
export class AuthComponent {

  // --- UI state variables ---
  scrolled = false;
  showLogin = false;
  showSignup = false;

  // --- Login fields ---
  loginEmail = 'test@gmail.com';
  loginPassword = 'test123';

  // --- Signup fields ---
  signupName = '';
  signupEmail = '';
  signupPassword = '';

  constructor(
    private router: Router,
    private snackBar: MatSnackBar,
    private authService: AuthService
  ) {}

  // Detect scroll and toggle header class
  @HostListener('window:scroll', [])
  onScroll() {
    this.scrolled = window.scrollY > 20;
  }

  // ---------------------------
  // LOGIN WITH FIREBASE
  // ---------------------------
  onLogin() {
    if (!this.loginEmail || !this.loginPassword) {
      this.snackBar.open('Please fill in all fields.', 'Close', { duration: 2000 });
      return;
    }

    this.authService.login(this.loginEmail, this.loginPassword)
      .then(() => {
        this.snackBar.open('Login successful!', 'Close', { duration: 2000 });
        this.router.navigate(['/dashboard']);
      })
      .catch(error => {
        this.snackBar.open(error.message, 'Close', { duration: 2000 });
      });
  }

  // ---------------------------
  // SIGNUP WITH FIREBASE
  // ---------------------------
  onSignup() {
    if (!this.signupName || !this.signupEmail || !this.signupPassword) {
      this.snackBar.open('Please complete all fields.', 'Close', { duration: 2000 });
      return;
    }

    this.authService.signup(this.signupEmail, this.signupPassword)
      .then(() => {
        this.snackBar.open('Account created successfully!', 'Close', { duration: 2000 });
        this.router.navigate(['/dashboard']);
      })
      .catch(error => {
        this.snackBar.open(error.message, 'Close', { duration: 2000 });
      });
  }
}
