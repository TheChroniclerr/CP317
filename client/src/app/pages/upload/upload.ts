import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css'],
})
export class UploadComponent {
  selectedImage: File | null = null;
  loading = false;
  result: any = null;

  constructor() {}

  // When a user selects or captures an image
  onCameraCapture(event: any) {
    this.selectedImage = event.target.files[0] || null;
    this.previewImage();
    this.uploadImage();
  }

  // Preview before upload
  previewImage() {
    if (!this.selectedImage) return;

    const reader = new FileReader();
    reader.onload = () => {
      // You can bind preview if needed
    };
    reader.readAsDataURL(this.selectedImage);
  }

  // Upload to Python backend
  uploadImage() {
    if (!this.selectedImage) return;

    this.loading = true;
    this.result = null;

    const formData = new FormData();
    formData.append('image', this.selectedImage);

    fetch('http://localhost:8080/analyze-image', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        this.result = data.items; // AI output list
      })
      .catch(err => console.error('Upload error:', err))
      .finally(() => {
        this.loading = false;
      });
  }
}
