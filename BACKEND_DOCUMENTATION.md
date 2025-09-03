# Documentación Técnica del Backend

## 1. Alcance
Este documento ofrece una descripción técnica detallada del código de
backend ubicado en los directorios `ar_catcher` y
`rock-paper-scissors-ai`. Está dirigido a desarrolladores que necesiten
comprender, extender o mantener el sistema.

---

## 2. Visión General de la Arquitectura

### 2.1 Diseño de Alto Nivel
El backend está organizado como dos motores de juego Python independientes.
Cada motor implementa su propia lógica de dominio y solo comparte
librerías de terceros comunes listadas en `requirements.txt`.

```
fain_ai/
├─ ar_catcher/                   # Juego de captura con seguimiento de manos
└─ rock-paper-scissors-ai/       # Juego de gestos Piedra-Papel-Tijeras
```

* Todo el código fuente es compatible con **Python 3.10**.
* Cada juego se inicia mediante un único punto de entrada
  (`game.py` o `main.py`).
* Las tareas computacionalmente intensivas (p. ej. detección de manos
  con MediaPipe) están encapsuladas en clases de servicio dedicadas para
  aislar dependencias externas.

### 2.2 Desglose de Módulos

| Paquete | Módulos Clave | Responsabilidad |
|---------|---------------|-----------------|
| **ar_catcher** | `camera.py` | Captura y pre-procesamiento de fotogramas |
| | `detector.py` | Detección de puntos clave de la mano (MediaPipe) |
| | `objects.py` | Estructuras de datos de sprites y física |
| | `sprite_manager.py` | Carga y caché de recursos gráficos |
| | `game.py` | Bucle principal, puntuación y máquina de estados |
| | `visual_effects.py` | Sistema de partículas y FX de pantalla |
| **rock-paper-scissors-ai** | `src/ai.py` | Estrategia de la computadora |
| | `src/hand_gesture.py` | Clasificación de gestos (MediaPipe) |
| | `src/game.py` | Flujo de partida, temporización y puntuación |
| | `src/gui.py` | Envoltorio GUI basado en Pygame |
| | `src/ui.py` | Widgets de interfaz de alto nivel |

---

## 3. Flujo de Ejecución en Tiempo de Ejecución

1. **Inicialización**
   * Se cargan sprites/sonidos con caché perezosa.
   * Se configuran superficies de Pygame y el reloj de FPS.
2. **Captura de Entrada**
   * Se leen fotogramas RGB de la webcam mediante OpenCV.
   * Los fotogramas se envían a MediaPipe para estimación de puntos clave.
3. **Tick de Lógica del Juego**
   * Se actualizan posiciones de sprites o contadores de partida.
   * Se aplican reglas físicas y detección de colisiones.
   * Se calcula la nueva puntuación y multiplicadores de combo.
4. **Renderizado**
   * Se dibujan fondo, sprites y HUD en la superficie fuera de pantalla.
   * Se muestra la superficie con `pygame.display.flip()`.
5. **Terminación**
   * Se libera la cámara, se limpian recursos y se cierra Pygame.

Cada iteración del bucle se limita a **60 FPS** para garantizar una
experiencia consistente en hardware de gama media.

---

## 4. Matriz de Dependencias

| Categoría | Librería | Propósito |
|-----------|---------|-----------|
| CV Core  | `opencv-python` | Captura de fotogramas y utilidades de imagen |
| ML       | `mediapipe` | Detección en tiempo real de puntos clave |
| Matemáticas | `numpy`, `scipy` | Álgebra lineal e interpolación |
| Audio    | `sounddevice`, `pygame` | Reproducción de efectos de sonido |
| Utilidad | `absl-py`, `dateutil` | Registro y manejo de tiempo |

Todos los paquetes obligatorios están especificados en `requirements.txt`.
Para instalar localmente ejecute:

```bash
python -m pip install -r requirements.txt
```

---

## 5. Estrategia de Manejo de Errores

* **Llamadas externas** (p. ej. OpenCV, MediaPipe): se envuelven en
  `try/except` y se lanzan subclases específicas de `RuntimeError` con
  un mensaje claro.
* Las **invariantes internas** se refuerzan con aserciones de tipo.
* Cada función pública devuelve un objeto de dominio válido o lanza un
  error específico; no se utilizan valores centinela `None`.

```python
class CameraFailure(RuntimeError):
    """Se lanza cuando no se puede inicializar la webcam."""
```

---

## 6. Registro y Telemetría

* Se utiliza el módulo `logging` con formateador **JSON** para facilitar
  la ingesta posterior.
* El nivel por defecto es **INFO**; cambiar a **DEBUG** mediante la
  variable de entorno `LOG_LEVEL`.
* Los archivos de registro rotan diariamente y se almacenan en `./logs/`.

---

## 7. Pruebas

* El proyecto contiene actualmente una sola prueba de carga de sprites
  (`test_sprites.py`). Al agregar nueva funcionalidad mantenga la
  estructura `test_<feature>.py` dentro de cada directorio de juego.
* Se recomienda PyTest ≥ 8.0.

---

## 8. Despliegue

Los juegos están orientados a escritorio y no requieren servidor. Para
la distribución multiplataforma utilice [PyInstaller]. Ejemplo de
compilación en una línea:

```bash
pyinstaller --onefile --name ar_catcher ar_catcher/game.py
```

---

## 9. Mejoras Futuras

* Integrar un equivalente de **date-fns** para Python (p. ej. `pendulum`)
  y unificar el manejo de zonas horarias.
* Refactorizar los envoltorios de MediaPipe duplicados en un paquete
  compartido `vision`.
* Introducir integración continua (CI) para linting y pruebas unitarias.

---

© 2025 FAIN-AI. Todos los derechos reservados.
