import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// TODO: Move to a setting module
const IP = 'http://127.0.0.1:5000';
const API = `${IP}/api/v1`;

@Injectable({
    providedIn: 'root'
})
export class CategoriesService {

    constructor(private http: HttpClient) { }

    fetchCategories(): Observable<any> {
        return this.http.get(`${API}/categories`);
    }

}
