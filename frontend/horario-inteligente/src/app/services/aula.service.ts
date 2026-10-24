
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Aula {
  id_aula: number;
  codigo: string;
  nombre: string;
  capacidad: number;
  ubicacion: string | null;
  estado: boolean;
}

export interface AulaCreate {
  codigo: string;
  nombre: string;
  capacidad: number;
  ubicacion: string | null;
  estado: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AulaService {
  private readonly apiUrl = 'http://127.0.0.1:8000/api/aulas';

  constructor(private http: HttpClient) {}

  obtenerAulas(): Observable<Aula[]> {
    return this.http.get<Aula[]>(this.apiUrl);
  }

  obtenerAula(id: number): Observable<Aula> {
    return this.http.get<Aula>(`${this.apiUrl}/${id}`);
  }

  crearAula(aula: AulaCreate): Observable<Aula> {
    return this.http.post<Aula>(this.apiUrl, aula);
  }

  actualizarAula(id: number, aula: AulaCreate): Observable<Aula> {
    return this.http.put<Aula>(`${this.apiUrl}/${id}`, aula);
  }

  eliminarAula(id: number): Observable<unknown> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
