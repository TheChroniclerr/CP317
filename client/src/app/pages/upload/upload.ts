import { Component } from '@angular/core';
import { CommonModule, JsonPipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, JsonPipe],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css'],
})
export class UploadComponent {

  selectedImage: File | null = null;
  loading = false;
  result: any = null;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any) {
    this.selectedImage = event.target.files[0];
    this.upload();
  }

  onCameraCapture(event: any) {
    this.selectedImage = event.target.files[0];
    this.upload();
  }

  upload() {
    if (!this.selectedImage) return;

    this.loading = true;

    const formData = new FormData();
    formData.append('image', this.selectedImage);

    this.http.post('http://127.0.0.1:8000/analyze-fridge', formData)
      .subscribe({
        next: (res) => {
          this.result = res;
          this.loading = false;
        },
        error: () => {
          this.loading = false;
        }
      });
  }
}
