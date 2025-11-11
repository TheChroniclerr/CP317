import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';


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
  signupName = '';
  signupEmail = '';
  signupPassword = '';
  showSignup = false;
  loginEmail = "test@gmail.com";
  loginPassword = "test123";
  scrolled = false;

  showLogin = false;

  constructor(private router: Router, private snackBar: MatSnackBar) {}

onLogin() {
  if (this.loginEmail && this.loginPassword) {
    this.snackBar.open('Login successful!', 'Close', { duration: 2000 });
    this.router.navigate(['/dashboard']);
  } else {
    this.snackBar.open('Please fill in all fields.', 'Close', { duration: 2000 });
  }
}

onSignup() {
  if (this.signupName && this.signupEmail && this.signupPassword) {
    this.snackBar.open('Account created successfully!', 'Close', { duration: 2000 });
    this.router.navigate(['/dashboard']);
  } else {
    this.snackBar.open('Please complete all fields.', 'Close', { duration: 2000 });
  }
}

  
}
