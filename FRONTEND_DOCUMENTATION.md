# Documentación Técnica del Front-End

## 1. Alcance
Este documento describe la capa de presentación utilizada por las
aplicaciones de escritorio ubicadas en `ar_catcher` y
`rock-paper-scissors-ai`. Aunque el código está escrito en Python (no en
HTML/CSS), lo denominamos *front-end* porque gestiona los gráficos en
pantalla, las animaciones y la interacción con el usuario.

---

## 2. Pila Gráfica

1. **OpenCV** – captura y entrega fotogramas de la webcam.
2. **MediaPipe** – detecta puntos clave de la mano (entrada para la
   lógica del juego).
3. **NumPy** – proporciona álgebra de píxeles de alto rendimiento.
4. **Pygame** – maneja la ventana, el blitting y el audio.

El renderizado finaliza en un único `pygame.Surface` mostrado mediante
`pygame.display.flip()` en cada fotograma.

---

## 3. Sistemas de Coordenadas

| Componente   | Resolución | Origen     | Notas                               |
|--------------|-----------:|-----------|-------------------------------------|
| Flujo webcam | 720 × 720  | Esquina sup. izda. | Redimensionado a cuadrado. |
| Lienzo main  | 1280 × 720 | Esquina sup. izda. | Contiene feed + HUD.        |
| Iconos HUD   | 100 × 100  | Panel derecho      |                               |

Todas las funciones esperan canales **BGR** para mantener la
compatibilidad con imágenes OpenCV.

---

## 4. Mapa de Módulos

| Paquete | Módulo         | Rol                                    |
|---------|---------------|----------------------------------------|
| **rock-paper-scissors-ai** | `src/gui.py` | Ayudantes de composición principal |
| | `src/ui.py`     | Fachada pública usada por el bucle principal |
| | `src/animations.py` | Animación de texto de ganador             |
| | `src/assets.py` | Carga y redimensiona iconos de gestos       |
| **ar_catcher** | `visual_effects.py` | Sacudida de pantalla, flashes, estelas |
| | `objects.py` | Ayudantes de sprite y colisión               |

---

## 5. Canal de Renderizado (por fotograma)

```text
┌─ captura de fotograma (OpenCV)
│
├─ actualización de estado de juego (lógica)
│
├─ ui.display_ui(...)  ← punto de entrada RPS
│   ├─ gui.compose_frame()  ← fusiona webcam + HUD
│   └─ devuelve superficie compuesta
│
└─ pygame.display.flip()
```

Para **AR Catcher** el flujo es similar salvo que el bucle principal está
en `ar_catcher/game.py` y utiliza métodos de `visual_effects.py` para
postprocesar el fotograma compuesto.

---

## 6. Pipeline de Recursos

* Todas las sprites PNG viven en la carpeta `assets/` de cada juego.
* En el arranque `assets.load_images()` carga los archivos a memoria y
  los redimensiona a 100 × 100 px para el HUD.
* Los canales alfa se preservan; la composición usa overwrite simple
  porque los iconos están pre-multiplicados al cargarse con OpenCV.

---

## 7. Guía de Animaciones

* Utilice capas **aditivas** (`cv2.addWeighted`) para flashes y pulsos;
  evite shaders personalizados: la CPU es suficiente a 60 FPS.
* Mantenga los efectos pesados opcionales; protégidos por un booleano
  para que los equipos de gama baja puedan desactivarlos.
* Respete a usuarios daltónicos: no codifique estados críticos solo con
  color – acompáñelo de texto o forma.

---

## 8. Manejo de Entrada

| Fuente     | Módulo            | Notas                                  |
|------------|------------------|----------------------------------------|
| Teclado    | `pygame.event`   | `P` pausa, `Q` salir en AR Catcher.     |
| Gestos mano| MediaPipe key-points | Clasificación en `hand_gesture.py`. |

La entrada es **basada en sondeo**; no existen lecturas bloqueantes para
mantener el hilo principal receptivo.

---

## 9. Errores y Resiliencia

* Los ayudantes de dibujo validan formas/canales y lanzan `ValueError`
  si no coinciden.
* Desconexiones de webcam se propagan como `CameraFailure` y el bucle
  principal muestra un popup amigable antes de salir.
* Errores de inicialización de Pygame se encapsulan en `DisplayInitError`.

---

## 10. Rendimiento

* Objetivo de frame-rate: **60 FPS**.
* El paso de composición del HUD cuesta ≈ 1.2 ms en un portátil de gama
  media.
* Evite `cv2.resize` dentro de la ruta crítica; redimensione una vez y
  cachee.

---

## 11. Tematización y Consistencia Visual

Aunque el proyecto no es web, adoptamos un enfoque basado en sistema de
 diseño:

* **Colores**: grises neutros para fondo, colores de acento para estado.
* **Tipografía**: `FONT_HERSHEY_TRIPLEX` de OpenCV para títulos.
* **Espaciado**: margen de 20 px entre región webcam y HUD.

En el futuro podríamos migrar a un front-end web con **Tailwind CSS**
para mantener estos tokens de estilo.

---

## 12. Mejoras Futuras

* Reemplazar el renderizado de texto de OpenCV por FreeType para mayor
  nitidez.
* Añadir animaciones basadas en *tweening* mediante
  `pygame.transform.scale` para pop-ups.
* Proporcionar un menú de ajustes que permita a los jugadores personalizar
  temas de color.

---

© 2025 FAIN-AI. Todos los derechos reservados.
