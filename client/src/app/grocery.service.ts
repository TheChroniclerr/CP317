import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GroceryService {
  // DYNAMIC URL: Uses the hostname from the browser address bar.
  // If you visit http://10.0.0.141:4200, this becomes http://10.0.0.141:5000
  // If you visit http://localhost:4200, this becomes http://localhost:5000
  private baseUrl = `http://${window.location.hostname}:5000`;

  constructor(private http: HttpClient) {}

  // 1. Upload File (Used by Image Upload and Wishlist CSV)
  uploadFile(file: File): Observable<{ message: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{ message: string; filename: string }>(
      `${this.baseUrl}/upload`,
      formData
    );
  }

  // 2. Compare Items 
  compareItems(imageName: string, csvName: string): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/compare/${imageName}/${csvName}`
    );
  }
}