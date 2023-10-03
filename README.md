# Desarrollo de Agente Snake con PyTorch

Con el objetivo de fortalecer mis habilidades en PyTorch y el desarrollo de agentes, he tomado como base el código del juego Snake implementado en PyGame. Mi enfoque ha sido implementar una red neuronal simple con el fin de maximizar la puntuación alcanzable en el juego.

## Modelo Neuronal

La red neuronal utilizada es fundamentalmente básica, compuesta por una única capa oculta. Se sigue el esquema visualizado en la siguiente imagen:

![Esquema de la Red Neuronal](https://github.com/McGregory99/snakeAI-game/assets/85994371/b8f218db-f726-4062-8254-95141c0c3b7a)

Con esta red, la serpiente logra:

- Detectar y evitar obstáculos como paredes.
- Evitar colisiones consigo misma.
- Detectar la presencia de comida y perseguirla de manera eficiente.

## Resultados

A medida que el modelo va entrenando, en la carpeta ```/img``` se guardan gráficas con las métricas obtenidas

![250 juegos](https://github.com/McGregory99/snakeAI-game/assets/85994371/1259df00-4aab-4dc6-a028-f6759389c96c)

## Instrucciones para Utilizar Este Repositorio

1. **Clona el Repositorio:**
   - Utiliza el siguiente comando para clonar el repositorio a tu máquina local:

     ```
     git clone [URL_DEL_REPOSITORIO]
     ```

2. **Configura un Entorno Virtual:**
   - Crea un entorno virtual para este proyecto. Ejecuta los siguientes comandos:

     ```
     pip -m venv .venv
     source .venv/bin/activate  # (si estás en Windows, usa .venv\Scripts\activate.bat)
     ```

3. **Instala las Dependencias:**
   - Utiliza el siguiente comando para instalar las dependencias necesarias:

     ```
     pip install -r requirements.txt
     ```

4. **Ejecuta el Archivo Principal:**
   - Finalmente, ejecuta el archivo principal de la aplicación:

     ```
     python agent.py
     ```

Ahora deberías tener todo configurado y funcionando para utilizar este repositorio.

  
