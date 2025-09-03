# AR Catcher - Experiencia de Juego Mejorada
Un juego de realidad aumentada con gestos de mano donde los jugadores atrapan objetos que caen usando sus manos a través de una cámara.  

---

## 🎮 Características Mejoradas  

### Más Bombas y Desafíos
- **Aumento en la tasa de aparición de bombas:** Empieza en 40% y sube hasta 70% con el tiempo.  
- **Tipos de bombas con sprites únicos:**
  - **Bomba Regular (bomb.png):** -2 puntos, explosión estándar.  
  - **Mega Bomba (bomb2.png):** -3 puntos, explosión más grande, movimiento más lento.  
  - **Bomba de Racimo (cluster.png):** -1 punto, movimiento más rápido, tamaño reducido.  

### Sistema de Power-Ups
- **Escudo (shield.png):** Protege al jugador de bombas durante 8 segundos.  
- **Fruta Dorada (goldFruit.png):** Ítem raro que otorga 3x puntos y extiende el combo.  
- **Sistema de Combos:** Encadena capturas para multiplicadores de hasta 5x.  

### Mejoras Visuales
- **Efectos de Brillo:** Objetos especiales con resplandores únicos.  
- **Partículas de Explosión:** Efectos dinámicos según el tipo de bomba.  
- **UI Mejorada:** Indicadores de power-up, combos y tiempo de juego.  
- **Pantalla con Destello:** Colores diferentes para cada explosión.  

### Mejoras en la Jugabilidad
- **Dificultad Dinámica:** La tasa de bombas aumenta cada 30 segundos.  
- **Aparición más Rápida:** Objetos aparecen cada 0.8 segundos.  
- **Meta más Alta:** Condición de victoria aumentada a 15 puntos para partidas más largas.  
- **Función de Pausa:** Presiona `P` para pausar/reanudar.  

---

## 🎯 Cómo Jugar  

**Configuración:**  
Asegúrate de que tu cámara funcione y esté bien posicionada.  

**Controles:**  
- Mueve tus manos frente a la cámara.  
- Atrapa frutas para ganar puntos.  
- Evita bombas (reducen tu puntaje).  
- Recoge power-ups para obtener ventajas.  

**Teclas:**  
- `P`: Pausa/Reanuda el juego.  
- `Q`: Salir del juego.  

---

## 🚀 Primeros Pasos  

```bash
# Navega al directorio del proyecto
cd fain_ai/ar_catcher

# Probar la carga de sprites (opcional pero recomendado)
python test_sprites.py

# Ejecutar el juego
python game.py

```
## 🎨 Tipos de Objetos  

| Objeto          | Puntos | Efecto            | Especial                        | Sprite        |
|-----------------|--------|-------------------|---------------------------------|---------------|
| 🍎 Manzana      | +1     | Fruta básica      | Ninguno                         | apple.png     |
| 🍊 Naranja      | +1     | Fruta básica      | Tamaño mayor                    | orange.png    |
| ⚡ Pokeball     | +2     | Fruta bonus       | Ninguno                         | pokeball.png  |
| 💣 Bomba        | -2     | Explosión         | Destello rojo                   | bomb.png      |
| 💥 Mega Bomba   | -3     | Gran explosión    | Destello rojo, sacudida         | bomb2.png     |
| 💥 Racimo       | -1     | Explosión rápida  | Destello amarillo               | cluster.png   |
| 🌟 Fruta Dorada | +3     | Puntos bonus      | Multiplicador de combos         | goldFruit.png |
| 🛡️ Escudo       | 0      | Protección        | Bloquea bombas por 8 segundos   | shield.png    |

---

## 🔧 Características Técnicas  
- **Detección de Manos:** Usa MediaPipe para seguimiento preciso.  
- **Procesamiento en Tiempo Real:** Optimizado para fluidez.  
- **Sistema de Partículas:** Explosiones y efectos dinámicos.  
- **Gestión de Power-Ups:** Basado en temporizador.  
- **Escalado de Dificultad:** Incremento progresivo del reto.  

---

## 📱 Requisitos  
- Python 3.7+  
- OpenCV  
- MediaPipe  
- Pillow (PIL)  
- NumPy  
- Cámara web funcional  

---

## 🖼️ Sprites Necesarios  
Deben estar en `assets/sprites/`:  

- `apple.png` - Sprite de manzana  
- `orange.png` - Sprite de naranja  
- `pokeball.png` - Sprite de pokeball  
- `bomb.png` - Sprite de bomba normal  
- `bomb2.png` - Sprite de mega bomba  
- `cluster.png` - Sprite de bomba racimo  
- `goldFruit.png` - Sprite de fruta dorada  
- `shield.png` - Sprite de escudo  

---

## 🎮 Consejos para Altas Puntuaciones  
- **Construye Combos:** Encadena frutas para maximizar puntos.  
- **Usa Escudos con Cautela:** Guárdalos para cuando haya muchas bombas.  
- **Observa el Tiempo:** La tasa de bombas aumenta con los minutos.  
- **Mantente Activo:** Más movimiento = más capturas.  
- **Coordina en Multijugador:** Evita choques con tu compañero.  

---
