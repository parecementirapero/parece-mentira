# Parece Mentira — instrucciones para Claude

Canal de Shorts/Reels/TikToks (9:16) de historia, ciencia y misterios que parecen mentira.
Trabajan **dos personas (Nico y Jorge) con la misma cuenta de Claude**, cada una en su ordenador.
Este repo es la **única fuente de verdad**: lo que no esté aquí, no está decidido.

## Protocolo obligatorio (anti-pisadas)

### 1. Antes de hacer NADA
1. `git pull --rebase` en `main`.
2. Lee, en este orden: `PROJECT_STATE.md`, `TASKS.md`, `HANDOFF.md`, `DECISIONS.md`.
3. Pregunta (si no lo sabes) **quién te habla: Nico o Jorge**. Todo lo que registres lleva ese nombre.

### 2. Reservar la tarea
1. Busca la tarea en `TASKS.md`. Si no existe, créala en «Pendiente».
2. **Si está «En curso» por la otra persona, NO la toques.** Avisa y propone otra.
3. Muévela a «En curso» con `— Nico|Jorge — AAAA-MM-DD HH:MM`.
4. Commit (`tasks: reserva <tarea> (Nico|Jorge)`) y `git push` **antes de empezar a trabajar**.
5. Si el push falla: `git pull --rebase`, vuelve a mirar `TASKS.md`. Si la otra persona la reservó a la vez, gana el commit que llegó primero; tú eliges otra.

### 3. Mientras trabajas
- Una petición que contradiga `DECISIONS.md` **no se aplica en silencio**: se señala a la persona y, si confirma, se cambia `DECISIONS.md` con fecha, quién y motivo.
- Commits pequeños y frecuentes. Nada de secretos en el repo (`.env` está ignorado).
- Los vídeos y audios pesados **no** se suben a git: van a Drive (ver `DECISIONS.md`). En `lotes/` solo texto: guiones, metadatos, enlaces.

### 4. Al terminar (o al parar a medias)
1. `TASKS.md`: mueve la tarea a «Hecho» (o déjala «En curso» con una nota de dónde se quedó).
2. `PROJECT_STATE.md`: actualiza lo que cambie.
3. `HANDOFF.md`: añade una entrada arriba (fecha, quién, rama, commit, qué se hizo, pruebas, pendientes, siguiente paso).
4. Commit + `git push`. Comprueba que el push ha entrado.

## Reglas de seguridad
- Publicar en redes **solo** cuando la persona escriba «ok» para ese lote concreto en el chat.
- Nunca meter contraseñas ni códigos: los inicios de sesión los hace la persona.
- Sin compras ni gastos nuevos sin confirmación (presupuesto: 50–150 €/mes entre ambos proyectos).

## Estructura
```
CLAUDE.md          este protocolo
PROJECT_STATE.md   estado actual del proyecto
TASKS.md           tablero de tareas (pendiente / en curso / hecho)
DECISIONS.md       decisiones vigentes con fecha y motivo
HANDOFF.md         registro de traspasos (lo más reciente arriba)
lotes/AAAA-MM-DD-manana|tarde/   guiones, metadatos y enlaces de cada lote
```
