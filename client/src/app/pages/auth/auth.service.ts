import { Injectable } from '@angular/core';
import { Auth, signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from '@angular/fire/auth';

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private auth: Auth) {}

  // ---------------------------
  // LOGIN
  // ---------------------------
  login(email: string, password: string) {
    return signInWithEmailAndPassword(this.auth, email, password);
  }

  // ---------------------------
  // SIGNUP (with displayName)
  // ---------------------------
  async signup(email: string, password: string, fullName: string) {
    // Create the user
    const userCredential = await createUserWithEmailAndPassword(this.auth, email, password);

    // Update displayName
    if (userCredential.user) {
      await updateProfile(userCredential.user, {
        displayName: fullName
      });
    }

    return userCredential;
  }
}
