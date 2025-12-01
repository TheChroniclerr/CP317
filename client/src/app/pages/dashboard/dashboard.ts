import { Component } from '@angular/core'; // Removed 'computed'
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common'; 
import { FormsModule } from '@angular/forms';     
import { Auth } from '@angular/fire/auth';

// Material Imports
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';

// Import Service
import { GroceryService } from '../../grocery.service';

// --- 1. DEFINE THE SHAPE OF YOUR DATA ---
export interface ShoppingOption {
  walmart?: { price: number; link: string };
  amazon?: { price: number; link: string };
  error?: string;
}

export interface ComparisonResponse {
  analysis: {
    items_detected_in_image: string[];
    items_in_wishlist: string[];
  };
  results: {
    available: string[];
    missing: string[];
  };
  shopping_options: { [key: string]: ShoppingOption }; 
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'],
  imports: [
    RouterModule, 
    CommonModule, 
    FormsModule, 
    MatButtonModule, 
    MatInputModule, 
    MatIconModule,
    MatCardModule
  ], 
})
export class DashboardComponent {
  // --- UI State ---
  menuOpen = false;
  userName: string = '';
  userPfp: string = '';

  // --- Image Upload State ---
  selectedImage: File | null = null;
  imagePreviewUrl: string | null = null;
  uploadedImageName: string = ''; 
  isUploadingImage = false;

  // --- Wishlist State ---
  wishlistItems: string[] = [];
  newItem: string = '';
  uploadedCsvName: string = ''; 
  isUploadingCsv = false;

  // --- Analysis State ---
  analysisResult: ComparisonResponse | null = null; 
  isAnalyzing = false;
  errorMessage = '';

  constructor(
    private router: Router, 
    private auth: Auth,
    private groceryService: GroceryService
  ) {
    const user = this.auth.currentUser;
    if (user) {
      this.userName = user.displayName || 'User';
      const randomId = Math.floor(Math.random() * 70) + 1;
    }
  }

  // --- FIX: Standard Helper Method (Not Computed) ---
  // This allows Angular to check the status automatically
  isReadyToAnalyze(): boolean {
    return this.uploadedImageName !== '' && this.uploadedCsvName !== '';
  }

  // --- 1. IMAGE UPLOAD ---
  onImageSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedImage = file;
      
      const reader = new FileReader();
      reader.onload = () => this.imagePreviewUrl = reader.result as string;
      reader.readAsDataURL(file);

      this.uploadImageToBackend(file);
    }
  }

  uploadImageToBackend(file: File) {
    this.isUploadingImage = true;
    this.groceryService.uploadFile(file).subscribe({
      next: (res) => {
        this.uploadedImageName = res.filename;
        this.isUploadingImage = false;
        console.log('Image uploaded:', this.uploadedImageName);
      },
      error: (err) => {
        console.error('Image upload failed', err);
        this.isUploadingImage = false;
        this.errorMessage = 'Failed to upload image.';
      }
    });
  }

  // --- 2. WISHLIST LOGIC ---
  addWishlistItem() {
    if (this.newItem.trim()) {
      this.wishlistItems.push(this.newItem.trim());
      this.newItem = ''; 
    }
  }

  removeWishlistItem(index: number) {
    this.wishlistItems.splice(index, 1);
  }

  saveAndUploadWishlist() {
    if (this.wishlistItems.length === 0) return;

    this.isUploadingCsv = true;

    const csvContent = this.wishlistItems.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const file = new File([blob], 'wishlist.csv');

    this.groceryService.uploadFile(file).subscribe({
      next: (res) => {
        this.uploadedCsvName = res.filename; 
        this.isUploadingCsv = false;
        console.log('Wishlist uploaded:', this.uploadedCsvName);
      },
      error: (err) => {
        console.error('CSV upload failed', err);
        this.isUploadingCsv = false;
        this.errorMessage = 'Failed to upload wishlist.';
      }
    });
  }

  // --- 3. ANALYSIS LOGIC ---
  runAnalysis() {
    if (!this.isReadyToAnalyze()) return;

    this.isAnalyzing = true;
    this.errorMessage = '';
    this.analysisResult = null;

    this.groceryService.compareItems(this.uploadedImageName, this.uploadedCsvName)
      .subscribe({
        next: (data) => {
          this.analysisResult = data as ComparisonResponse;
          this.isAnalyzing = false;
        },
        error: (err) => {
          console.error(err);
          this.errorMessage = 'Analysis failed. Check backend connection.';
          this.isAnalyzing = false;
        }
      });
  }

  // --- 4. UI HELPERS ---
  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }

  logout() {
    this.menuOpen = false;
    this.auth.signOut().then(() => {
      this.router.navigate(['/']);
    });
  }

  reset() {
    this.selectedImage = null;
    this.imagePreviewUrl = null;
    this.wishlistItems = [];
    this.analysisResult = null;
    this.uploadedImageName = '';
    this.uploadedCsvName = '';
  }
}