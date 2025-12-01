import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GroceryService {
  // FIX: Updated to your local network IP so your phone can reach the backend
  private baseUrl = 'http://10.0.0.141:5000'; 

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
  // Calls the /compare/<image_name>/<csv_name> endpoint on the Flask server
  compareItems(imageName: string, csvName: string): Observable<any> {
    return this.http.get(
      `${this.baseUrl}/compare/${imageName}/${csvName}`
    );
  }
}