# Guía de Instalación y Puesta en Marcha

Este repositorio contiene dos juegos desarrollados en Python que hacen
uso de visión por computador y detección de gestos en tiempo real:

1. **AR Catcher** (`ar_catcher/`)
2. **Rock-Paper-Scissors AI** (`rock-paper-scissors-ai/`)

A continuación encontrarás instrucciones paso a paso para clonar el
proyecto, instalar las dependencias y ejecutar cada juego.

---

## 1. Requisitos Previos

* **Sistema operativo:** Windows, macOS o Linux
* **Python:** 3.10 o superior
* **Git** (opcional, para clonar el repositorio)
* **Webcam** funcional

> 💡 Para Windows se recomienda instalar Python mediante el instalador
> oficial que incluye `pip`.

---

## 2. Clonar el Proyecto

```bash
# Clona el repositorio (cambia la URL si usas SSH)
git clone https://github.com/tu-usuario/fain_ai.git
cd fain_ai
```

---

## 3. Crear y Activar un Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Verás el prefijo `(venv)` en la terminal indicando que el entorno está
activo.

---

## 4. Instalar Dependencias

Todas las librerías comunes se listan en `requirements.txt` en la raíz:

```bash
pip install -r requirements.txt
```

Esto descargará OpenCV, MediaPipe, Pygame y demás paquetes necesarios.

---

## 5. Probar la Carga de Sprites (opcional)

```bash
python ar_catcher/test_sprites.py
```

El script verifica que todos los archivos PNG existen y pueden leerse.

---

## 6. Ejecutar los Juegos

### 6.1 AR Catcher

```bash
python ar_catcher/game.py
```

* **Teclas rápidas**
  * `P` – Pausar / reanudar
  * `Q` – Salir

### 6.2 Rock-Paper-Scissors AI

```bash
python rock-paper-scissors-ai/main.py
```

Muestra tus gestos (piedra, papel o tijeras) frente a la webcam y compite
contra la IA. Pulsa `ESC` para cerrar la ventana.

---

## 7. Solución de Problemas Comunes

| Síntoma | Causa Probable | Solución |
|---------|----------------|----------|
| **La webcam no se abre** | Otra aplicación la está usando | Cierra la app o reinicia la cámara. |
| **ImportError: DLL load failed** | Falta MSVC / libGL | Instala los runtime de Visual C++ (Windows) o `libgl1-mesa` (Linux). |
| **Lentitud / FPS bajos** | Hardware limitado | Reduce la resolución de la webcam o desactiva efectos. |

---

## 8. Empaquetado en Ejecutable (opcional)

Para distribuir un ejecutable independiente usa **PyInstaller**:

```bash
pyinstaller --onefile --name ar_catcher ar_catcher/game.py
```

Generará un binario en `dist/`. Repite el proceso para el segundo juego
cambiando el script principal.

---

## 9. Estructura del Proyecto

```text
fain_ai/
├── ar_catcher/
│   └── ...
├── rock-paper-scissors-ai/
│   └── ...
├── requirements.txt
├── BACKEND_DOCUMENTACIÓN.md
├── FRONTEND_DOCUMENTACIÓN.md
└── README.md  ← (este archivo)
```

---

¡Disfruta de los juegos y siéntete libre de contribuir! 🎮
