import { Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar'; // Import Config
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
  loginEmail = '';
  loginPassword = '';

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

  // Helper for nice notifications
  private showNotification(message: string, isError: boolean = false) {
    const config: MatSnackBarConfig = {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'bottom',
      panelClass: isError ? ['error-snackbar'] : ['success-snackbar'] // You can style these classes in global styles.css if needed
    };
    this.snackBar.open(message, 'Close', config);
  }

  // ---------------------------
  // LOGIN WITH FIREBASE
  // ---------------------------
  onLogin() {
    if (!this.loginEmail || !this.loginPassword) {
      this.showNotification('Please fill in all fields.', true);
      return;
    }

    this.authService.login(this.loginEmail, this.loginPassword)
      .then(() => {
        this.showNotification('Welcome back! Login successful.');
        this.router.navigate(['/dashboard']);
      })
      .catch(error => {
        // Customize error messages if needed
        let msg = 'Login failed. Please check your credentials.';
        if (error.code === 'auth/user-not-found') msg = 'No account found with this email.';
        if (error.code === 'auth/wrong-password') msg = 'Incorrect password.';
        
        this.showNotification(msg, true);
      });
  }

  // ---------------------------
  // SIGNUP WITH FIREBASE
  // ---------------------------
  onSignup() {
    if (!this.signupName || !this.signupEmail || !this.signupPassword) {
      this.showNotification('Please complete all fields.', true);
      return;
    }

    this.authService.signup(this.signupEmail, this.signupPassword, this.signupName)
      .then(() => {
        this.showNotification('Account created successfully! Welcome to Refillr.');
        this.router.navigate(['/dashboard']);
      })
      .catch(error => {
        let msg = 'Signup failed. Please try again.';
        if (error.code === 'auth/email-already-in-use') msg = 'This email is already registered.';
        if (error.code === 'auth/weak-password') msg = 'Password should be at least 6 characters.';

        this.showNotification(msg, true);
      });
  }
}