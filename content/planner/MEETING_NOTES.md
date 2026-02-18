# Meeting Notes
- status: active
- type: log
- id: planner.meeting_notes
- context_dependencies: { "conventions": "../../MD_CONVENTIONS.md" }
- last_checked: 2026-01-25T17:39:00+01:00

<!-- content -->
This file contains the historical log of meetings with colleagues and collaborators. Every meeting should follow the template below.

## Meeting Template
- status: active
- type: guideline
<!-- content -->
### [YYYY-MM-DD] - [Meeting Title]
- status: todo
- type: log
- participants: []
<!-- content -->

**Agenda:**
- 

**Discussion:**
- 

**Action Items:**
- [ ] 

---

## 2026-01-25 - Setting the Intelligent Control SaaS Roadmap
- status: todo
- type: log
- participants: ["Ignacio", "Fran"]
- id: planner.meeting.20260125.roadmap
- last_checked: 2026-01-25T17:45:00+01:00
<!-- content -->

**Agenda:**
- Understand Planning Tools and Master Plan
- Cloud Situation: is snake up?
- Gitaccess?
- React vs Python
- Next steps

**Discussion:**
- Tema centralizacion: Upstream vs Downstream
- Fran se hace cargo del nodo Phase 2 del Master Plan.
- Hacer scipt que mapee las dependencias.
- Vamos a usar React.
- Darle acceso a los repositorios de git.
- En los project setup guidelines, aclararle al agente que incluya un .gitignore tipico a los lenguajes que se manajen.
- hablamos la fase 3, acordamos que viene despues de las primeras dos fases.
- Volvio el tema seguridad, pero lo dejamos para adelante en la fase 2.
- Agregamos cosas a status.
- No olvidar que se puede usar Claude en VSCode.

**Action Items:**
- Que Fran avance con Phase 2: The Cloud Bridge todo lo que pueda. En particular, poder jugar al snake desde nuestros servers en la nube.
- Que Ignacio avance con Phase 1: Local Nexus todo lo que pueda.
- En los project setup guidelines, aclararle al agente que incluya un .gitignore tipico a los lenguajes que se manajen.
- Hacer scipt que mapee las dependencias.

---

## 2026-02-03 - Status Update & Planning
- status: done
- type: log
- participants: ["Fran", "Nacho"]
- id: planner.meeting.20260203.status_update
- last_checked: 2026-02-03T20:26:00+01:00
<!-- content -->

**Agenda:**
- Knowledge Base & Central Planner Migration
- Infrastructure & Deployment
- Local Nexus & Next Steps

**Discussion:**

**Fran:**
- Mirar el knowledge base xq ya esta andando.
- Despues migrar el central planner.
- Streamlit de ambos al google cloud.
- Tiene via libre para mejorar el mergeador de knowledge base (usar el generador de prompt).
- Documentar todo en markdowns inclusive funcionamiento de infraestructura subyacente.

**Nacho:**
- Tener el central planner andando cuanto antes.
- Actualizar el central planner con el nodo del snake.
- Agregar la migracion de knowledge base et al como un nodo.
- Seguir trabajando en el local nexus.
INFRASTRUCTURE.md
**Action Items:**
- [ ] Mirar el knowledge base (Fran).
- [ ] Migrar el central planner (Fran).
- [ ] Deploy Streamlit de ambos al google cloud (Fran).
- [ ] Mejorar el mergeador de knowledge base usando prompt generator (Fran).
- [ ] Documentar infraestructura subyacente en markdown (Fran).
- [ ] Tener el central planner andando cuanto antes (Nacho).
- [ ] Actualizar el central planner con el nodo del snake (Nacho).
- [ ] Agregar la migracion de knowledge base como un nodo (Nacho).
- [ ] Seguir trabajando en el local nexus (Nacho).

---

## 2026-02-18 - Status Update & Planning
- status: doing
- type: log
- participants: ["Fran", "Nacho"]
- id: planner.meeting.20260218.status_update
- last_checked: 2026-02-18T20:57:00+01:00
<!-- content -->

**Agenda:**
- Knowledge Base & Central Planner Cleanup
- Local Nexus Design
- Google ADK
