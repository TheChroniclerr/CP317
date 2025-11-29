import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  // Your Flask backend endpoint
  private apiUrl = 'http://localhost:8080/api/data';

  constructor(private http: HttpClient) {}

  uploadImage(file: File) {
  const formData = new FormData();
  formData.append('image', file);

  return this.http.post<any>('http://localhost:8080/api/extract', formData);
}


}
