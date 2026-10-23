
import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { Aula, AulaCreate, AulaService } from './services/aula.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private readonly aulaService = inject(AulaService);

  aulas: Aula[] = [];
  aulasFiltradas: Aula[] = [];

  buscando = false;
  guardando = false;
  mensaje = '';
  tipoMensaje: 'exito' | 'error' = 'exito';
  busqueda = '';

  modoFormulario: 'crear' | 'editar' | 'ver' = 'crear';
  mostrarFormulario = false;
  idSeleccionado: number | null = null;

  formulario: AulaCreate = this.formularioVacio();

  formularioVacio(): AulaCreate {
    return {
      codigo: '',
      nombre: '',
      capacidad: 1,
      ubicacion: '',
      estado: true
    };
  }

  ngOnInit(): void {
    this.cargarAulas();
  }

  cargarAulas(): void {
    this.buscando = true;

    this.aulaService.obtenerAulas().subscribe({
      next: (datos) => {
        this.aulas = datos;
        this.filtrarAulas();
        this.buscando = false;
      },
      error: (error: HttpErrorResponse) => {
        this.buscando = false;
        this.mostrarMensaje(
          this.obtenerError(error),
          'error'
        );
      }
    });
  }

  filtrarAulas(): void {
    const termino = this.busqueda.trim().toLowerCase();

    this.aulasFiltradas = this.aulas.filter((aula) =>
      aula.codigo.toLowerCase().includes(termino) ||
      aula.nombre.toLowerCase().includes(termino) ||
      (aula.ubicacion ?? '').toLowerCase().includes(termino)
    );
  }

  abrirCrear(): void {
    this.modoFormulario = 'crear';
    this.idSeleccionado = null;
    this.formulario = this.formularioVacio();
    this.mostrarFormulario = true;
    this.mensaje = '';
  }

  abrirEditar(aula: Aula): void {
    this.modoFormulario = 'editar';
    this.idSeleccionado = aula.id_aula;

    this.formulario = {
      codigo: aula.codigo,
      nombre: aula.nombre,
      capacidad: aula.capacidad,
      ubicacion: aula.ubicacion ?? '',
      estado: aula.estado
    };

    this.mostrarFormulario = true;
    this.mensaje = '';
  }

  abrirDetalle(aula: Aula): void {
    this.modoFormulario = 'ver';
    this.idSeleccionado = aula.id_aula;

    this.formulario = {
      codigo: aula.codigo,
      nombre: aula.nombre,
      capacidad: aula.capacidad,
      ubicacion: aula.ubicacion ?? '',
      estado: aula.estado
    };

    this.mostrarFormulario = true;
    this.mensaje = '';
  }

  cerrarFormulario(): void {
    if (this.guardando) {
      return;
    }

    this.mostrarFormulario = false;
    this.idSeleccionado = null;
  }

  guardarAula(): void {
    if (this.guardando || this.modoFormulario === 'ver') {
      return;
    }

    const datos: AulaCreate = {
      codigo: this.formulario.codigo.trim(),
      nombre: this.formulario.nombre.trim(),
      capacidad: Number(this.formulario.capacidad),
      ubicacion: this.formulario.ubicacion?.trim() || null,
      estado: this.formulario.estado
    };

    if (
      !datos.codigo ||
      !datos.nombre ||
      !Number.isInteger(datos.capacidad) ||
      datos.capacidad <= 0
    ) {
      this.mostrarMensaje(
        'Ingresa un código, nombre y capacidad válida mayor que cero.',
        'error'
      );
      return;
    }

    this.guardando = true;

    const peticion = this.modoFormulario === 'editar' &&
      this.idSeleccionado !== null
      ? this.aulaService.actualizarAula(this.idSeleccionado, datos)
      : this.aulaService.crearAula(datos);

    peticion.subscribe({
      next: () => {
        this.guardando = false;
        this.mostrarFormulario = false;

        this.mostrarMensaje(
          this.modoFormulario === 'editar'
            ? 'El aula se actualizó correctamente.'
            : 'El aula se registró correctamente.',
          'exito'
        );

        this.cargarAulas();
      },
      error: (error: HttpErrorResponse) => {
        this.guardando = false;
        this.mostrarMensaje(this.obtenerError(error), 'error');
      }
    });
  }

  eliminarAula(aula: Aula): void {
    const confirmar = window.confirm(
      `¿Deseas desactivar el aula "${aula.nombre}" (${aula.codigo})?`
    );

    if (!confirmar) {
      return;
    }

    this.aulaService.eliminarAula(aula.id_aula).subscribe({
      next: () => {
        this.mostrarMensaje(
          'La operación de eliminación se realizó correctamente.',
          'exito'
        );
        this.cargarAulas();
      },
      error: (error: HttpErrorResponse) => {
        this.mostrarMensaje(this.obtenerError(error), 'error');
      }
    });
  }

  mostrarMensaje(
    texto: string,
    tipo: 'exito' | 'error'
  ): void {
    this.mensaje = texto;
    this.tipoMensaje = tipo;
  }

  obtenerError(error: HttpErrorResponse): string {
    if (error.status === 0) {
      return 'No se pudo conectar con FastAPI. Verifica que el backend esté ejecutándose.';
    }

    if (typeof error.error?.detail === 'string') {
      return error.error.detail;
    }

    if (Array.isArray(error.error?.detail)) {
      return error.error.detail
        .map((detalle: { msg?: string }) => detalle.msg ?? 'Dato inválido')
        .join('. ');
    }

    return `Ocurrió un error al comunicarse con el servidor (HTTP ${error.status}).`;
  }

  get totalAulas(): number {
    return this.aulas.length;
  }

  get aulasActivas(): number {
    return this.aulas.filter((aula) => aula.estado).length;
  }

  get capacidadTotal(): number {
    return this.aulas
      .filter((aula) => aula.estado)
      .reduce((total, aula) => total + aula.capacidad, 0);
  }
}
